
import tkinter as tk
import random

score = 0
question = 0
attempts = 0
def startQuiz():
    global score, question
    score = 0
    question = 0
    menu.destroy()
    nextQuestion()
def nextQuestion():
    global num1, num2, answer, attempts, question
    if question == 10:
        result.config(text=f"quiz finished! your score: {score}/100")
        return
    question += 1
    attempts = 0
    num1 = random.randint(1, 9)
    num2 = random.randint(1, 9)
    if random.choice(["+", "-"]) == "+":
        answer = num1 + num2
        operation = "+"
    else:
        answer = num1 - num2
        operation = "-"
    questionLabel.config(text=f"{question}. {num1} {operation} {num2} =")
    answerEntry.delete(0, tk.END)
    feedback.config(text="")
def checkAnswer():
    global score, attempts
    try:
        userAnswer = int(answerEntry.get())
    except ValueError:
        feedback.config(text="enter a number")
        return
    if userAnswer == answer:
        if attempts == 0:
            score += 10
        else:
            score += 5
        nextQuestion()
    else:
        attempts += 1
        if attempts == 1:
            feedback.config(text="incorrect")
        else:
            feedback.config(text="incorrect")
            window.after(1000, nextQuestion)
window = tk.Tk()
window.title("Math quiz")
window.geometry("300x250")
menu = tk.Frame(window)
menu.pack()
tk.Label(menu, text="DIFFICULTY LEVEL").pack()
tk.Button(menu, text="Easy", command=startQuiz).pack()
tk.Button(menu, text="Moderate", command=startQuiz).pack()
tk.Button(menu, text="Advanced", command=startQuiz).pack()
questionLabel = tk.Label(window, text="")
questionLabel.pack()
answerEntry = tk.Entry(window)
answerEntry.pack()
tk.Button(window, text="Submit", command=checkAnswer).pack()
feedback = tk.Label(window, text="")
feedback.pack()
result = tk.Label(window, text="")
result.pack()
window.mainloop()