import random
import tkinter as tk
from tkinter import ttk


# The colours and fonts are kept in one place to make the interface easy to edit.
BG = "#F3F6FA"
CARD = "#FFFFFF"
DARK = "#172B4D"
MUTED = "#667085"
BLUE = "#315EFB"
GREEN = "#16845B"
RED = "#C83D4D"
FONT = ("Segoe UI", 10)


class MathsQuizApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Maths Quiz | Programming Skills Portfolio")
        self.root.geometry("760x570")
        self.root.minsize(650, 500)
        self.root.configure(bg=BG)

        self.score = 0
        self.questionNumber = 0
        self.attempts = 0
        self.minimum = 1
        self.maximum = 9
        self.num1 = 0
        self.num2 = 0
        self.operation = "+"
        self.correctAnswer = 0
        self.answerSubmitted = False

        self.configure_style()
        self.displayMenu()

    def configure_style(self):
        style = ttk.Style()
        style.theme_use("clam")
        style.configure("TButton", font=("Segoe UI", 10, "bold"), padding=(13, 9))
        style.configure("Primary.TButton", background=BLUE, foreground="white")
        style.map("Primary.TButton", background=[("active", "#2449D8")])
        style.configure("TEntry", font=("Segoe UI", 14), padding=8)
        style.configure("TRadiobutton", background=CARD, font=FONT)

    def clear_window(self):
        for widget in self.root.winfo_children():
            widget.destroy()

    def make_header(self, subtitle):
        header = tk.Frame(self.root, bg=DARK, padx=28, pady=20)
        header.pack(fill="x")
        tk.Label(header, text="MATHS QUIZ", bg=DARK, fg="white",
                 font=("Segoe UI", 19, "bold")).pack(anchor="w")
        tk.Label(header, text=subtitle, bg=DARK, fg="#D6DDF0",
                 font=("Segoe UI", 10)).pack(anchor="w", pady=(4, 0))

    # Required function: displayMenu shows the difficulty choices before the quiz.
    def displayMenu(self):
        self.clear_window()
        self.make_header("Choose a level and answer 10 arithmetic questions.")

        card = tk.Frame(self.root, bg=CARD, padx=34, pady=30,
                        highlightbackground="#E1E7F0", highlightthickness=1)
        card.pack(fill="both", expand=True, padx=42, pady=34)

        tk.Label(card, text="DIFFICULTY LEVEL", bg=CARD, fg=DARK,
                 font=("Segoe UI", 15, "bold")).pack(anchor="w")
        tk.Label(card, text="Choose how challenging you want the questions to be.",
                 bg=CARD, fg=MUTED, font=FONT).pack(anchor="w", pady=(5, 20))

        self.difficulty = tk.StringVar(value="Easy")
        choices = [
            ("Easy", "Single-digit numbers (1 to 9)"),
            ("Moderate", "Double-digit numbers (10 to 99)"),
            ("Advanced", "Four-digit numbers (1000 to 9999)"),
        ]
        for name, description in choices:
            line = tk.Frame(card, bg="#F8FAFC", padx=14, pady=11)
            line.pack(fill="x", pady=5)
            ttk.Radiobutton(line, text=name, value=name,
                            variable=self.difficulty).pack(anchor="w")
            tk.Label(line, text=description, bg="#F8FAFC", fg=MUTED,
                     font=("Segoe UI", 9)).pack(anchor="w", padx=24, pady=(2, 0))

        ttk.Button(card, text="Start quiz", style="Primary.TButton",
                   command=self.startQuiz).pack(anchor="e", pady=(24, 0))

    def startQuiz(self):
        levels = {
            "Easy": (1, 9),
            "Moderate": (10, 99),
            "Advanced": (1000, 9999),
        }
        self.minimum, self.maximum = levels[self.difficulty.get()]
        self.score = 0
        self.questionNumber = 0
        self.displayProblem()

    # Required function: randomInt returns a random number within the selected level.
    def randomInt(self, minimum, maximum):
        return random.randint(minimum, maximum)

    # Required function: decideOperation randomly returns addition or subtraction.
    def decideOperation(self):
        return random.choice(["+", "-"])

    # Required function: displayProblem prepares and displays the current question.
    def displayProblem(self):
        self.questionNumber += 1
        self.attempts = 1
        self.answerSubmitted = False
        self.num1 = self.randomInt(self.minimum, self.maximum)
        self.num2 = self.randomInt(self.minimum, self.maximum)
        self.operation = self.decideOperation()

        # Swap subtraction values when needed so the answer is not negative.
        if self.operation == "-" and self.num2 > self.num1:
            self.num1, self.num2 = self.num2, self.num1

        if self.operation == "+":
            self.correctAnswer = self.num1 + self.num2
        else:
            self.correctAnswer = self.num1 - self.num2

        self.clear_window()
        self.make_header(f"{self.difficulty.get()} level  •  Question {self.questionNumber} of 10")

        card = tk.Frame(self.root, bg=CARD, padx=34, pady=28,
                        highlightbackground="#E1E7F0", highlightthickness=1)
        card.pack(fill="both", expand=True, padx=42, pady=32)

        top = tk.Frame(card, bg=CARD)
        top.pack(fill="x")
        tk.Label(top, text=f"QUESTION {self.questionNumber:02d} / 10", bg=CARD,
                 fg=MUTED, font=("Segoe UI", 9, "bold")).pack(side="left")
        tk.Label(top, text=f"SCORE  {self.score}/100", bg=CARD,
                 fg=BLUE, font=("Segoe UI", 10, "bold")).pack(side="right")

        tk.Label(card, text=f"{self.num1}  {self.operation}  {self.num2}  = ?",
                 bg=CARD, fg=DARK, font=("Segoe UI", 31, "bold")).pack(pady=(42, 24))
        tk.Label(card, text="Enter your answer below", bg=CARD, fg=MUTED,
                 font=FONT).pack()

        self.answerEntry = ttk.Entry(card, justify="center", width=18)
        self.answerEntry.pack(pady=12)
        self.answerEntry.bind("<Return>", lambda _event: self.submitAnswer())
        self.answerEntry.focus_set()

        self.feedbackLabel = tk.Label(card, text="You have two attempts for each question.",
                                      bg=CARD, fg=MUTED, font=FONT)
        self.feedbackLabel.pack(pady=(3, 12))
        self.submitButton = ttk.Button(card, text="Submit answer", style="Primary.TButton",
                                        command=self.submitAnswer)
        self.submitButton.pack()

    # Required function: isCorrect checks the submitted answer against the answer key.
    def isCorrect(self, userAnswer, correctAnswer):
        return userAnswer == correctAnswer

    def submitAnswer(self):
        if self.answerSubmitted:
            return
        raw_answer = self.answerEntry.get().strip()
        if not raw_answer:
            self.feedbackLabel.config(text="Please enter an answer.", fg=RED)
            return
        try:
            user_answer = int(raw_answer)
        except ValueError:
            self.feedbackLabel.config(text="Please enter a whole number.", fg=RED)
            return

        if self.isCorrect(user_answer, self.correctAnswer):
            if self.attempts == 1:
                self.score += 10
                message = "Correct! You earned 10 points."
            else:
                self.score += 5
                message = "Correct on your second attempt! You earned 5 points."
            self.feedbackLabel.config(text=message, fg=GREEN)
            self.answerSubmitted = True
            self.submitButton.config(state="disabled")
            self.root.after(850, self.nextQuestion)
        elif self.attempts == 1:
            self.attempts = 2
            self.feedbackLabel.config(text="Not quite. Try the same question one more time.",
                                      fg=RED)
            self.answerEntry.delete(0, tk.END)
            self.answerEntry.focus_set()
        else:
            self.feedbackLabel.config(text=f"The correct answer was {self.correctAnswer}.",
                                      fg=RED)
            self.answerSubmitted = True
            self.submitButton.config(state="disabled")
            self.root.after(1100, self.nextQuestion)

    def nextQuestion(self):
        if self.questionNumber >= 10:
            self.displayResults()
        else:
            self.displayProblem()

    # Required function: displayResults shows the final score and a performance rank.
    def displayResults(self):
        if self.score >= 90:
            grade = "A+"
            comment = "Excellent work!"
        elif self.score >= 80:
            grade = "A"
            comment = "Great result!"
        elif self.score >= 70:
            grade = "B"
            comment = "Well done!"
        elif self.score >= 60:
            grade = "C"
            comment = "Good effort. Keep practising."
        elif self.score >= 50:
            grade = "D"
            comment = "You are making progress."
        else:
            grade = "F"
            comment = "Keep practising and try again."

        self.clear_window()
        self.make_header("Quiz complete")
        card = tk.Frame(self.root, bg=CARD, padx=34, pady=35,
                        highlightbackground="#E1E7F0", highlightthickness=1)
        card.pack(fill="both", expand=True, padx=42, pady=34)
        tk.Label(card, text="YOUR FINAL SCORE", bg=CARD, fg=MUTED,
                 font=("Segoe UI", 10, "bold")).pack()
        tk.Label(card, text=f"{self.score} / 100", bg=CARD, fg=BLUE,
                 font=("Segoe UI", 38, "bold")).pack(pady=(6, 0))
        tk.Label(card, text=f"Rank: {grade}", bg=CARD, fg=DARK,
                 font=("Segoe UI", 19, "bold")).pack(pady=(12, 3))
        tk.Label(card, text=comment, bg=CARD, fg=MUTED, font=FONT).pack()
        ttk.Button(card, text="Play again", style="Primary.TButton",
                   command=self.displayMenu).pack(pady=(28, 8))
        ttk.Button(card, text="Quit", command=self.root.destroy).pack()


def main():
    root = tk.Tk()
    MathsQuizApp(root)
    root.mainloop()


if __name__ == "__main__":
    main()
