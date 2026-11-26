import csv
from pathlib import Path
import tkinter as tk
from tkinter import ttk, messagebox


BG = "#F3F6FA"
CARD = "#FFFFFF"
DARK = "#172B4D"
MUTED = "#667085"
BLUE = "#315EFB"
RED = "#C83D4D"
FONT = ("Segoe UI", 9)


class StudentManagerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Student Manager | Programming Skills Portfolio")
        self.root.geometry("1120x700")
        self.root.minsize(900, 600)
        self.root.configure(bg=BG)

        self.dataFile = Path(__file__).resolve().parent / "resources" / "studentMarks.txt"
        self.students = []
        self.configure_style()
        self.loadStudents()
        self.build_interface()
        self.viewAllRecords()

    def configure_style(self):
        style = ttk.Style()
        style.theme_use("clam")
        style.configure("TButton", font=("Segoe UI", 9, "bold"), padding=(9, 7))
        style.configure("Primary.TButton", background=BLUE, foreground="white")
        style.map("Primary.TButton", background=[("active", "#2449D8")])
        style.configure("Treeview", font=("Segoe UI", 9), rowheight=29,
                        background="white", fieldbackground="white")
        style.configure("Treeview.Heading", font=("Segoe UI", 9, "bold"),
                        background="#E9EEF7", foreground=DARK, padding=7)
        style.map("Treeview", background=[("selected", "#DCE6FF")],
                  foreground=[("selected", DARK)])
        style.configure("TEntry", padding=7)

    # AI-assisted section: read the count on line one and student rows below it.
    def loadStudents(self):
        self.students = []
        try:
            with self.dataFile.open("r", encoding="utf-8", newline="") as file:
                first_line = file.readline().strip()
                int(first_line)  # Check that the first line contains the record count.
                reader = csv.reader(file)
                for line_number, row in enumerate(reader, start=2):
                    if not row:
                        continue
                    if len(row) != 6:
                        raise ValueError(f"Line {line_number} should contain 6 values.")
                    code, name, mark1, mark2, mark3, exam = row
                    student = {
                        "code": code.strip(),
                        "name": name.strip(),
                        "course1": int(mark1),
                        "course2": int(mark2),
                        "course3": int(mark3),
                        "exam": int(exam),
                    }
                    self.validateStudent(student, existingCode=None)
                    self.students.append(student)
        except FileNotFoundError:
            messagebox.showerror(
                "Student file not found",
                "The file resources/studentMarks.txt is missing. Add the resource file and restart the app."
            )
        except (ValueError, OSError) as error:
            messagebox.showerror("Could not read student file", str(error))
            self.students = []

    # Calculate marks and grades in one place so every screen uses the same rules.
    def getResults(self, student):
        coursework = student["course1"] + student["course2"] + student["course3"]
        total = coursework + student["exam"]
        percentage = (total / 160) * 100
        if percentage >= 70:
            grade = "A"
        elif percentage >= 60:
            grade = "B"
        elif percentage >= 50:
            grade = "C"
        elif percentage >= 40:
            grade = "D"
        else:
            grade = "F"
        return coursework, total, percentage, grade

    # Check the student code and each mark before adding or changing a record.
    def validateStudent(self, student, existingCode=None):
        code = str(student["code"]).strip()
        name = str(student["name"]).strip()
        if not code.isdigit() or not 1000 <= int(code) <= 9999:
            raise ValueError("Student number must be a four-digit number (1000 to 9999).")
        if not name:
            raise ValueError("Please enter the student's name.")
        if any(other["code"] == code and other["code"] != existingCode
               for other in self.students):
            raise ValueError("That student number is already in use.")
        for key in ("course1", "course2", "course3"):
            if not isinstance(student[key], int) or not 0 <= student[key] <= 20:
                raise ValueError("Each coursework mark must be between 0 and 20.")
        if not isinstance(student["exam"], int) or not 0 <= student["exam"] <= 100:
            raise ValueError("The examination mark must be between 0 and 100.")

    # Save the updated count and all records back to the text file.
    def saveStudents(self):
        try:
            self.dataFile.parent.mkdir(parents=True, exist_ok=True)
            with self.dataFile.open("w", encoding="utf-8", newline="") as file:
                file.write(f"{len(self.students)}\n")
                writer = csv.writer(file)
                for student in self.students:
                    writer.writerow([
                        student["code"], student["name"], student["course1"],
                        student["course2"], student["course3"], student["exam"]
                    ])
            return True
        except OSError as error:
            messagebox.showerror("Save error", f"The student file could not be saved:\n{error}")
            return False

    def build_interface(self):
        header = tk.Frame(self.root, bg=DARK, padx=24, pady=18)
        header.pack(fill="x")
        tk.Label(header, text="STUDENT MANAGER", bg=DARK, fg="white",
                 font=("Segoe UI", 18, "bold")).pack(anchor="w")
        tk.Label(header, text="View, compare and maintain student assessment records.",
                 bg=DARK, fg="#D6DDF0", font=("Segoe UI", 10)).pack(anchor="w", pady=(4, 0))

        body = tk.Frame(self.root, bg=BG, padx=22, pady=18)
        body.pack(fill="both", expand=True)

        toolbar = tk.Frame(body, bg=CARD, padx=12, pady=12,
                           highlightbackground="#E1E7F0", highlightthickness=1)
        toolbar.pack(fill="x", pady=(0, 12))
        tk.Label(toolbar, text="Find by student number or name", bg=CARD, fg=MUTED,
                 font=FONT).grid(row=0, column=0, sticky="w", padx=(0, 8))
        self.searchEntry = ttk.Entry(toolbar, width=25)
        self.searchEntry.grid(row=0, column=1, padx=5)
        self.searchEntry.bind("<Return>", lambda _event: self.viewIndividualRecord())
        ttk.Button(toolbar, text="View individual", command=self.viewIndividualRecord).grid(
            row=0, column=2, padx=5
        )
        ttk.Button(toolbar, text="View all", style="Primary.TButton",
                   command=self.viewAllRecords).grid(row=0, column=3, padx=5)

        actions = tk.Frame(body, bg=BG)
        actions.pack(fill="x", pady=(0, 12))
        ttk.Button(actions, text="Highest total", command=self.showHighest).pack(side="left", padx=(0, 6))
        ttk.Button(actions, text="Lowest total", command=self.showLowest).pack(side="left", padx=6)
        self.sortOrder = tk.StringVar(value="Descending")
        self.sortBox = ttk.Combobox(actions, textvariable=self.sortOrder,
                                    values=["Ascending", "Descending"],
                                    state="readonly", width=13)
        self.sortBox.pack(side="left", padx=(14, 5))
        ttk.Button(actions, text="Sort records", command=self.sortRecords).pack(side="left", padx=5)
        ttk.Button(actions, text="Add student", style="Primary.TButton",
                   command=self.addStudent).pack(side="right", padx=(6, 0))
        ttk.Button(actions, text="Update selected", command=self.updateStudent).pack(side="right", padx=6)
        ttk.Button(actions, text="Delete selected", command=self.deleteStudent).pack(side="right", padx=6)

        table_card = tk.Frame(body, bg=CARD, padx=10, pady=10,
                              highlightbackground="#E1E7F0", highlightthickness=1)
        table_card.pack(fill="both", expand=True)
        columns = ("name", "code", "coursework", "exam", "total", "percentage", "grade")
        self.tree = ttk.Treeview(table_card, columns=columns, show="headings", height=13)
        headings = {
            "name": ("Student name", 220),
            "code": ("Student number", 115),
            "coursework": ("Coursework / 60", 125),
            "exam": ("Exam / 100", 105),
            "total": ("Total / 160", 105),
            "percentage": ("Overall %", 105),
            "grade": ("Grade", 70),
        }
        for column, (heading, width) in headings.items():
            self.tree.heading(column, text=heading)
            self.tree.column(column, width=width, anchor="center" if column != "name" else "w")
        scrollbar = ttk.Scrollbar(table_card, orient="vertical", command=self.tree.yview)
        self.tree.configure(yscrollcommand=scrollbar.set)
        self.tree.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

        footer = tk.Frame(body, bg=BG)
        footer.pack(fill="x", pady=(10, 0))
        self.summaryLabel = tk.Label(footer, text="", bg=BG, fg=DARK,
                                     font=("Segoe UI", 9, "bold"))
        self.summaryLabel.pack(anchor="w")
        self.statusLabel = tk.Label(footer, text="Select a row to update or delete a student.",
                                    bg=BG, fg=MUTED, font=FONT)
        self.statusLabel.pack(anchor="w", pady=(4, 0))

    def showRecords(self, records, status="Showing student records."):
        for item in self.tree.get_children():
            self.tree.delete(item)
        for student in records:
            coursework, total, percentage, grade = self.getResults(student)
            self.tree.insert("", "end", iid=student["code"], values=(
                student["name"], student["code"], coursework, student["exam"],
                total, f"{percentage:.1f}%", grade
            ))
        if self.students:
            average = sum(self.getResults(student)[2] for student in self.students) / len(self.students)
        else:
            average = 0
        self.summaryLabel.config(
            text=f"Class size: {len(self.students)} students     |     Class average: {average:.1f}%"
        )
        self.statusLabel.config(text=status)

    # Menu item 1: display all student records and the class summary.
    def viewAllRecords(self):
        self.showRecords(self.students, "All student records are displayed.")

    # Menu item 2: search by exact student number or by student name.
    def viewIndividualRecord(self):
        query = self.searchEntry.get().strip()
        if not query:
            messagebox.showinfo("Find a student", "Enter a student number or name first.")
            return
        matches = [student for student in self.students
                   if student["code"] == query or student["name"].casefold() == query.casefold()]
        if not matches:
            matches = [student for student in self.students
                       if query.casefold() in student["name"].casefold()]
        if not matches:
            messagebox.showinfo("No match", "No student matched that number or name.")
            return
        self.showRecords(matches, f"Showing {len(matches)} matching student record(s).")
        if len(matches) == 1:
            self.tree.selection_set(matches[0]["code"])
            self.tree.focus(matches[0]["code"])

    # Menu item 3: identify the student with the highest total mark.
    def showHighest(self):
        if not self.students:
            messagebox.showinfo("No records", "There are no student records to compare.")
            return
        student = max(self.students, key=lambda item: self.getResults(item)[1])
        self.showRecords([student], "Student with the highest overall mark.")
        self.tree.selection_set(student["code"])

    # Menu item 4: identify the student with the lowest total mark.
    def showLowest(self):
        if not self.students:
            messagebox.showinfo("No records", "There are no student records to compare.")
            return
        student = min(self.students, key=lambda item: self.getResults(item)[1])
        self.showRecords([student], "Student with the lowest overall mark.")
        self.tree.selection_set(student["code"])

    # Extension item 5: sort the displayed student records by total mark.
    def sortRecords(self):
        reverse = self.sortOrder.get() == "Descending"
        sorted_students = sorted(
            self.students, key=lambda item: self.getResults(item)[1], reverse=reverse
        )
        direction = self.sortOrder.get().lower()
        self.showRecords(sorted_students, f"Records sorted in {direction} order by total mark.")

    def getSelectedStudent(self):
        selection = self.tree.selection()
        if not selection:
            messagebox.showinfo("Select a student", "Select a student row in the table first.")
            return None
        selected_code = selection[0]
        return next((student for student in self.students if student["code"] == selected_code), None)

    # Add and update use the same form so the required fields are consistent.
    def openStudentForm(self, title, existingStudent=None):
        window = tk.Toplevel(self.root)
        window.title(title)
        window.configure(bg=CARD)
        window.resizable(False, False)
        window.transient(self.root)
        window.grab_set()

        values = existingStudent or {
            "code": "", "name": "", "course1": 0, "course2": 0,
            "course3": 0, "exam": 0
        }
        fields = [
            ("Student number", "code"),
            ("Student name", "name"),
            ("Coursework mark 1 (0-20)", "course1"),
            ("Coursework mark 2 (0-20)", "course2"),
            ("Coursework mark 3 (0-20)", "course3"),
            ("Examination mark (0-100)", "exam"),
        ]
        entries = {}
        frame = tk.Frame(window, bg=CARD, padx=24, pady=20)
        frame.pack()
        for row, (label, key) in enumerate(fields):
            tk.Label(frame, text=label, bg=CARD, fg=DARK,
                     font=FONT).grid(row=row, column=0, sticky="w", pady=6, padx=(0, 16))
            entry = ttk.Entry(frame, width=27)
            entry.grid(row=row, column=1, pady=6)
            entry.insert(0, str(values[key]))
            entries[key] = entry

        def save_record():
            try:
                new_student = {
                    "code": entries["code"].get().strip(),
                    "name": entries["name"].get().strip(),
                    "course1": int(entries["course1"].get()),
                    "course2": int(entries["course2"].get()),
                    "course3": int(entries["course3"].get()),
                    "exam": int(entries["exam"].get()),
                }
                old_code = existingStudent["code"] if existingStudent else None
                self.validateStudent(new_student, existingCode=old_code)
                if existingStudent:
                    index = self.students.index(existingStudent)
                    self.students[index] = new_student
                else:
                    self.students.append(new_student)
                if self.saveStudents():
                    window.destroy()
                    self.viewAllRecords()
                    self.statusLabel.config(text="Student record saved to studentMarks.txt.")
                else:
                    # Restore the in-memory list if the file could not be saved.
                    if existingStudent:
                        self.students[index] = existingStudent
                    else:
                        self.students.remove(new_student)
            except ValueError as error:
                messagebox.showerror("Check the entered information", str(error), parent=window)

        ttk.Button(frame, text="Save record", style="Primary.TButton",
                   command=save_record).grid(row=len(fields), column=1, sticky="e", pady=(14, 0))

    # Extension item 6: add a new student record.
    def addStudent(self):
        self.openStudentForm("Add student record")

    # Extension item 7: remove the currently selected record from the file.
    def deleteStudent(self):
        student = self.getSelectedStudent()
        if student is None:
            return
        confirm = messagebox.askyesno(
            "Delete student",
            f"Delete {student['name']} ({student['code']}) from the records?"
        )
        if confirm:
            self.students.remove(student)
            if self.saveStudents():
                self.viewAllRecords()
                self.statusLabel.config(text="Student record deleted from studentMarks.txt.")
            else:
                self.students.append(student)

    # Extension item 8: update the currently selected record.
    def updateStudent(self):
        student = self.getSelectedStudent()
        if student is not None:
            self.openStudentForm("Update student record", student)


def main():
    root = tk.Tk()
    StudentManagerApp(root)
    root.mainloop()


if __name__ == "__main__":
    main()
