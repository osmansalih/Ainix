import webbrowser

def open_website(site_name):
    sites = {
        "انستاجرام": "https://www.instagram.com",
        "يوتيوب": "https://www.youtube.com",
        "فيس بوك": "https://www.facebook.com",
        "خمسات": "https://khamsat.com/",
        "سبوتيفاي": "https://www.spotify.com",
        "localhost": "http://localhost",
        "قوقل": "https://www.google.com",
        "جوجل": "https://www.google.com",
        "واتساب": "https://web.whatsapp.com",
        "واتس اب": "https://web.whatsapp.com",
        "Github": "https://github.com",
        "ChatGPT": "https://chatgpt.com",
        "شات جي بي تي": "https://chatgpt.com",
    }
    url = sites.get(site_name.lower())
    if url:
        webbrowser.open(url)
        return f"فتحت ليك موقع {site_name}."
    else:
        return "الموقع غير معروف."
