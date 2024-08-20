def replace_placeholders(text, memory):
    if '(name)' in text:
        name = memory.get('name', '')
        text = text.replace('(name)', name if name else "ما عارف اسمك")
        
    if '(country)' in text:
        country = memory.get('country', '')
        text = text.replace('(country)', country if country else "ما عارف بلدك")
        
    if '(gender)' in text:
        gender = memory.get('gender', '')
        gender_word = "ولد" if gender == "ولد" else "بت" if gender == "بت" else "ما عارف جنسك"
        text = text.replace('(gender)', gender_word)
        
    return text
