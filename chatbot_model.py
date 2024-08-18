import json
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.preprocessing import LabelEncoder
from datetime import datetime
import wikipedia
from deep_translator import GoogleTranslator

with open('config.json') as config_file:
    config = json.load(config_file)

with open('data/intents.json', 'r', encoding='utf-8') as file:
    data = json.load(file)

patterns = []
responses = []
tags = []

for intent in data['intents']:
    for pattern in intent['patterns']:
        patterns.append(pattern)
        responses.append(intent['responses'][0])
        tags.append(intent['tag'])

vectorizer = TfidfVectorizer()
X = vectorizer.fit_transform(patterns)

le = LabelEncoder()
y = le.fit_transform(tags)

def predict_class(text):
    text_vec = vectorizer.transform([text])
    similarities = cosine_similarity(text_vec, X)
    best_match_idx = np.argmax(similarities)
    return tags[best_match_idx]

def get_weather():
    return "لازم تظبط الطقس من اعدادات البوت (config.json)."

def get_wikipedia_summary(query):
    try:
        summary = wikipedia.summary(query, sentences=2)
        return summary
    except wikipedia.exceptions.DisambiguationError as e:
        return f"هاك دي اقتراحات: {', '.join(e.options)}"
    except wikipedia.exceptions.PageError:
        return "صراحة ما بعرف معلومات."

def calculate_expression(expression):
    try:
        result = eval(expression)
        return f"الناتج هو {result}."
    except Exception as e:
        return f"خطأ في الحسابات: {e}"

def translate_text(text, dest_language='en'):
    try:
        dest_language = dest_language.strip().lower()
        translation = GoogleTranslator(source='auto', target=dest_language).translate(text)
        return f"الترجمة: {translation}"
    except Exception as e:
        return f"في خطأ في الترجمة: {e}"

def respond_to_query(text):
    text_lower = text.lower()

    if "التاريخ" in text_lower or "اليوم" in text_lower:
        return f"تاريخ الليلة هو {datetime.now().strftime('%Y-%m-%d')}."
    elif "الساعة" in text_lower or "الوقت" in text_lower:
        return f"الساعة هسي {datetime.now().strftime('%H:%M:%S')}."
    elif "الطقس" in text_lower or "الجو" in text_lower:
        return get_weather()
    elif "معلومات عن" in text_lower or "منو هو" in text_lower or "شنو هو" in text_lower:
        query = text_lower.replace("معلومات عن", "").replace("منو هو", "").replace("شنو هو", "").strip()
        return get_wikipedia_summary(query)
    elif "احسب" in text_lower:
        expression = text_lower.replace("احسب", "").strip()
        return calculate_expression(expression)
    elif "ترجم" in text_lower:
        parts = text_lower.split(" الى ")
        if len(parts) == 2:
            phrase, language = parts
            phrase = phrase.replace("ترجم", "").strip()
            language = language.replace(" اللغة", "").strip()  
            return translate_text(phrase, dest_language=language)
        else:
            return "اديني الكلام الدايرو واللغة الدايرني اترجمها."
    else:
        pred_class = predict_class(text)
        for intent in data['intents']:
            if intent['tag'] == pred_class:
                return np.random.choice(intent['responses'])

    return "معليش لكن ما فهمت."

if __name__ == "__main__":
    queries = [
        "عندك نكتة بتضحك؟",
        "كيف الجو الليلة؟",
        "تاريخ الليلة كم؟",
        "الساعة هسي كم؟",
        "اديني معلومات عن اينشتاين",
        "منو هو دونالد ترامب",
        "احسب 3 + 4 * 2.",
        "ترجم اهلا للغة الاسبانية."
    ]
    
    for query in queries:
        response = respond_to_query(query)
        print(f"Query: {query}\nResponse: {response}\n")
