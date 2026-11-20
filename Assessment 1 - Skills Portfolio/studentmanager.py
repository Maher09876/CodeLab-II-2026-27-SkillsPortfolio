
import tkinter as tk
from tkinter import messagebox

students = []


def loadStudents():
    try:
        file = open("studentMarks.txt", "r")

        file.readline()

        for line in file:
            data = line.strip().split(",")

            if len(data) == 6:
                student = {
                    "code": data[0],
                    "name": data[1],
                    "mark1": int(data[2]),
                    "mark2": int(data[3]),
                    "mark3": int(data[4]),
                    "exam": int(data[5])
                }

                students.append(student)

        file.close()

    except FileNotFoundError:
        messagebox.showerror("Error", "studentMarks.txt not found.")


def getCoursework(student):
    return student["mark1"] + student["mark2"] + student["mark3"]


def getTotal(student):
    return getCoursework(student) + student["exam"]


def getPercentage(student):
    return getTotal(student) / 160 * 100


def getGrade(percentage):
    if percentage >= 70:
        return "A"
    elif percentage >= 60:
        return "B"
    elif percentage >= 50:
        return "C"
    elif percentage >= 40:
        return "D"
    else:
        return "F"


def displayRecord(student):
    coursework = getCoursework(student)
    percentage = getPercentage(student)
    grade = getGrade(percentage)

    return (
        f"Name: {student['name']}\n"
        f"Student Number: {student['code']}\n"
        f"Coursework: {coursework}/60\n"
        f"Exam: {student['exam']}/100\n"
        f"Total: {getTotal(student)}/160\n"
        f"Percentage: {percentage:.2f}%\n"
        f"Grade: {grade}\n"
    )


def showText(text):
    output.delete("1.0", tk.END)
    output.insert(tk.END, text)


def viewAll():
    if len(students) == 0:
        showText("No student records found.")
        return

    result = ""
    totalPercentage = 0

    for student in students:
        result += displayRecord(student)
        result += "\n-------------------------\n"

        totalPercentage += getPercentage(student)

    average = totalPercentage / len(students)

    result += f"\nNumber of students: {len(students)}"
    result += f"\nClass average: {average:.2f}%"

    showText(result)


def viewIndividual():
    search = searchEntry.get().strip().lower()

    if search == "":
        showText("Enter a student name or number.")
        return

    for student in students:
        if search == student["code"] or search in student["name"].lower():
            showText(displayRecord(student))
            return

    showText("Student not found.")


def highestStudent():
    if len(students) == 0:
        showText("No student records found.")
        return

    highest = students[0]

    for student in students:
        if getTotal(student) > getTotal(highest):
            highest = student

    showText("Student with highest score:\n\n" + displayRecord(highest))


def lowestStudent():
    if len(students) == 0:
        showText("No student records found.")
        return

    lowest = students[0]

    for student in students:
        if getTotal(student) < getTotal(lowest):
            lowest = student

    showText("Student with lowest score:\n\n" + displayRecord(lowest))


# Main window
window = tk.Tk()
window.title("Student Manager")
window.geometry("600x550")


tk.Label(window, text="STUDENT MANAGER",
         font=("Arial", 16)).pack(pady=10)

tk.Button(window, text="1. View all student records",
          command=viewAll).pack(pady=5)

tk.Label(window, text="Enter student name or number:").pack()

searchEntry = tk.Entry(window)
searchEntry.pack(pady=5)

tk.Button(window, text="2. View individual student record",
          command=viewIndividual).pack(pady=5)

tk.Button(window, text="3. Show student with highest score",
          command=highestStudent).pack(pady=5)

tk.Button(window, text="4. Show student with lowest score",
          command=lowestStudent).pack(pady=5)


output = tk.Text(window, width=65, height=18)
output.pack(pady=10)


loadStudents()

window.mainloop()