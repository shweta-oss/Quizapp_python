import tkinter as tk
from tkinter import messagebox
import csv
import os
import random

class QuizApp:
    def __init__(self, master):
        self.master = master
        self.master.title("Python Quiz App")
        self.username = ""
        self.topic = ""
        self.difficulty = ""
        self.score = 0
        self.qn = 0
        self.questions = []

        self.create_intro_screen()

    def create_intro_screen(self):
        self.clear_window()

        tk.Label(self.master, text="Enter Your Name:").pack(pady=10)
        self.name_entry = tk.Entry(self.master)
        self.name_entry.pack()

        tk.Button(self.master, text="Next", command=self.select_topic).pack(pady=10)

    def select_topic(self):
        self.username = self.name_entry.get().strip()
        if not self.username:
            messagebox.showerror("Error", "Please enter your name.")
            return

        self.clear_window()

        tk.Label(self.master, text="Select Topic").pack(pady=10)
        self.topic_var = tk.StringVar()
        topics = ["math", "gk", "sports"]
        for topic in topics:
            tk.Radiobutton(self.master, text=topic.capitalize(), variable=self.topic_var, value=topic).pack()

        tk.Button(self.master, text="Next", command=self.select_difficulty).pack(pady=10)

    def select_difficulty(self):
        self.topic = self.topic_var.get()
        if not self.topic:
            messagebox.showerror("Error", "Please select a topic.")
            return

        self.clear_window()

        tk.Label(self.master, text="Select Difficulty Level").pack(pady=10)
        self.diff_var = tk.StringVar()
        levels = ["easy", "medium", "hard"]
        for level in levels:
            tk.Radiobutton(self.master, text=level.capitalize(), variable=self.diff_var, value=level).pack()

        tk.Button(self.master, text="Start Quiz", command=self.load_questions).pack(pady=10)

    def load_questions(self):
        self.difficulty = self.diff_var.get()
        if not self.difficulty:
            messagebox.showerror("Error", "Please select a difficulty level.")
            return

        file_path = f"DATAquestions/{self.topic}_{self.difficulty}.csv"
        try:
            with open(file_path, newline='', encoding='utf-8') as file:
                reader = csv.DictReader(file)
                self.questions = list(reader)
                random.shuffle(self.questions)
        except FileNotFoundError:
            messagebox.showerror("Error", f"File not found: {file_path}")
            return

        self.qn = 0
        self.score = 0
        self.display_question()

    def display_question(self):
        self.clear_window()
        if self.qn >= len(self.questions):
            self.show_result()
            return

        current = self.questions[self.qn]

        tk.Label(self.master, text=f"Q{self.qn + 1}: {current['Question']}", font=("Arial", 14)).pack(pady=10)

        self.answer_var = tk.StringVar()

        for i in range(1, 5):
            option = current[f'Option{i}']
            tk.Radiobutton(self.master, text=option, variable=self.answer_var, value=option).pack(anchor="w")

        tk.Button(self.master, text="Submit", command=self.check_answer).pack(pady=10)

    def check_answer(self):
        selected = self.answer_var.get()
        if not selected:
            messagebox.showwarning("Warning", "Please select an answer.")
            return

        correct = self.questions[self.qn]['Answer']
        if selected == correct:
            self.score += 1

        self.qn += 1
        self.display_question()

    def show_result(self):
        self.clear_window()
        tk.Label(self.master, text=f"{self.username}, your score: {self.score}/{len(self.questions)}", font=("Arial", 14)).pack(pady=10)

        self.save_score()

        tk.Button(self.master, text="Play Again", command=self.create_intro_screen).pack(pady=10)
        tk.Button(self.master, text="Exit", command=self.master.quit).pack(pady=10)

    def save_score(self):
        file_exists = os.path.isfile("scoreboard.csv")
        with open("scoreboard.csv", "a", newline='', encoding='utf-8') as file:
            writer = csv.writer(file)
            if not file_exists:
                writer.writerow(["Name", "Topic", "Difficulty", "Score"])
            writer.writerow([self.username, self.topic, self.difficulty, self.score])

    def clear_window(self):
        for widget in self.master.winfo_children():
            widget.destroy()

if __name__ == "__main__":
    root = tk.Tk()
    root.geometry("400x400")
    app = QuizApp(root)
    root.mainloop()
