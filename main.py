import sys
sys.stdout.reconfigure(encoding='utf-8')
import random

import translator
import neuralSpeaker


def generate_random_excluding(exclusion_list, range_start, range_end):
    valid_numbers = [num for num in range(range_start, range_end + 1) if num not in exclusion_list]
    if not valid_numbers:
        raise ValueError("No valid numbers available in the given range")
    
    return random.choice(valid_numbers)

def print_translations_from_dictionnary(dictionnary):
    for russian, english in dictionnary.items():
        if english:
            print(f"{russian} -> {english}")
        else:
            print(f"{russian} -> Translation failed")

def speak_translations_from_dictionnary(dictionnary, speaker):
    for russian, english in dictionnary.items():
        speaker.speak(russian)

def main():
    m_speaker = neuralSpeaker.NeuralSpeaker()
    m_translator = translator.Translator()
    translations = m_translator.load_translations()
    for input_text in ["Привет! Как дела ?", "Это тест", "Я инженер", "ещё", "иногда", "играть"]:
        translation, translations = m_translator.translate_text(input_text, translations)
        m_speaker.speak(input_text)
    m_translator.save_translations(translations)
    # print_translations_from_dictionnary(m_translator.load_translations())
    # speak_translations_from_dictionnary(m_translator.load_translations(), m_speaker)



if __name__ == "__main__":
    main()