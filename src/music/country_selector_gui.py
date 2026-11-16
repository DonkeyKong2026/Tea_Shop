import tkinter as tk
from tkinter import ttk
import subprocess


def play_mp3(filename):
    try:
        subprocess.Popen(
            ["mpg123", filename, "-q"],
            stdin=subprocess.PIPE,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE
        )
    except Exception as e:
        result_label.config(text=f"Error playing file:\n{e}")


def select_country():
    country = country_var.get()

    if country == "Japan":
        result_label.config(text="To Japan we go")
        play_mp3("/home/pi/Downloads/Test.mp3")

    elif country == "China":
        result_label.config(text="To China we go")
        play_mp3("/home/pi/Downloads/China.mp3")

    elif country == "Taiwan":
        result_label.config(text="To Taiwan we go")
        play_mp3("/home/pi/Downloads/Taiwan.mp3")

    elif country == "Vietnam":
        result_label.config(text="To Vietnam we go")
        play_mp3("/home/pi/Downloads/Vietnam.mp3")

    else:
        result_label.config(
            text="Sorry, we don't operate in that country just yet"
        )


# Main Window
root = tk.Tk()
root.title("Country Selector")
root.geometry("400x250")
root.resizable(False, False)

# Title
title_label = tk.Label(
    root,
    text="Select a Country",
    font=("Arial", 16, "bold")
)
title_label.pack(pady=20)

# Dropdown
country_var = tk.StringVar()
country_dropdown = ttk.Combobox(
    root,
    textvariable=country_var,
    state="readonly",
    width=25
)

country_dropdown["values"] = (
    "Japan",
    "China",
    "Taiwan",
    "Vietnam"
)

country_dropdown.current(0)
country_dropdown.pack(pady=10)

# Button
select_button = tk.Button(
    root,
    text="Go",
    command=select_country,
    width=15,
    height=2
)
select_button.pack(pady=15)

# Result Label
result_label = tk.Label(
    root,
    text="",
    font=("Arial", 12)
)
result_label.pack(pady=10)

root.mainloop()