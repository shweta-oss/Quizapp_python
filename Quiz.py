import tkinter as tk
from tkinter import messagebox
import csv
import random
import os

class QuizApp:
    def __init__(self, master):
        self.master = master
        self.master.title("Python Quiz App")
        self.master.geometry("500x400")
        self.score = 0
        self.question_index = 0
        self.questions = []
        self.current_question = None
        self.user_name = ""

        self.welcome_screen()

    def welcome_screen(self):
        for widget in self.master.winfo_children():
            widget.destroy()
        
        tk.Label(self.master, text="Welcome to Quiz App", font=("Arial", 18)).pack(pady=20)

        tk.Label(self.master, text="Enter Your Name:").pack()
        self.name_entry = tk.Entry(self.master)
        self.name_entry.pack(pady=10)

        tk.Button(self.master, text="Start Quiz", command=self.start_quiz).pack(pady=10)

    def start_quiz(self):
        self.user_name = self.name_entry.get()
        if self.user_name.strip() == "":
            messagebox.showerror("Error", "Please enter your name.")
            return

        self.load_questions()

    def load_questions(self):
        # Hardcoded for testing; can extend for difficulty/topic
        path = os.path.join("DATAquestions", "math_easy.csv")

        try:
            with open(path, newline='', encoding='utf-8') as f:
                reader = csv.DictReader(f)
                self.questions = list(reader)
                if not self.questions:
                    raise Exception("CSV is empty.")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to load questions:\n{e}")
            return

        random.shuffle(self.questions)
        self.show_question()

    def show_question(self):
        for widget in self.master.winfo_children():
            widget.destroy()

        if self.question_index >= len(self.questions):
            self.end_quiz()
            return

        self.current_question = self.questions[self.question_index]
        q = self.current_question

        tk.Label(self.master, text=f"Q{self.question_index+1}: {q['Question']}", wraplength=400, font=("Arial", 12)).pack(pady=20)

        options = [q['Option1'], q['Option2'], q['Option3'], q['Option4']]
        self.selected_option = tk.StringVar()

        for opt in options:
            tk.Radiobutton(self.master, text=opt, variable=self.selected_option, value=opt).pack(anchor="w")

        tk.Button(self.master, text="Submit", command=self.check_answer).pack(pady=10)

    def check_answer(self):
        selected = self.selected_option.get()
        correct = self.current_question['Answer']

        if selected == "":
            messagebox.showwarning("No Selection", "Please select an option.")
            return

        if selected == correct:
            self.score += 1

        self.question_index += 1
        self.show_question()

    def end_quiz(self):
        for widget in self.master.winfo_children():
            widget.destroy()

        tk.Label(self.master, text=f"Quiz Over!\n{self.user_name}, your score is {self.score}/{len(self.questions)}", font=("Arial", 14)).pack(pady=20)
        self.save_score()

        tk.Button(self.master, text="Exit", command=self.master.quit).pack()

    def save_score(self):
        with open("scoreboard.csv", "a", newline='', encoding='utf-8') as f:
            writer = csv.writer(f)
            writer.writerow([self.user_name, self.score])

# Main Execution
if __name__ == "__main__":
    root = tk.Tk()
    app = QuizApp(root)
    root.mainloop()
