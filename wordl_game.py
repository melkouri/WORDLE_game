import tkinter as tk
from tkinter import messagebox
import random

class WordleGame:
    def __init__(self, master):
        self.master = master
        self.master.title("Wordle Game")

        self.secret_word = self.choose_secret_word()
        self.attempts_left = 6

        self.create_widgets()

    def choose_secret_word(self):
        word_list = ["apple", "beach", "charm", "dance", "equip", "flame", "grain", "happy", "inbox", "jumbo"]
        return random.choice(word_list)

    def provide_feedback(self, user_guess):
        feedback = []
        for i in range(len(self.secret_word)):
            if user_guess[i] == self.secret_word[i]:
                feedback.append('green')
            elif user_guess[i] in self.secret_word:
                feedback.append('orange')
            else:
                feedback.append('grey')
        return feedback

    def check_win(self, feedback):
        return feedback.count('green') == 5

# To do: upadte colors depending on feedback!!
    def update_alphabet_labels(self, used_letters):
        for letter, label in zip("abcdefghijklmnopqrstuvwxyz", self.alphabet_labels):
            if letter in used_letters:
                label.config(bg='grey')
            else:
                label.config(bg='white')
# To do: add letters in feedback_labels!!
    def update_feedback_labels(self, attempt, feedback):
        for i, color in enumerate(feedback):
            self.feedback_labels[attempt][i].config(bg=color)

    def make_guess(self, attempt):
        user_guess = "".join(self.guess_entries[attempt][i].get() for i in range(5)).lower()

        if len(user_guess) != 5 or not user_guess.isalpha():
            messagebox.showwarning("Invalid Input", "Please enter a valid 5-letter word.")
            return

        feedback = self.provide_feedback(user_guess)
        self.update_feedback_labels(attempt, feedback)
# What does it do??? 
        self.update_alphabet_labels(set(user_guess) | set([letter for letter, feedback_color in zip("abcdefghijklmnopqrstuvwxyz", feedback) if feedback_color == 'grey']))

        if self.check_win(feedback):
            messagebox.showinfo("Congratulations!", f"You guessed the word: {self.secret_word}")
            self.master.destroy()
        else:
            self.attempts_left -= 1

            if self.attempts_left == 0:
                messagebox.showinfo("Game Over", f"Sorry, you ran out of attempts. The word was: {self.secret_word}")
                self.master.destroy()

    def create_widgets(self):
        # Create labels for alphabet
        self.alphabet_labels = []
        for i, letter in enumerate("abcdefghijklmnopqrstuvwxyz"):
            label = tk.Label(self.master, width=2, height=1, text=letter, relief=tk.SOLID, borderwidth=1)
            label.grid(row=0, column=i, padx=5)
            self.alphabet_labels.append(label)

        # Create 6 rows for attempts
# To do: Keep only 1 guess_entry
        self.guess_entries = []
        self.feedback_labels = []
        for attempt in range(6):
            # Create 5 text boxes for input
            guess_row = []
            for i in range(5):
                entry = tk.Entry(self.master, width=3, font=('Helvetica', 14), justify='center')
                entry.grid(row=attempt + 1, column=i, padx=5, pady=5)
                guess_row.append(entry)
            self.guess_entries.append(guess_row)

            # Create labels for feedback
            feedback_row = []
            for i in range(5):
                label = tk.Label(self.master, width=3, height=2, bg='white', relief=tk.SOLID, borderwidth=1)
                label.grid(row=attempt + 7, column=i, padx=5)
                feedback_row.append(label)
            self.feedback_labels.append(feedback_row)

        # Create Submit Button
        submit_button = tk.Button(self.master, text="Submit Guess", command=lambda: self.make_guess(6 - self.attempts_left))
        submit_button.grid(row=13, columnspan=5, pady=10)

def main():
    root = tk.Tk()
    game = WordleGame(root)
    root.mainloop()

if __name__ == "__main__":
    main()
