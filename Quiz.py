import tkinter as tk
from tkinter import messagebox
import pandas as pd
import os

class QuizApp:
    def __init__(self, master):
        self.master = master
        self.master.title("QUIZ APP")
        self.master.geometry("500x450")

        self.score = 0
        self.question_index = 0

        self.player_name = ""
        self.create_name_entry_screen()

    def create_name_entry_screen(self):
        self.clear_screen()

        tk.Label(self.master, text="Enter Your Name:", font=('Arial', 14)).pack(pady=20)
        self.name_entry = tk.Entry(self.master, font=('Arial', 12))
        self.name_entry.pack()

        tk.Button(self.master, text="Next", command=self.save_name_and_next).pack(pady=10)

    def save_name_and_next(self):
        name = self.name_entry.get().strip()
        if not name:
            messagebox.showwarning("Warning", "Please enter your name!")
            return
        self.player_name = name
        self.create_topic_difficulty_screen()

    def create_topic_difficulty_screen(self):
        self.clear_screen()

        tk.Label(self.master, text="Choose Topic", font=('Arial', 14)).pack(pady=10)
        self.topic_var = tk.StringVar()
        topics = ['gk', 'math', 'sports']
        for topic in topics:
            tk.Radiobutton(self.master, text=topic.upper(), variable=self.topic_var, value=topic).pack()

        tk.Label(self.master, text="Choose Difficulty", font=('Arial', 14)).pack(pady=10)
        self.difficulty_var = tk.StringVar()
        difficulties = ['easy', 'medium', 'hard']
        for level in difficulties:
            tk.Radiobutton(self.master, text=level.title(), variable=self.difficulty_var, value=level).pack()

        tk.Button(self.master, text="Start Quiz", command=self.load_questions).pack(pady=20)

    def load_questions(self):
        topic = self.topic_var.get()
        difficulty = self.difficulty_var.get()

        if not topic or not difficulty:
            messagebox.showwarning("Warning", "Please select both topic and difficulty!")
            return

        filepath = f"DATAquestions/{topic}_{difficulty}.csv"
        if not os.path.exists(filepath):
            messagebox.showerror("Error", f"No questions found for {topic.upper()} - {difficulty.title()}")
            return

        self.questions_df = pd.read_csv(filepath)
        self.questions = self.questions_df.to_dict('records')
        self.score = 0
        self.question_index = 0

        self.show_question()

    def show_question(self):
        self.clear_screen()

        if self.question_index < len(self.questions):
            q = self.questions[self.question_index]

            if 'question' not in q:
                messagebox.showerror("Error", f"'question' column not found in CSV row: {q}")
                return

            tk.Label(self.master, text=f"Q{self.question_index+1}: {q['question']}", wraplength=450, font=('Arial', 12)).pack(pady=20)
            self.selected_option = tk.StringVar()
            options = ['option1', 'option2', 'option3', 'option4']
            for opt in options:
                tk.Radiobutton(self.master, text=q[opt], variable=self.selected_option, value=q[opt], font=('Arial', 10)).pack(anchor='w', padx=30)

            tk.Button(self.master, text="Submit", command=self.check_answer).pack(pady=20)
        else:
            self.save_score_to_leaderboard()
            self.show_result()

    def check_answer(self):
        selected = self.selected_option.get()
        correct = self.questions[self.question_index]['answer']

        if selected == correct:
            self.score += 1

        self.question_index += 1
        self.show_question()

    def save_score_to_leaderboard(self):
        leaderboard_file = "leaderboard.csv"
        entry = {"name": self.player_name, "score": self.score}
        if os.path.exists(leaderboard_file):
            df = pd.read_csv(leaderboard_file)
            df = pd.concat([df, pd.DataFrame([entry])], ignore_index=True)
        else:
            df = pd.DataFrame([entry])

        df.to_csv(leaderboard_file, index=False)

    def show_result(self):
        self.clear_screen()

        tk.Label(self.master, text=f"Your Score: {self.score} / {len(self.questions)}", font=('Arial', 14)).pack(pady=20)
        tk.Button(self.master, text="Play Again", command=self.create_topic_difficulty_screen).pack(pady=10)
        tk.Button(self.master, text="Exit", command=self.master.quit).pack(pady=10)

    def clear_screen(self):
        for widget in self.master.winfo_children():
            widget.destroy()

if __name__ == "__main__":
    root = tk.Tk()
    app = QuizApp(root)
    root.mainloop()
