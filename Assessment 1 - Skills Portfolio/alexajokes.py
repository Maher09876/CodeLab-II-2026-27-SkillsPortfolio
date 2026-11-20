
import tkinter as tk
import random
from tkinter import messagebox

jokes = []
punchline = ""


def loadJokes():
    global jokes

    try:
        file = open("randomJokes.txt", "r")

        for line in file:
            line = line.strip()

            if line.startswith("- "):
                line = line[2:]

            if "?" in line:
                setup, answer = line.split("?", 1)
                jokes.append((setup + "?", answer))

        file.close()

    except FileNotFoundError:
        messagebox.showerror("Error", "Joke file not found.")


def tellJoke():
    global punchline

    if len(jokes) == 0:
        messagebox.showinfo("Jokes", "No jokes found.")
        return

    joke = random.choice(jokes)

    setupLabel.config(text=joke[0])
    punchlineLabel.config(text="")

    punchline = joke[1]


def showPunchline():
    if punchline == "":
        messagebox.showinfo("Jokes", "Choose a joke first.")
    else:
        punchlineLabel.config(text=punchline)


# Main window
window = tk.Tk()
window.title("Alexa Tell Me a Joke")
window.geometry("400x300")


titleLabel = tk.Label(window, text="Alexa Tell Me a Joke")
titleLabel.pack(pady=15)

setupLabel = tk.Label(window, text="Click the button for a joke.")
setupLabel.pack(pady=15)

punchlineLabel = tk.Label(window, text="")
punchlineLabel.pack(pady=10)


tk.Button(window, text="Alexa tell me a Joke",
          command=tellJoke).pack(pady=5)

tk.Button(window, text="Show Punchline",
          command=showPunchline).pack(pady=5)

tk.Button(window, text="Next Joke",
          command=tellJoke).pack(pady=5)

tk.Button(window, text="Quit",
          command=window.destroy).pack(pady=5)


loadJokes()

window.mainloop()