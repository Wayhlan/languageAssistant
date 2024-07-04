import os
os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = "hide"
import time

import torch
import numpy as np
import wave
from pygame import mixer
from pydub import AudioSegment
from transliterate import translit
from num2words import num2words
import re

file_name = 'res/tmp/output.wav'
slowed_file_name = 'res/tmp/slowed_output.wav'

def speed_change(sound, speed=1.0):
    sound_with_altered_frame_rate = sound._spawn(sound.raw_data, overrides={
        "frame_rate": int(sound.frame_rate * speed)
    })
    return sound_with_altered_frame_rate.set_frame_rate(sound.frame_rate)

class NeuralSpeaker:
    def __init__(self, language='ru'):
        print('Initializing neural speaker model')
        start = time.time()
        device = torch.device('cpu')
        torch.set_num_threads(4)
        local_file = f'res/v4_{language}.pt'
        if not os.path.isfile(local_file):
            torch.hub.download_url_to_file('https://models.silero.ai/models/tts/ru/v4_ru.pt',
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

        if not os.path.exists('res/tmp/'):
            os.makedirs('res/tmp/')
        with wave.open(file_name, 'w') as wf:
            wf.setnchannels(1)
            wf.setsampwidth(2)  # 2 bytes per sample
            wf.setframerate(sample_rate)
            wf.writeframes(audio.tobytes())
            wf.close()

        mixer.init()
        mixer.music.load(file_name)
        mixer.music.play()
        while mixer.music.get_busy():
            pass
        mixer.music.unload()
        mixer.quit()
        return

    def runAudioFile(self):
        try:
            audio_object = AudioSegment.from_file(file_name)
            slowed_audio = speed_change(audio_object, 0.9)
            slowed_audio.export(slowed_file_name, format="wav")

            mixer.init()
            mixer.music.load(slowed_file_name)
            mixer.music.play()
            while mixer.music.get_busy():
                pass
            mixer.music.unload()
            mixer.quit()
        except Exception as e:
            print(f"Exception while reading audio file : {e}")