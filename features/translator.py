from deep_translator import GoogleTranslator

def translate_text(text, dest_language='en'):
    try:
        dest_language = dest_language.strip().lower()
        translation = GoogleTranslator(source='auto', target=dest_language).translate(text)
        return f"الترجمة: {translation}"
    except Exception as e:
        return f"في خطأ في الترجمة: {e}"
