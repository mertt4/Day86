import tkinter as tk
import tkinter.font as tkFont
import random
import time
from tkinter import messagebox


class TypingSpeedTest:
    def __init__(self, master):
        self.master = master
        self.master.title("Typing Speed Test")
        self.master.geometry("400x525")
        self.master.config(bg="#153448")  # Dark Slate Gray

        # Load words from file
        try:
            with open("word_list.txt", "r") as f:
                self.words = f.read().splitlines()
        except FileNotFoundError:
            tk.messagebox.showerror("Error", "word_list.txt file not found!")
            self.master.quit()

        self.current_word = ""
        self.start_time = 0
        self.best_gross_wpm = 0
        self.best_net_wpm = 0
        self.best_cpm = 0
        self.uncorrected_errors = 0
        self.total_characters_typed = 0
        self.test_running = False

        self.custom_font = tkFont.Font(family="Helvetica", size=24, weight="bold")
        self.label_font = tkFont.Font(family="Helvetica", size=14)
        self.result_font = tkFont.Font(family="Helvetica", size=12)

        # Create a frame for the main content
        self.frame = tk.Frame(self.master, bg="#3C5B6F")  # Medium Slate Gray
        self.frame.pack(pady=20, padx=20, fill=tk.BOTH, expand=True)

        self.label_instruction = tk.Label(self.frame, text="Type the word below:", font=self.label_font,
                                          bg="#3C5B6F", fg="#DFD0B8")  # Pale Goldenrod
        self.label_instruction.pack(pady=10)

        self.word_display = tk.Label(self.frame, text="", font=self.custom_font, bg="#948979", fg="#153448", pady=10)  # Medium Aquamarine for background, Dark Slate Gray for text
        self.word_display.pack(pady=10)

        self.entry = tk.Entry(self.frame, font=self.custom_font, bg="#DFD0B8", fg="#153448")  # Pale Goldenrod for background, Dark Slate Gray for text
        self.entry.pack(pady=10)

        self.label_result = tk.Label(self.frame, text="", font=self.result_font, bg="#3C5B6F", fg="#DFD0B8")  # Medium Slate Gray for background, Pale Goldenrod for text
        self.label_result.pack(pady=10)

        self.label_timer = tk.Label(self.frame, text="Time left: 60", font=self.label_font, bg="#3C5B6F", fg="#DFD0B8")  # Medium Slate Gray for background, Pale Goldenrod for text
        self.label_timer.pack(pady=10)

        self.button_start = tk.Button(self.frame, text="Start Test", font=self.label_font, command=self.start_test,
                                      bg="#4CAF50", fg="white", padx=20, pady=5)
        self.button_start.pack(pady=5)

        self.button_restart = tk.Button(self.frame, text="Restart", font=self.label_font, command=self.restart_test,
                                        state=tk.DISABLED, bg="#f44336", fg="white", padx=20, pady=5)
        self.button_restart.pack(pady=5)

    def start_test(self):
        if not self.test_running:
            self.new_word()
            self.start_time = time.time()
            self.test_running = True
            self.uncorrected_errors = 0
            self.total_characters_typed = 0
            self.button_start.config(state=tk.DISABLED)
            self.button_restart.config(state=tk.NORMAL)
            self.entry.bind("<space>", self.check_input)
            self.entry.focus_set()
            self.start_timer(60)  # Set timer to 60 seconds initially

    def new_word(self):
        self.current_word = random.choice(self.words)
        self.word_display.config(text=self.current_word)

    def check_input(self, event):
        if self.test_running:
            input_word = self.entry.get().strip()  # Remove leading/trailing whitespace
            self.total_characters_typed += len(input_word)
            elapsed_time = time.time() - self.start_time
            gross_wpm = int((self.total_characters_typed / 5) / (elapsed_time / 60))
            net_wpm = gross_wpm - (self.uncorrected_errors / (elapsed_time / 60))
            cpm = int(self.total_characters_typed / (elapsed_time / 60))

            self.best_gross_wpm = max(self.best_gross_wpm, gross_wpm)
            self.best_net_wpm = max(self.best_net_wpm, net_wpm)
            self.best_cpm = max(self.best_cpm, cpm)

            if input_word == self.current_word:
                self.label_result.config(text=f"Gross WPM: {gross_wpm}\nBest Gross WPM: "
                                              f"{self.best_gross_wpm}\nNet WPM: {net_wpm}\nBest Net WPM: "
                                              f"{self.best_net_wpm}\nCPM: {cpm}\nBest CPM: {self.best_cpm}")
            else:
                self.label_result.config(text="Incorrect. Try again.")
                self.uncorrected_errors += 1

            self.entry.delete(0, tk.END)
            self.new_word()
            return "break"  # Prevent the default behavior of inserting a space

    def start_timer(self, seconds):
        if hasattr(self, 'timer_id'):
            self.master.after_cancel(self.timer_id)
        self.remaining_time = seconds
        self.update_timer()

    def update_timer(self):
        self.label_timer.config(text=f"Time left: {self.remaining_time}")
        if self.remaining_time > 0:
            self.remaining_time -= 1
            self.timer_id = self.master.after(1000, self.update_timer)
        else:
            self.label_timer.config(text="Time left: 0")
            self.entry.config(state=tk.DISABLED)
            self.button_start.config(state=tk.NORMAL)
            self.button_restart.config(state=tk.DISABLED)
            self.test_running = False

    def restart_test(self):
        self.entry.config(state=tk.NORMAL)
        self.button_start.config(state=tk.NORMAL)
        self.button_restart.config(state=tk.DISABLED)
        self.label_result.config(text="")
        self.label_timer.config(text="Time left: 60")
        self.test_running = False
        self.uncorrected_errors = 0
        self.total_characters_typed = 0
        self.best_gross_wpm = 0
        self.best_net_wpm = 0
        self.best_cpm = 0
        self.new_word()
        self.start_timer(60)  # Reset timer to 60 seconds


root = tk.Tk()
app = TypingSpeedTest(root)
root.mainloop()
