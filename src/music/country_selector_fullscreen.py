import tkinter as tk
import subprocess

current_player = None


def play_mp3(filename):
    global current_player

    # Stop currently playing audio
    if current_player:
        try:
            current_player.terminate()
        except:
            pass

    current_player = subprocess.Popen(
        ["mpg123", "-q", filename],
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL
    )


def choose_country(country, file):
    status_label.config(
        text=f"✈ Destination Selected: {country}"
    )

    play_mp3(file)


# Main Window
root = tk.Tk()
root.title("Country Destination Selector")

# Fullscreen
root.attributes("-fullscreen", True)

# Background
root.configure(bg="#1E293B")


# Exit button (top right)
exit_btn = tk.Button(
    root,
    text="✕ Exit",
    font=("Arial", 14, "bold"),
    bg="#DC2626",
    fg="white",
    command=root.destroy
)
exit_btn.place(relx=0.98, rely=0.02, anchor="ne")


# Title
title_label = tk.Label(
    root,
    text="🌎 Select Your Destination",
    font=("Arial", 32, "bold"),
    bg="#1E293B",
    fg="white"
)
title_label.pack(pady=40)


# Button Frame
button_frame = tk.Frame(root, bg="#1E293B")
button_frame.pack(expand=True)


# Country Buttons
buttons = [
    ("🇯🇵 Japan", "#EF4444", "/home/pi/Downloads/Test.mp3"),
    ("🇨🇳 China", "#F59E0B", "/home/pi/Downloads/China.mp3"),
    ("🇹🇼 Taiwan", "#3B82F6", "/home/pi/Downloads/Taiwan.mp3"),
    ("🇻🇳 Vietnam", "#10B981", "/home/pi/Downloads/Vietnam.mp3")
]

for i, (country, color, mp3) in enumerate(buttons):
    btn = tk.Button(
        button_frame,
        text=country,
        font=("Arial", 22, "bold"),
        bg=color,
        fg="white",
        width=20,
        height=3,
        relief="raised",
        bd=4,
        command=lambda c=country, f=mp3:
            choose_country(c, f)
    )

    btn.grid(
        row=i // 2,
        column=i % 2,
        padx=20,
        pady=20
    )


# Status Label
status_label = tk.Label(
    root,
    text="Please choose a destination",
    font=("Arial", 20),
    bg="#1E293B",
    fg="#CBD5E1"
)

status_label.pack(pady=40)

root.mainloop()