import json
import os
from datetime import datetime
from features.weather import get_weather
from features.wikipedia import get_wikipedia_summary
from features.calculator import calculate_expression
from features.translator import translate_text
from features.website_opener import open_website
from features.placeholders import replace_placeholders
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.preprocessing import LabelEncoder

learned_intents_file = 'data/learned_intents.json'
intents_file = 'data/intents.json'
memory_file = 'data/memory.json'

def load_data():
    try:
        with open(learned_intents_file, 'r', encoding='utf-8') as file:
            learned_data = json.load(file)
            if not learned_data:
                learned_data = {"intents": []}
    except (FileNotFoundError, json.JSONDecodeError):
        learned_data = {"intents": []}

    with open(intents_file, 'r', encoding='utf-8') as file:
        data = json.load(file)

    return data, learned_data

def load_memory():
    try:
        with open(memory_file, 'r', encoding='utf-8') as file:
            memory = json.load(file)
    except (FileNotFoundError, json.JSONDecodeError):
        memory = {}
    return memory

def save_memory(memory):
    with open(memory_file, 'w', encoding='utf-8') as file:
        json.dump(memory, file, ensure_ascii=False, indent=4)

data, learned_data = load_data()
memory = load_memory()

all_data = data['intents'] + learned_data['intents']

patterns = []
responses = []
tags = []

for intent in all_data:
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

def add_training_data(bot_message, user_message):
    tag = "custom"
    intent_exists = False

    for intent in learned_data['intents']:
        if intent['tag'] == tag:
            intent['patterns'].append(bot_message)
            intent['responses'].append(user_message)
            intent_exists = True
            break

    if not intent_exists:
        new_intent = {
            "tag": tag,
            "patterns": [bot_message],
            "responses": [user_message]
        }
        learned_data['intents'].append(new_intent)

    with open(learned_intents_file, 'w', encoding='utf-8') as file:
        json.dump(learned_data, file, ensure_ascii=False, indent=4)

    print(f"Added training data: {bot_message} -> {user_message}")

def respond_to_query(text):
    global memory

    text_lower = text.lower()

    if "التاريخ" in text_lower or "اليوم" in text_lower:
        return replace_placeholders(f"تاريخ الليلة هو {datetime.now().strftime('%Y-%m-%d')}.", memory)
    elif "الساعة" in text_lower or "الوقت" in text_lower:
        return replace_placeholders(f"الساعة هسي {datetime.now().strftime('%H:%M:%S')}.", memory)
    elif "الطقس" in text_lower or "الجو" in text_lower:
        return replace_placeholders(get_weather(), memory)
    elif "معلومات عن" in text_lower or "منو هو" in text_lower or "شنو هو" in text_lower:
        query = text_lower.replace("معلومات عن", "").replace("منو هو", "").replace("شنو هو", "").strip()
        return replace_placeholders(get_wikipedia_summary(query), memory)
    elif "احسب" in text_lower:
        expression = text_lower.replace("احسب", "").strip()
        return replace_placeholders(calculate_expression(expression), memory)
    elif "ترجم" in text_lower:
        parts = text_lower.split(" الى ")
        if len(parts) == 2:
            phrase, language = parts
            phrase = phrase.replace("ترجم", "").strip()
            language = language.replace(" اللغة", "").strip()
            return replace_placeholders(translate_text(phrase, dest_language=language), memory)
        else:
            return replace_placeholders(f"{memory.get('name', '')}, اديني الكلام الدايرو واللغة الدايرني اترجمها", memory)
    elif "افتح" in text_lower or "شغل" in text_lower:
        site_name = text_lower.replace("افتح", "").replace("شغل", "").strip()
        return replace_placeholders(open_website(site_name), memory)
    elif "اسمي شنو" in text_lower or "ما هو اسمي" in text_lower or "اسمي منو" in text_lower or "انا منو" in text_lower or "من انا" in text_lower:
        return replace_placeholders(f"{memory.get('name', 'ما عارف اسمك')}", memory)
    elif "انا ولد" in text_lower or "انا بت" in text_lower or "انا بنت" in text_lower:
        gender = "ولد" if "ولد" in text_lower else "بت"
        memory['gender'] = gender
        save_memory(memory)
        return replace_placeholders(f"اتشرفنا والله كدا حفظتك انك {gender}.", memory)
    elif "انا من" in text_lower:
        country = text_lower.replace("انا من", "").strip()
        memory['country'] = country
        save_memory(memory)
        return replace_placeholders(f"غايتو حا اقول ليك اقدع ناس دامك من {country}.", memory)
    elif "معاك" in text_lower or "أنا اسمي" in text_lower or "اسمي" in text_lower:
        name = text_lower.replace("معاك", "").replace("أنا اسمي", "").replace("اسمي", "").strip()
        memory['name'] = name
        save_memory(memory)
        return replace_placeholders(f"اتشرفنا والله كدا عرفت اسمك يا {name}.", memory)
    else:
        pred_class = predict_class(text)
        for intent in all_data:
            if intent['tag'] == pred_class:
                response = np.random.choice(intent['responses'])
                return replace_placeholders(response, memory)
        return learn_new_intent(text)

def learn_new_intent(text):
    print(f"ما عندي فكرة عن '{text}'.")
    user_feedback = input("شنو الرد المناسب؟: ")

    last_bot_message = "هذا هو آخر رسالة من البوت"
    tag = "custom"

    add_training_data(last_bot_message, user_feedback)
    return replace_placeholders(f"اتعلمت الرد الجديد: '{user_feedback}' للتصنيف '{tag}'.", memory)

def get_tags():
    tags = set(intent['tag'] for intent in data['intents'])
    return list(tags)

def get_learned_tags():
    tags = set(intent['tag'] for intent in learned_data['intents'])
    return list(tags)

def add_tag(tag):
    if not any(intent['tag'] == tag for intent in data['intents']):
        data['intents'].append({
            "tag": tag,
            "patterns": [],
            "responses": []
        })
        with open(intents_file, 'w', encoding='utf-8') as file:
            json.dump(data, file, ensure_ascii=False, indent=4)

def remove_tag(tag):
    data['intents'] = [intent for intent in data['intents'] if intent['tag'] != tag]
    with open(intents_file, 'w', encoding='utf-8') as file:
        json.dump(data, file, ensure_ascii=False, indent=4)

if __name__ == "__main__":
    queries = [
        "اسمي عثمان",
        "أنا ولد",
        "أنا من السودان",
        "ما هو اسمي؟",
        "من ياتو دولة انا؟",
        "ما هو جنسي؟",
    ]
    
    for query in queries:
        response = respond_to_query(query)
        print(f"Query: {query}\nResponse: {response}\n")