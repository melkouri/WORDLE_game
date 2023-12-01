import tkinter as tk
from tkinter import messagebox
import random

class WordleGame:
    def __init__(self, master):
        self.master = master
        self.master.title("Wordle Game")

        # Set the window size to the whole screen
        width = self.master.winfo_screenwidth()
        height = self.master.winfo_screenheight()
        self.master.geometry(f"{width}x{height}")

        # Allow the window to be resizable both horizontally and vertically
        self.master.resizable(True, True)

        # Set background color
        self.master.configure(bg='#cdd7f1')

        self.secret_word = self.choose_secret_word()
        self.attempts_left = 6

        self.create_widgets()

    def choose_secret_word(self):
        word_list = ["apple", "beach", "charm", "dance", "equip", "flame", "grain", "happy", "inbox", "jumbo"]
        return random.choice(word_list)

    def provide_feedback(self, user_guess):
        feedback = []
        for i in range(len(self.secret_word)):
            letter = user_guess[i]
            if letter == self.secret_word[i]:
                feedback.append((letter, 'green'))
            elif letter in self.secret_word:
                feedback.append((letter, 'orange'))
            else:
                feedback.append((letter, 'grey'))
        return feedback

    def check_win(self, feedback):
        green_count = sum(1 for letter, color in feedback if color == 'green')
        return green_count == 5

    def update_alphabet_labels(self, feedback_colors):
        for letter, label in zip("abcdefghijklmnopqrstuvwxyz", self.alphabet_labels):
            matching_colors = [color for l, color in feedback_colors if l == letter]
            if matching_colors:
                prioritized_colors = sorted(matching_colors, key=lambda c: c != 'green')
                label.config(bg=prioritized_colors[0])

    def update_feedback_labels(self, attempt, feedback):
        for i, (letter, color) in enumerate(feedback):
            # Display feedback labels in front of guess entries in the same row
            self.feedback_labels[attempt][i].config(bg=color)
            self.feedback_labels[attempt][i].config(bg=color, text=letter)

    def clear_guess_entry(self):
        for entry in self.guess_entry:
            entry.delete(0, 'end')

    def make_guess(self, attempt):
        user_guess = "".join(entry.get() for entry in self.guess_entry).lower()

        self.clear_guess_entry()

        if len(user_guess) != 5 or not user_guess.isalpha():
            messagebox.showwarning("Invalid Input", "Please enter a valid 5-letter word.")
            return

        feedback = self.provide_feedback(user_guess)
        self.update_feedback_labels(attempt, feedback)
        self.update_alphabet_labels(feedback)

        if self.check_win(feedback):
            messagebox.showinfo("Congratulations!", f"You guessed the word: {self.secret_word}")
            self.master.destroy()
        else:
            self.attempts_left -= 1

            if self.attempts_left == 0:
                messagebox.showinfo("Game Over", f"Sorry, you ran out of attempts. The word was: {self.secret_word}")
                self.master.destroy()

    def create_widgets(self):
        self.feedback_labels = []

        self.guess_entry = [tk.Entry(self.master, width=4, font=('Helvetica', 18), justify='center') for _ in range(5)]
        for i, entry in enumerate(self.guess_entry):
            entry.grid(row=3, column=i + 1, padx=5, pady=5)

        for attempt in range(6):
            feedback_row = []
            for i in range(5):
                feedback_label = tk.Label(self.master, width=3, height=2, bg='white', relief=tk.SOLID, borderwidth=1)
                feedback_label.grid(row=attempt + 4, column=i+1, padx=5)
                feedback_row.append(feedback_label)

            
            self.feedback_labels.append(feedback_row)

        # Create labels for alphabet in three rows at the bottom
        self.alphabet_labels = []
        alphabet_rows = ["abcdefghijklm", "nopqrstuvwxyz", ""]
        for row_index, row in enumerate(alphabet_rows):
            for col_index, letter in enumerate(row):
                label = tk.Label(self.master, width=3, height=2, text=letter, relief=tk.SOLID, borderwidth=1, font=('Helvetica', 18))
                label.grid(row=row_index + 11, column=col_index + 1, padx=5, pady=5)
                self.alphabet_labels.append(label)

        # Create Submit Button
        submit_button = tk.Button(self.master, text="Submit Guess", command=lambda: self.make_guess(6 - self.attempts_left))
        submit_button.grid(row=14, column=6, columnspan=3, pady=10)

def main():
    root = tk.Tk()
    game = WordleGame(root)
    root.mainloop()

if __name__ == "__main__":
    main()


