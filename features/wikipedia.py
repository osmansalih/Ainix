import wikipedia

def get_wikipedia_summary(query):
    try:
        summary = wikipedia.summary(query, sentences=2)
        return summary
    except wikipedia.exceptions.DisambiguationError as e:
        return f"هاك دي اقتراحات: {', '.join(e.options)}"
    except wikipedia.exceptions.PageError:
        return "صراحة ما بعرف معلومات."
