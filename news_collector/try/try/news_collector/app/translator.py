import deepl

DEEPL_API_KEY = "49a435b1-7380-4a48-bf9d-11b5db85f42b:fx"

def translate_text(text, target_lang="RU"):
    translator = deepl.Translator(DEEPL_API_KEY)
    result = translator.translate_text(text, target_lang=target_lang)
    return result.text

def translate_article(article):
    return {
        "title": translate_text(article["title"]),
        "summary": translate_text(article["summary"]),
        "full_text": translate_text(article["full_text"]),
        "published": article["published"],
        "media": article["media"],
        "link": article["link"]
    }
