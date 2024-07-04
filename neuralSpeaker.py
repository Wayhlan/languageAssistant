import os
os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = "hide"
import time

import torch
import numpy as np
import wave
import pygame
from transliterate import translit
from num2words import num2words
import re


class NeuralSpeaker:
    def __init__(self, language='ru'):
        print('Initializing neural speaker model')
        start = time.time()
        device = torch.device('cpu')
        torch.set_num_threads(4)
        local_file = f'res/{language}_speaker_model.pt'
        if not os.path.isfile(local_file):
            torch.hub.download_url_to_file('https://models.silero.ai/models/tts/ru/v3_1_ru.pt',
                                           local_file)
        self.__model = torch.package.PackageImporter(local_file).load_pickle("tts_models", "model")
        self.__model.to(device)
        end = time.time()
        print(f'Model ready in {round(end - start, 2)} seconds\n')

    @staticmethod
    def __num2words_ru(match):
        clean_number = match.group().replace(',', '.')
        return num2words(clean_number, lang='ru')

    # Speakers available: aidar, baya, kseniya, xenia, eugene, random
    def speak(self, words, speaker='xenia', save_file=False, sample_rate=48000):
        words = translit(words, 'ru')
        words = re.sub(r'-?[0-9][0-9,._]*', self.__num2words_ru, words)

        example_text = f'{words}'
        if sample_rate not in [48000, 24000, 8000]:
            sample_rate = 48000

        start = time.time()
        try:
            audio = self.__model.apply_tts(text=example_text,
                                           speaker=speaker,
                                           sample_rate=sample_rate, )
        except ValueError:
            print('Bad input')
            return
        end = time.time()
        time_elapsed = round(end - start, 2)
        print(f'Speaker model applied in {time_elapsed} seconds, for text : "{words}"')
        audio = audio.numpy()
        audio *= 32767 / np.max(np.abs(audio))
        audio = audio.astype(np.int16)

        file_name = 'res/tmp/output.wav'
        if not os.path.exists('res/tmp/'):
            os.makedirs('res/tmp/')
        with wave.open(file_name, 'w') as wf:
            wf.setnchannels(1)
            wf.setsampwidth(2)  # 2 bytes per sample
            wf.setframerate(sample_rate)
            wf.writeframes(audio.tobytes())
            wf.close()

        pygame.mixer.init()
        pygame.mixer.music.load(file_name)
        pygame.mixer.music.play()
        while pygame.mixer.music.get_busy():
            pass
        pygame.mixer.music.unload()

        return