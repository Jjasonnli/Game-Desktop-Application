import random
import tkinter as tk
from tkinter import messagebox

class WordleGame:
    def __init__(self, master):
        self.master = master
        self.master.title("Wordle")

        # Set up the initial game state
        self.word = choose_word()
        self.num_guesses = 6
        self.correct_word = tk.StringVar()
        self.correct_word.set(" ".join(["_" for _ in self.word]))

        # Create the widgets
        self.create_widgets()

        # Start the game timer
        self.timer_running = False
        self.time_limit = 180
        self.remaining_time = self.time_limit
        self.timer_label = tk.Label(
            self.master,
            text=f"Time left: {self.remaining_time}s",
            font=("Arial", 16),
            fg="#191970",
            bg="#f0f8ff"
        )
        self.timer_label.pack()
        self.start_timer()

        # Create the score label
        self.score = 0
        self.score_label = tk.Label(
            self.master,
            text=f"Score: {self.score}",
            font=("Arial", 16),
            fg="#191970",
            bg="#f0f8ff"
        )
        self.score_label.pack()

        # Create the history table
        self.history_table = []
        self.create_history_table()

    def create_widgets(self):
        # Create the title label
        self.title_label = tk.Label(
            self.master,
            text="Wordle",
            font=("Comic Sans MS", 28),
            bg="#78c5ef",
            fg="white",
            padx=20,
            pady=20,
        )
        self.title_label.pack(fill="x")

        # Create the word label
        self.word_label = tk.Label(
            self.master,
            text=" ".join(["_" for _ in self.word]),
            font=("Arial", 24),
            fg="#4b0082",
            pady=20,
            bg="#f0f8ff"
        )
        self.word_label.pack()

        # Create the guesses left label
        self.guess_label = tk.Label(
            self.master,
            text=f"Guesses left: {self.num_guesses}",
            font=("Arial", 16),
            fg="#191970",
            bg="#f0f8ff"
        )
        self.guess_label.pack()

        # Create the guess entry widget
        self.guess_entry = tk.Entry(
            self.master,
            width=30,
            font=("Arial", 14),
            fg="#191970",
            bg="#f0f8ff",
        )
        self.guess_entry.pack(pady=10)

        # Create the guess button widget
        self.guess_button = tk.Button(
            self.master,
            text="Guess",
            font=("Arial", 14),
            fg="white",
            bg="#ffa500",
            command=self.check_guess,
        )
        self.guess_button.pack(pady=10)

    def create_history_table(self):
        # Create the table frame
        self.table_frame = tk.Frame(self.master, bg="#f0f8ff")
        self.table_frame.pack()

        # Create the table headers
        headers = ["Guess", "Correct Position", "Wrong Word", "Wrong Position"]
        for i in range(len(headers)):
            header_label = tk.Label(
                self.table_frame,
                text=headers[i],
                font=("Arial", 12, "bold"),
                fg="#4b0082",
                bg="#f0f8ff",
                width=12,
                padx=10,
                pady=5,
                relief=tk.RAISED
            )
            header_label.grid(row=0, column=i)

        # Create the table cells
        for row in range(1, self.num_guesses + 1):
            guess_cell = tk.Label(
                self.table_frame,
                text="",
                font=("Arial", 12),
                fg="#4b0082",
                bg="#f0f8ff",
                width=12,
                padx=10,
                pady=5,
                relief=tk.SOLID
            )
            guess_cell.grid(row=row, column=0)

            correct_cell = tk.Label(
                self.table_frame,
                text="",
                font=("Arial", 12),
                fg="#4b0082",
                bg="#f0f8ff",
                width=12,
                padx=10,
                pady=5,
                relief=tk.SOLID
            )
            correct_cell.grid(row=row, column=1)

            wrong_cell = tk.Label(
                self.table_frame,
                text="",
                font=("Arial", 12),
                fg="#4b0082",
                bg="#f0f8ff",
                width=12,
                padx=10,
                pady=5,
                relief=tk.SOLID
            )
            wrong_cell.grid(row=row, column=2)

            missing_cell = tk.Label(
                self.table_frame,
                text="",
                font=("Arial", 12),
                fg="#4b0082",
                bg="#f0f8ff",
                width=12,
                padx=10,
                pady=5,
                relief=tk.SOLID
            )
            missing_cell.grid(row=row, column=3)

            self.history_table.append([guess_cell, correct_cell, wrong_cell, missing_cell])

    def start_timer(self):
        if not self.timer_running:
            self.timer_running = True
            self.update_timer()

    def update_timer(self):
        if self.remaining_time > 0:
            self.remaining_time -= 1
            self.timer_label.config(text=f"Time left: {self.remaining_time}s")
            self.master.after(1000, self.update_timer)
        else:
            self.timer_label.config(text="Time's up!")
            self.guess_entry.config(state="disabled")
            self.guess_button.config(state="disabled")

    def check_guess(self):
        guess = self.guess_entry.get().lower()
        if len(guess) != 5 or not guess.isalpha():
            messagebox.showerror("Error", "Your guess should be a word containing only alphabets.")
        else:
            self.num_guesses -= 1
            correct_pos, correct_letter, wrong_pos = check_guess(guess, self.word)
            if correct_pos == 5:
                self.word_label.config(text=self.word, fg="green")
                self.guess_label.config(text=f"You won!", fg="green")
                self.guess_button.config(state="disabled", bg="grey", fg="white")
                self.update_score()
            else:
                # modify the word to show only correctly guessed letters in the correct positions
                new_word = ""
                for i in range(5):
                    if guess[i] == self.word[i]:
                        new_word += self.word[i] + " "
                    elif guess[i] in self.word:
                        new_word += "_ "
                    else:
                        new_word += "_ "
                self.word_label.config(text=new_word.strip())
                hint_text = ""
                if correct_letter:
                    hint_text += f"{correct_letter} is in the word, but in the wrong position. "
                if wrong_pos:
                    hint_text += f"{wrong_pos} is not in the word. "
                self.guess_label.config(text=f"Guesses left: {self.num_guesses}")
                self.update_history_table(guess, correct_pos, correct_letter, wrong_pos)
                self.guess_entry.delete(0, tk.END)
                if self.num_guesses == 0:
                    self.word_label.config(text=self.word, fg="red")
                    self.guess_label.config(text="You lost!", fg="red")
                    self.guess_button.config(state="disabled", bg="grey", fg="white")

    def update_history_table(self, guess, correct_pos, correct_letter, wrong_pos):
        # Find the first empty row in the table
        empty_row = None
        for i in range(len(self.history_table)):
            if self.history_table[i][0].cget("text") == "":
                empty_row = i
                break

        if empty_row is not None:
            # Update the guess cell
            self.history_table[empty_row][0].config(text=guess)

            # Update the correct cell
            correct_text = ""
            for i in range(5):
                if guess[i] == self.word[i]:
                    correct_text += guess[i]
                elif guess[i] in self.word:
                    correct_text += "-"
                else:
                    correct_text += " "
            self.history_table[empty_row][1].config(text=correct_text)

            # Update the wrong cell
            wrong_text = ""
            for letter in wrong_pos:
                wrong_text += letter + " "
            self.history_table[empty_row][2].config(text=wrong_text)

            # Update the missing cell
            missing_text = ""
            for letter in correct_letter:
                missing_text += letter + " "
            self.history_table[empty_row][3].config(text=missing_text)

    def update_score(self):
        self.score += 1
        self.score_label.config(text=f"Score: {self.score}")

