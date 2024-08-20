import tkinter as tk
from tkinter import messagebox, simpledialog
from chatbot_model import get_tags, get_learned_tags, add_tag, remove_tag

def open_settings_window(root):
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
        main_tags = get_tags()
        learned_tags = get_learned_tags()
        
        main_tags_list.delete(0, tk.END)
        learned_tags_list.delete(0, tk.END)
        
        for tag in main_tags:
            main_tags_list.insert(tk.END, tag)
        for tag in learned_tags:
            learned_tags_list.insert(tk.END, tag)

    load_tags()

    def add_tag():
        new_tag = simpledialog.askstring("Add Tag", "Enter the new tag:")
        if new_tag:
            add_tag(new_tag)
            load_tags()
    
    def remove_tag():
        selected_tag = learned_tags_list.get(tk.ACTIVE)
        if selected_tag:
            confirm = messagebox.askyesno("Confirm", f"Are you sure you want to remove the tag '{selected_tag}'?")
            if confirm:
                remove_tag(selected_tag)
                load_tags()

    add_button = tk.Button(settings_window, text="Add Tag", command=add_tag)
    add_button.pack(side=tk.LEFT, padx=5, pady=10)
    
    remove_button = tk.Button(settings_window, text="Remove Tag", command=remove_tag)
    remove_button.pack(side=tk.RIGHT, padx=5, pady=10)
