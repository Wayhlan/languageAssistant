import os
import time
import json
from transformers import MarianMTModel, MarianTokenizer

dictionnary_file_path = 'res/tmp/translations.json'

class Translator:
    def __init__(self, src_lang='ru', dest_lang='en'):
        model_name = f'Helsinki-NLP/opus-mt-{src_lang}-{dest_lang}'
        print(f"Initializing translation model '{model_name}'")
        start = time.time()
        self.tokenizer = MarianTokenizer.from_pretrained(model_name)
        self.model = MarianMTModel.from_pretrained(model_name)
        end = time.time()
        print(f'Model ready in {round(end - start, 2)} seconds\n')

    def translate(self, text):
        start = time.time()
        translated = self.model.generate(**self.tokenizer(text, return_tensors="pt", padding=True))
        translated_text = [self.tokenizer.decode(t, skip_special_tokens=True) for t in translated]
        end = time.time()
        time_elapsed = round(end - start, 2)
        print(f'Translator model applied in {time_elapsed} seconds, for text : "{text}" -> "{translated_text[0]}"')
        return translated_text[0]

    def load_translations(self, filename=dictionnary_file_path):
        if os.path.exists(filename):
            with open(filename, 'r', encoding='utf-8') as f:
                return json.load(f)
        return {}

    def save_translations(self, translations, filename=dictionnary_file_path):
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(translations, f, ensure_ascii=False, indent=4)

    def translate_text(self, text):
        text = text.lower()
        translations = self.load_translations()
        if text not in translations:
            try:
                translation = self.translate(text)
                translations[text] = translation
                self.save_translations(translations)
            except Exception as e:
                print(f"Error translating text '{text}': {e}")
                return None
        return translations[text]
    
    def print_all_translations(self):
        translations = self.load_translations()
        for russian, english in translations.items():
            if english:
                print(f"{russian} -> {english}")
            else:
                print(f"{russian} -> Translation failed")