import tkinter as tk
from tkinter import scrolledtext, messagebox, simpledialog
from chatbot_model import respond_to_query, add_training_data, get_tags, get_learned_tags
from time import sleep
import threading
from PIL import Image, ImageTk, ImageDraw, ImageFont 

def typewriter_effect(text, tag):
    for char in text:
        chat_display.insert(tk.END, char, tag)
        chat_display.update()
        sleep(0.05)
    chat_display.insert(tk.END, "\n\n")

def on_ask_button_click():
    user_query = entry.get()
    if user_query.strip() == "":
        return 
    
    chat_display.config(state=tk.NORMAL)
    chat_display.insert(tk.END, f"You: {user_query}\n", 'user')

    entry.delete(0, tk.END)

    chat_display.insert(tk.END, "Ainix is typing...\n", 'typing')
    chat_display.yview(tk.END)
    chat_display.config(state=tk.DISABLED)
    
    def bot_response():
        sleep(3)
        chat_display.config(state=tk.NORMAL)
        chat_display.delete("end-2l", "end-1l")
        response = respond_to_query(user_query)
        chat_display.insert(tk.END, f"Ainix: ", 'bot')
        typewriter_effect(response, 'bot')
        chat_display.config(state=tk.DISABLED)
        chat_display.yview(tk.END)

    threading.Thread(target=bot_response).start()

def on_train_button_click():
    user_query = entry.get()
    if user_query.strip() == "":
        return 

    chat_display.config(state=tk.NORMAL)
    bot_response = respond_to_query(user_query)
    
    add_training_data(user_query, bot_response)
    
    chat_display.insert(tk.END, f"تدريب: {user_query} -> {bot_response}\n", 'train')
    entry.delete(0, tk.END)
    chat_display.config(state=tk.DISABLED)
    chat_display.yview(tk.END)

def copy_text():
    chat_display.event_generate('<<Copy>>')

def open_settings_window():
    settings_window = tk.Toplevel(root)
    settings_window.title("Settings")
    settings_window.geometry("500x500")

    title_label = tk.Label(settings_window, text="Manage Tags", font=("Helvetica", 14, "bold"))
    title_label.pack(pady=10)

    main_tags_frame = tk.Frame(settings_window)
    main_tags_frame.pack(side=tk.LEFT, padx=10, pady=10, fill=tk.BOTH, expand=True)

    main_tags_label = tk.Label(main_tags_frame, text="Main Tags", font=("Helvetica", 12, "bold"))
    main_tags_label.pack(pady=5)

    main_tags_list = tk.Listbox(main_tags_frame, selectmode=tk.SINGLE, width=30, height=20)
    main_tags_list.pack(pady=5)

    learned_tags_frame = tk.Frame(settings_window)
    learned_tags_frame.pack(side=tk.RIGHT, padx=10, pady=10, fill=tk.BOTH, expand=True)

    learned_tags_label = tk.Label(learned_tags_frame, text="Learned Tags", font=("Helvetica", 12, "bold"))
    learned_tags_label.pack(pady=5)

    learned_tags_list = tk.Listbox(learned_tags_frame, selectmode=tk.SINGLE, width=30, height=20)
    learned_tags_list.pack(pady=5)

    def load_tags():
        main_tags_list.delete(0, tk.END)
        learned_tags_list.delete(0, tk.END)

        main_tags = get_tags()
        learned_tags = get_learned_tags()

        for tag in main_tags:
            main_tags_list.insert(tk.END, tag)

        for tag in learned_tags:
            learned_tags_list.insert(tk.END, tag)

    load_tags()

    def add_tag():
        new_tag = simpledialog.askstring("Add Tag", "Enter the new tag:")
        if new_tag:
            add_training_data(new_tag, "Example response for new tag")
            load_tags()
    
    def remove_tag():
        selected_tag = learned_tags_list.get(tk.ACTIVE)
        if selected_tag:
            confirm = messagebox.askyesno("Confirm", f"Are you sure you want to remove the tag '{selected_tag}'?")
            if confirm:
                remove_tag_from_data(selected_tag)
                load_tags()

    add_button = tk.Button(settings_window, text="Add Tag", command=add_tag)
    add_button.pack(side=tk.LEFT, padx=5, pady=10)
    
    remove_button = tk.Button(settings_window, text="Remove Tag", command=remove_tag)
    remove_button.pack(side=tk.RIGHT, padx=5, pady=10)


def add_tag_to_data(tag):
    print(f"Tag '{tag}' added to the data.")

def remove_tag_from_data(tag):
    print(f"Tag '{tag}' removed from the data.")

root = tk.Tk()
root.title("Ainix Model")

root.geometry("600x700")

title_label = tk.Label(root, text="Ainix AI", font=("Helvetica", 18, "bold"))
title_label.pack(pady=10)

chat_display = scrolledtext.ScrolledText(root, wrap=tk.WORD, height=25, width=70, state=tk.DISABLED, bg="#f5f5f5", font=("Helvetica", 14))
chat_display.pack(pady=10)

right_click_menu = tk.Menu(root, tearoff=0)
right_click_menu.add_command(label="Copy", command=copy_text)

def show_right_click_menu(event):
    chat_display.tag_add(tk.SEL, "1.0", tk.END)  
    right_click_menu.post(event.x_root, event.y_root)

chat_display.bind("<Button-3>", show_right_click_menu) 

entry_frame = tk.Frame(root)
entry_frame.pack(pady=10, padx=10, fill=tk.X)
entry = tk.Entry(entry_frame, font=("Helvetica", 14), bd=3, relief=tk.SUNKEN)
entry.pack(side=tk.LEFT, fill=tk.X, expand=True)

icon_font = ImageFont.truetype("fontawesome-webfont.ttf", 20)  
icon_text = "\uf1d8"  

image = Image.new('RGBA', (40, 40), (255, 255, 255, 0))
draw = ImageDraw.Draw(image)
draw.text((10, 10), icon_text, font=icon_font, fill=(255, 255, 255))

send_icon = ImageTk.PhotoImage(image)

ask_button = tk.Button(entry_frame, image=send_icon, command=on_ask_button_click, bg="#4CAF50", relief=tk.RAISED, bd=3)
ask_button.pack(side=tk.RIGHT, fill=tk.Y)

train_button = tk.Button(entry_frame, text="Train", command=on_train_button_click, bg="#f44336", relief=tk.RAISED, bd=3)
train_button.pack(side=tk.RIGHT, padx=5, fill=tk.Y)

settings_icon = "\uf013" 
settings_image = Image.new('RGBA', (40, 40), (255, 255, 255, 0))
settings_draw = ImageDraw.Draw(settings_image)
settings_draw.text((10, 10), settings_icon, font=icon_font, fill=(255, 255, 255))
settings_icon_image = ImageTk.PhotoImage(settings_image)

settings_button = tk.Button(root, image=settings_icon_image, command=open_settings_window, bg="#2196F3", relief=tk.RAISED, bd=3)
settings_button.pack(side=tk.TOP, anchor=tk.NE, padx=10, pady=10)

footer_label = tk.Label(root, text="Powered by Osman Salih", font=("Helvetica", 10), fg="gray")
footer_label.pack(side=tk.BOTTOM, pady=5)

chat_display.tag_config('user', foreground='blue', font=("Helvetica", 12, "bold"), justify='right')
chat_display.tag_config('bot', foreground='green', font=("Helvetica", 12), justify='left')
chat_display.tag_config('typing', foreground='gray', font=("Helvetica", 12, "italic"), justify='left')
chat_display.tag_config('train', foreground='red', font=("Helvetica", 12, "bold"), justify='left')

root.mainloop()
