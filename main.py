import tkinter as tk
import tkinter.font as tkFont
import random
import time
from tkinter import messagebox

AQUAMARINE = '#948979'
DARK_GREY = '#153448'
LIGHT_GREY = '#3C5B6F'
GOLDENROD = '#DFD0B8'
START_TIME = 60
WORDS_DISPLAYED = 2


class TypingSpeedTest:
    def __init__(self, master):
        self.master = master
        self.master.title("Typing Speed Test")
        self.master.geometry("400x525")
        self.master.config(bg=DARK_GREY)  # Dark Slate Gray

        # Load words from file
        try:
            with open("word_list.txt", "r") as f:
                self.words = f.read().splitlines()
        except FileNotFoundError:
            tk.messagebox.showerror("Error", "word_list.txt file not found!")
            self.master.quit()

        self.current_words = []
        self.start_time = 0
        self.best_gross_wpm = 0
        self.best_net_wpm = 0
        self.best_cpm = 0
        self.uncorrected_errors = 0
        self.total_characters_typed = 0
        self.test_running = False
        self.timer_id = None  # Store timer ID for cancelling

        self.custom_font = tkFont.Font(family="Helvetica", size=24, weight="bold")
        self.label_font = tkFont.Font(family="Helvetica", size=14)
        self.result_font = tkFont.Font(family="Helvetica", size=12)

        # Create a frame for the main content
        self.frame = tk.Frame(self.master, bg=LIGHT_GREY)  # Medium Slate Gray
        self.frame.pack(pady=20, padx=20, fill=tk.BOTH, expand=True)

        self.label_instruction = tk.Label(self.frame, text="Type the words below:", font=self.label_font,
                                          bg=LIGHT_GREY, fg=GOLDENROD)  # Pale Goldenrod
        self.label_instruction.pack(pady=10)

        self.word_display = tk.Label(self.frame, text="", font=self.custom_font, bg=AQUAMARINE, fg=DARK_GREY, pady=10)
        self.word_display.pack(pady=10)

        self.entry = tk.Entry(self.frame, font=self.custom_font, bg=GOLDENROD, fg=DARK_GREY)
        self.entry.pack(pady=10)

        self.label_result = tk.Label(self.frame, text="", font=self.result_font, bg=LIGHT_GREY, fg=GOLDENROD)
        self.label_result.pack(pady=10)

        self.label_timer = tk.Label(self.frame, text=f"Time left: {START_TIME}", font=self.label_font, bg=LIGHT_GREY,
                                    fg=GOLDENROD)
        self.label_timer.pack(pady=10)

        self.button_start = tk.Button(self.frame, text="Start Test", font=self.label_font, command=self.start_test,
                                      bg="#4CAF50", fg="white", padx=20, pady=5)
        self.button_start.pack(pady=5)

        self.button_reset = tk.Button(self.frame, text="Reset", font=self.label_font, command=self.reset_test,
                                      state=tk.DISABLED, bg="#f44336", fg="white", padx=20, pady=5)
        self.button_reset.pack(pady=5)

        # Bind space bar to check_input method
        self.entry.bind("<space>", self.check_input)

    def start_test(self):
        if not self.test_running:
            self.current_words = random.sample(self.words, WORDS_DISPLAYED)
            self.update_word_display()
            self.start_time = time.time()
            self.test_running = True
            self.uncorrected_errors = 0
            self.total_characters_typed = 0
            self.entry.delete(0, tk.END)  # Clear entry field
            self.entry.config(state=tk.NORMAL)  # Re-enable entry field
            self.button_start.config(state=tk.DISABLED)
            self.button_reset.config(state=tk.NORMAL)
            self.entry.focus_set()
            self.start_timer(START_TIME)  # Set timer to 60 seconds initially

    def update_word_display(self):
        self.word_display.config(text=" ".join(self.current_words))

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

            if input_word == self.current_words[0]:
                self.current_words.pop(0)  # Remove the finished word
                if len(self.current_words) < WORDS_DISPLAYED:
                    self.current_words.append(random.choice(self.words))
                self.update_word_display()
                self.label_result.config(text=f"Gross WPM: {gross_wpm}\nBest Gross WPM: "
                                              f"{self.best_gross_wpm}\nNet WPM: {net_wpm}\nBest Net WPM: "
                                              f"{self.best_net_wpm}\nCPM: {cpm}\nBest CPM: {self.best_cpm}")
            else:
                self.label_result.config(text="Incorrect. Try again.")
                self.uncorrected_errors += 1

            self.entry.delete(0, tk.END)
            return "break"  # Prevent the default behavior of inserting a space

    def start_timer(self, seconds):
        if self.timer_id is not None:
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
            self.button_reset.config(state=tk.NORMAL)  # Enable reset button
            self.test_running = False

    def reset_test(self):
        if self.timer_id is not None:
            self.master.after_cancel(self.timer_id)  # Cancel timer if running
        self.entry.delete(0, tk.END)  # Clear entry field
        self.entry.config(state=tk.NORMAL)  # Re-enable entry field
        self.button_start.config(state=tk.NORMAL)
        self.button_reset.config(state=tk.DISABLED)
        self.test_running = False
        self.label_result.config(text="")
        self.label_timer.config(text=f"Time left: {START_TIME}")
        self.uncorrected_errors = 0
        self.total_characters_typed = 0
        self.best_gross_wpm = 0
        self.best_net_wpm = 0
        self.best_cpm = 0
        self.entry.focus_set()  # Set focus back to entry field


root = tk.Tk()
app = TypingSpeedTest(root)
root.mainloop()
