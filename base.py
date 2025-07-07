import random
import customtkinter as ctk
import time
from threading import Thread

ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")

MAX_LINES = 3
MAX_BET = float('inf')
MIN_BET = 1

ROWS = 3
COLS = 3
symbolCount = {"A": 9, "B": 6, "C": 6, "D": 5}
symbolValue = {"A": 5, "B": 4, "C": 3, "D": 2}

symbolGraphics = {
    "A": "🌟",
    "B": "🍀",
    "C": "🔥",
    "D": "🍒"
}

def getSpin(rows, cols, symbols):
    allSyms = []
    for sym, count in symbols.items():
        allSyms.extend([sym] * count)

    columns = []
    for _ in range(cols):
        column = []
        currSyms = allSyms[:]
        for _ in range(rows):
            value = random.choice(currSyms)
            currSyms.remove(value)
            column.append(value)
        columns.append(column)
    return columns

def checkWinnings(columns, lines, bet, values):
    winnings = 0
    winLines = []
    for line in range(lines):
        symbol = columns[0][line]
        for column in columns:
            if column[line] != symbol:
                break
        else:
            winnings += values[symbol] * bet
            winLines.append(line + 1)
    return winnings, winLines

class SlotMachineApp(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("Slot Machine")
        self.geometry("600x700")

        self.bg_frame = ctk.CTkFrame(self, fg_color="#1e1e2f")
        self.bg_frame.pack(fill="both", expand=True)

        self.title_label = ctk.CTkLabel(self.bg_frame, text="🔥 SLOT MACHINE 🔥", font=("Arial Black", 36, "bold"))
        self.title_label.pack(pady=20)

        self.balance = 0

        self.balance_label = ctk.CTkLabel(self.bg_frame, text=f"Balance: $0", font=("Oswald", 20))
        self.balance_label.pack(pady=10)

        self.deposit_entry = ctk.CTkEntry(self.bg_frame, placeholder_text="Deposit amount")
        self.deposit_entry.pack(pady=5)

        self.deposit_button = ctk.CTkButton(self.bg_frame, text="Deposit", command=self.deposit)
        self.deposit_button.pack(pady=5)

        self.bet_entry = ctk.CTkEntry(self.bg_frame, placeholder_text="Bet per line")
        self.bet_entry.pack(pady=5)

        self.lines_entry = ctk.CTkEntry(self.bg_frame, placeholder_text=f"Lines (1-{MAX_LINES})")
        self.lines_entry.pack(pady=5)

        self.spin_button = ctk.CTkButton(self.bg_frame, text="Spin", command=self.start_spin)
        self.spin_button.pack(pady=10)

        self.result_label = ctk.CTkLabel(self.bg_frame, text="", font=("Arial", 18))
        self.result_label.pack(pady=10)

        self.slots_frame = ctk.CTkFrame(self.bg_frame, fg_color="#2d2d44")
        self.slots_frame.pack(pady=10)

        self.slot_labels = [[ctk.CTkLabel(self.slots_frame, text="", width=60, height=50, font=("Arial", 30)) for _ in range(COLS)] for _ in range(ROWS)]
        for r in range(ROWS):
            for c in range(COLS):
                self.slot_labels[r][c].grid(row=r, column=c, padx=15, pady=10)

    def deposit(self):
        try:
            amount = int(self.deposit_entry.get())
            if amount > 0:
                self.balance += amount
                self.update_balance()
                self.deposit_entry.delete(0, ctk.END)
        except ValueError:
            pass

    def update_balance(self):
        self.balance_label.configure(text=f"Balance: ${self.balance}")

    def start_spin(self):
        Thread(target=self.play_game).start()

    def play_game(self):
        try:
            bet = int(self.bet_entry.get())
            lines = int(self.lines_entry.get())
            total_bet = bet * lines
            if lines < 1 or lines > MAX_LINES or bet < MIN_BET or bet > MAX_BET:
                self.result_label.configure(text="Invalid bet or lines.")
                return
            if total_bet > self.balance:
                self.result_label.configure(text="Insufficient balance.")
                return

            self.balance -= total_bet
            self.update_balance()

            for _ in range(10):
                fake_spin = getSpin(ROWS, COLS, symbolCount)
                self.display_slots(fake_spin)
                time.sleep(0.1)

            final_slots = getSpin(ROWS, COLS, symbolCount)
            winnings, win_lines = checkWinnings(final_slots, lines, bet, symbolValue)
            self.balance += winnings
            self.update_balance()
            self.display_slots(final_slots)
            if win_lines:
                self.result_label.configure(text=f"Won ${winnings} on lines: {win_lines}")
            else:
                self.result_label.configure(text="No winning lines.")
        except ValueError:
            self.result_label.configure(text="Please enter valid numbers.")

    def display_slots(self, columns):
        for r in range(ROWS):
            for c in range(COLS):
                sym = columns[c][r]
                display = symbolGraphics.get(sym, sym)
                self.slot_labels[r][c].configure(text=display)

if __name__ == '__main__':
    app = SlotMachineApp()
    app.mainloop()
