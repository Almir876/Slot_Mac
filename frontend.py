import random
import customtkinter as ctk

ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")

MAX_LINES = 3
MAX_BET = 200
MIN_BET = 1

ROWS = 3
COLS = 3
symbolCount = {"A": 3, "B": 6, "C": 6, "D": 5}
symbolValue = {"A": 5, "B": 4, "C": 3, "D": 2}

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
        self.geometry("600x500")

        self.balance = 0

        self.balance_label = ctk.CTkLabel(self, text=f"Balance: $0", font=("Arial", 18))
        self.balance_label.pack(pady=10)

        self.deposit_entry = ctk.CTkEntry(self, placeholder_text="Deposit amount")
        self.deposit_entry.pack(pady=5)

        self.deposit_button = ctk.CTkButton(self, text="Deposit", command=self.deposit)
        self.deposit_button.pack(pady=5)

        self.bet_entry = ctk.CTkEntry(self, placeholder_text="Bet per line")
        self.bet_entry.pack(pady=5)

        self.lines_entry = ctk.CTkEntry(self, placeholder_text=f"Number of lines (1-{MAX_LINES})")
        self.lines_entry.pack(pady=5)

        self.spin_button = ctk.CTkButton(self, text="Spin", command=self.play_game)
        self.spin_button.pack(pady=10)

        self.result_label = ctk.CTkLabel(self, text="", font=("Arial", 16))
        self.result_label.pack(pady=10)

        self.slots_frame = ctk.CTkFrame(self)
        self.slots_frame.pack(pady=10)

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
            slots = getSpin(ROWS, COLS, symbolCount)
            winnings, win_lines = checkWinnings(slots, lines, bet, symbolValue)
            self.balance += winnings
            self.update_balance()
            self.display_slots(slots)
            if win_lines:
                self.result_label.configure(text=f"Won ${winnings} on lines: {win_lines}")
            else:
                self.result_label.configure(text="No winning lines.")
        except ValueError:
            self.result_label.configure(text="Please enter valid numbers.")

    def display_slots(self, columns):
        for widget in self.slots_frame.winfo_children():
            widget.destroy()
        for row in range(ROWS):
            for col in range(COLS):
                symbol = columns[col][row]
                label = ctk.CTkLabel(self.slots_frame, text=symbol, width=40, height=30, font=("Arial", 20))
                label.grid(row=row, column=col, padx=10, pady=5)

if __name__ == '__main__':
    app = SlotMachineApp()
    app.mainloop()
