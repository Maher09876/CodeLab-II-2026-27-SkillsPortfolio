import random
from pathlib import Path
import tkinter as tk
from tkinter import ttk, messagebox


BG = "#F3F6FA"
CARD = "#FFFFFF"
DARK = "#172B4D"
MUTED = "#667085"
BLUE = "#315EFB"
FONT = ("Segoe UI", 10)


class JokeAssistantApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Joke Assistant | Programming Skills Portfolio")
        self.root.geometry("720x500")
        self.root.minsize(600, 430)
        self.root.configure(bg=BG)

        self.jokes = self.loadJokes()
        self.currentJoke = None
        self.punchlineVisible = False
        self.configure_style()
        self.build_interface()

    def configure_style(self):
        style = ttk.Style()
        style.theme_use("clam")
        style.configure("TButton", font=("Segoe UI", 10, "bold"), padding=(12, 9))
        style.configure("Primary.TButton", background=BLUE, foreground="white")
        style.map("Primary.TButton", background=[("active", "#2449D8")])

    # AI-assisted section: read and split each setup/punchline line from the text file.
    def loadJokes(self):
        file_path = Path(__file__).resolve().parent / "resources" / "randomJokes.txt"
        loaded_jokes = []
        try:
            with file_path.open("r", encoding="utf-8") as file:
                for line in file:
                    line = line.strip()
                    if not line:
                        continue
                    setup, separator, punchline = line.partition("?")
                    if separator and setup.strip() and punchline.strip():
                        setup = setup.strip()
                        if setup.startswith("- "):
                            setup = setup[2:]
                        loaded_jokes.append((setup + "?", punchline.strip()))
        except FileNotFoundError:
            messagebox.showerror(
                "Joke file not found",
                "The file resources/randomJokes.txt is missing. Add the resource file and restart the app."
            )
        except OSError as error:
            messagebox.showerror("File error", f"The joke file could not be read:\n{error}")
        return loaded_jokes

    def build_interface(self):
        header = tk.Frame(self.root, bg=DARK, padx=28, pady=20)
        header.pack(fill="x")
        tk.Label(header, text="ALEXA, TELL ME A JOKE", bg=DARK, fg="white",
                 font=("Segoe UI", 18, "bold")).pack(anchor="w")
        tk.Label(header, text="A small joke assistant powered by a text-file collection.",
                 bg=DARK, fg="#D6DDF0", font=("Segoe UI", 10)).pack(anchor="w", pady=(4, 0))

        card = tk.Frame(self.root, bg=CARD, padx=30, pady=26,
                        highlightbackground="#E1E7F0", highlightthickness=1)
        card.pack(fill="both", expand=True, padx=36, pady=28)

        tk.Label(card, text="READY FOR A LAUGH?", bg=CARD, fg=MUTED,
                 font=("Segoe UI", 9, "bold")).pack()
        self.setupLabel = tk.Label(
            card, text="Press the button below and I will find a joke for you.",
            bg=CARD, fg=DARK, font=("Segoe UI", 16, "bold"),
            wraplength=570, justify="center", height=4
        )
        self.setupLabel.pack(fill="x", pady=(16, 6))

        self.punchlineLabel = tk.Label(card, text="", bg=CARD, fg=BLUE,
                                       font=("Segoe UI", 12), wraplength=570,
                                       justify="center", height=2)
        self.punchlineLabel.pack(fill="x", pady=(4, 15))

        self.statusLabel = tk.Label(card, text="The punchline stays hidden until you ask.",
                                    bg=CARD, fg=MUTED, font=("Segoe UI", 9))
        self.statusLabel.pack(pady=(0, 16))

        buttons = tk.Frame(card, bg=CARD)
        buttons.pack()
        self.tellButton = ttk.Button(buttons, text="Alexa tell me a Joke",
                                     style="Primary.TButton", command=self.tellJoke)
        self.tellButton.grid(row=0, column=0, padx=5, pady=5)
        self.punchlineButton = ttk.Button(buttons, text="Show Punchline",
                                          command=self.showPunchline, state="disabled")
        self.punchlineButton.grid(row=0, column=1, padx=5, pady=5)
        self.nextButton = ttk.Button(buttons, text="Next Joke",
                                     command=self.nextJoke, state="disabled")
        self.nextButton.grid(row=1, column=0, padx=5, pady=5)
        ttk.Button(buttons, text="Quit", command=self.root.destroy).grid(
            row=1, column=1, padx=5, pady=5
        )

    # Select one random setup and punchline pair from the loaded list.
    def tellJoke(self):
        if not self.jokes:
            messagebox.showwarning("No jokes available", "Add valid jokes to resources/randomJokes.txt.")
            return
        self.currentJoke = random.choice(self.jokes)
        self.punchlineVisible = False
        self.setupLabel.config(text=self.currentJoke[0])
        self.punchlineLabel.config(text="")
        self.statusLabel.config(text="Joke selected. Reveal the punchline when you are ready.")
        self.punchlineButton.config(state="normal")
        self.nextButton.config(state="normal")

    # Reveal the punchline that belongs to the currently selected joke.
    def showPunchline(self):
        if self.currentJoke is None:
            return
        self.punchlineLabel.config(text=self.currentJoke[1])
        self.statusLabel.config(text="There you go!")
        self.punchlineVisible = True
        self.punchlineButton.config(state="disabled")

    # Choosing Next Joke selects another pair and hides the previous punchline.
    def nextJoke(self):
        if not self.jokes:
            return
        self.tellJoke()


def main():
    root = tk.Tk()
    JokeAssistantApp(root)
    root.mainloop()


if __name__ == "__main__":
    main()