def choose_word():
    words = [
    "apple", "beach", "chair", "dance", "eagle", "fairy", "ghost", "house", "igloo", "jelly",
    "kayak", "lemon", "mango", "noise", "olive", "peach", "quiet", "river", "snake", "table",
    "umbra", "vivid", "wagon", "zebra", "acorn", "bliss", "coral", "diary", "ember", "frost",
    "grape", "hound", "ivory", "jumbo", "koala", "lily", "medal", "nylon", "orbit", "pixel",
    "quirk", "roost", "swirl", "tidal", "unity", "velvet", "whirl", "xerox", "yacht", "zesty",
    "blaze", "candy", "flask", "glide", "hobby", "laser", "maple", "nexus", "prism", "quick",
    "shade", "titan", "vines", "abode", "bongo", "crush", "flint", "grime", "ideal", "kiwi",
    "lunar", "niche", "opal", "plush", "quirky", "solar", "truce", "wharf", "zoned", "ample",
    "brave", "chime", "dusty", "fluke", "grins", "inert", "karma", "lucid", "novel", "prism",
    "quack", "scold", "twist", "vocal", "yahoo", "zappy", "amber", "brute", "cloud", "dance",
    "fable", "grime", "howdy", "index", "kiosk", "lucky", "noted", "pizza", "quest", "snail",
    "unbox", "vouch", "waltz", "xenon", "yummy", "blaze", "crisp", "fluff", "grist", "hound",
    "jolly", "knave", "lynch", "muddy", "optic", "prong", "quake", "rusty", "silky", "trace",
    "uplift", "wacky", "blaze", "comic", "frost", "glide", "hazel", "jewel", "knoll", "laugh",
    "mural", "noisy", "optic", "plush", "quake", "rushy", "swift", "uncle", "viper", "wowed",
    "bloke", "candy", "dream", "frisk", "gusty", "ivory", "juicy", "kudos", "liven", "murky",
    "pixel", "quirky", "rove", "surge", "token", "voice", "whiff", "xerox", "yappy", "zesty",
    "bliss", "cider", "dandy", "ember", "frown", "glint", "horde", "irate", "joust", "knurl",
    "lunar", "mixup", "nymph", "opine", "plush", "quota", "snore", "trust", "vitae", "whoop",
    "xenon", "yodel", "zilch", "adore", "brave", "chump", "dusty", "flake", "grind", "hazel"]
    return random.choice(words)

def check_guess(guess, word):
    correct_pos = 0
    correct_letter = []
    wrong_pos = []
    for i in range(5):
        if guess[i] == word[i]:
            correct_pos += 1
        elif guess[i] in word:
            correct_letter.append(guess[i])
        else:
            wrong_pos.append(guess[i])
    return correct_pos, correct_letter, wrong_pos

root = tk.Tk()
root.geometry("800x800")
game = WordleGame(root)
root.mainloop()
