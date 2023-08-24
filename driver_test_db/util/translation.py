import csv
import os
from typing import Any, Dict
from .data import Test
from .language import Language
from .translator.deepl import DeepLTranslator
from .translator.google import GoogleTranslator
from .translator.mixed import MixedTranslator
from .transformer import Transformer


class CachedTranslator(Transformer):
    def __init__(self, domain: str, dest_lang: Language, impl: Any):
        super().__init__(domain, f"translation.{dest_lang.name}")
        self.dest_lang = dest_lang
        self.impl = impl

    def _get(self, src_text: str):
        return self.impl.get(self.dest_lang, src_text)


class Translator:
    def __init__(self, domain: str):
        self.domain = domain
        self.impl = MixedTranslator()
        self.translators: Dict[Language, Any] = {}

    def get(self, dest_lang: Language, src_text: str):
        translator = self.translators.get(dest_lang)
        if not translator:
            translator = CachedTranslator(self.domain, dest_lang, self.impl)
            self.translators[dest_lang] = translator
        return translator.get(src_text)

    def translate_tests(self, dest_lang: Language, src_tests: list):
        if dest_lang == Language.FA:
            transformer = lambda text: f"{self.get(dest_lang, text)}"
        else:
            transformer = lambda text: f"{self.get(dest_lang, text)} / {text}"
        return [test.transform(transformer) for test in src_tests]

    def save_cache(self):
        for lang, translator in self.translators.items():
            translator.save_cache()

    def load_cache(self):
        for lang in Language:
            translator = CachedTranslator(self.domain, lang, self.impl)
            translator.load_cache()
            self.translators[lang] = translator