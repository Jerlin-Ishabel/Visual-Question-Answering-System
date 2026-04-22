from deep_translator import GoogleTranslator # type: ignore

LANG_MAP = {
    "English": "en",
    "Hindi": "hi",
    "Tamil": "ta",
    "Malayalam": "ml",
    "Telugu": "te"
}


def translate_from_english(text, target_language):
    """
    Translate English text to selected language
    """

    if target_language == "English":
        return text

    try:
        lang_code = LANG_MAP.get(target_language, "en")

        translated = GoogleTranslator(
            source="en",
            target=lang_code
        ).translate(text)

        return translated

    except Exception:
        return text
