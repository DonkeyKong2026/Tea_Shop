import tkinter as tk
import subprocess
import sys
from pathlib import Path

sys.path.append(str(Path(__file__).resolve().parent.parent / "payment"))
from card_reader import CardReader, HCSR04

BACKGROUND_COLOR = "#1E293B"
TEXT_COLOR = "white"
SUBTLE_TEXT_COLOR = "#CBD5E1"
CARD_POLL_INTERVAL_MS = 100

current_player = None
pending_selection = None
card_poll_job = None


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
    """Remember the selected country and ask the customer to pay for it."""
    global pending_selection

    pending_selection = (country, file)
    show_payment_screen(country)


def complete_selection(country, file):
    """Announce the paid-for country and play its track."""
    status_label.config(
        text=f"✓ Payment accepted\n✈ Destination Selected: {country}"
    )

    play_mp3(file)


def draw_wifi_icon(canvas, center_x, base_y):
    """Draw a wifi signal icon: a dot with three arcs above it."""
    for radius in (35, 70, 105):
        canvas.create_arc(
            center_x - radius, base_y - radius,
            center_x + radius, base_y + radius,
            start=45, extent=90,
            style=tk.ARC, outline=TEXT_COLOR, width=14
        )

    dot_radius = 12
    canvas.create_oval(
        center_x - dot_radius, base_y - dot_radius,
        center_x + dot_radius, base_y + dot_radius,
        fill=TEXT_COLOR, outline=TEXT_COLOR
    )


def show_payment_screen(country):
    """Swap the country buttons for the tap-to-pay prompt and start watching the sensor."""
    payment_item_label.config(text=country)
    button_frame.pack_forget()
    payment_frame.pack(expand=True, before=status_label)
    status_label.config(text="Waiting for payment...")

    card_reader.reset()
    poll_card_reader()


def show_selection_screen():
    """Stop watching the sensor and bring back the country buttons."""
    global card_poll_job

    if card_poll_job is not None:
        root.after_cancel(card_poll_job)
        card_poll_job = None

    payment_frame.pack_forget()
    button_frame.pack(expand=True, before=status_label)


def poll_card_reader():
    """Check the sensor once and either finish the payment or check again shortly."""
    global card_poll_job

    if card_reader.check_for_tap():
        card_poll_job = None
        show_selection_screen()
        complete_selection(*pending_selection)
    else:
        card_poll_job = root.after(CARD_POLL_INTERVAL_MS, poll_card_reader)


def cancel_payment():
    """Abandon the current payment and return to the country buttons."""
    show_selection_screen()
    status_label.config(text="Please choose a destination")


def close_app():
    """Stop the music, release the sensor pins, and close the window."""
    if current_player:
        current_player.terminate()
    sensor.cleanup()
    root.destroy()


sensor = HCSR04()
card_reader = CardReader(sensor)


# Main Window
root = tk.Tk()
root.title("Country Destination Selector")

# Fullscreen
root.attributes("-fullscreen", True)

# Background
root.configure(bg="#1E293B")
root.protocol("WM_DELETE_WINDOW", close_app)


# Exit button (top right)
exit_btn = tk.Button(
    root,
    text="✕ Exit",
    font=("Arial", 14, "bold"),
    bg="#DC2626",
    fg="white",
    command=close_app
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


# Payment Screen (shown after a country is chosen)
payment_frame = tk.Frame(root, bg=BACKGROUND_COLOR)

payment_prompt_label = tk.Label(
    payment_frame,
    text="Tap card to pay",
    font=("Arial", 32, "bold"),
    bg=BACKGROUND_COLOR,
    fg=TEXT_COLOR
)
payment_prompt_label.pack(pady=10)

payment_item_label = tk.Label(
    payment_frame,
    text="",
    font=("Arial", 22),
    bg=BACKGROUND_COLOR,
    fg=SUBTLE_TEXT_COLOR
)
payment_item_label.pack(pady=10)

wifi_canvas = tk.Canvas(
    payment_frame,
    width=260,
    height=150,
    bg=BACKGROUND_COLOR,
    highlightthickness=0
)
draw_wifi_icon(wifi_canvas, center_x=130, base_y=130)
wifi_canvas.pack(pady=20)

cancel_btn = tk.Button(
    payment_frame,
    text="✕ Cancel",
    font=("Arial", 18, "bold"),
    bg="#475569",
    fg=TEXT_COLOR,
    width=12,
    command=cancel_payment
)
cancel_btn.pack(pady=10)


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