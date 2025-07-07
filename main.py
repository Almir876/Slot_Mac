import random

MAX_LINES = 3
MAX_BET = 200
MIN_BET = 1

ROWS = 3
COLS = 3

symbolCount = {"A": 3, "B": 6, "C": 6, "D": 5}
symbolValue = {"A": 5, "B": 4, "C": 3, "D": 2}

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

def printSpin(columns):
    for row in range(len(columns[0])):
        for i, column in enumerate(columns):
            end = " | " if i != len(columns) - 1 else ""
            print(column[row], end=end)
        print()

def deposit():
    while True:
        amount = input("How much would you like to deposit? $")
        if amount.isdigit():
            amount = int(amount)
            if amount > 0:
                return amount
            else:
                print("Deposit must be greater than 0.")
        else:
            print("Please enter a number.")

def getNumberOfLines():
    while True:
        lines = input(f"Which lines would you like to bet on (1-{MAX_LINES})? ")
        if lines.isdigit():
            lines = int(lines)
            if 1 <= lines <= MAX_LINES:
                return lines
            else:
                print("Enter a valid number of lines.")
        else:
            print("Please enter a number.")

def getBet():
    while True:
        bet = input("How much would you like to bet on each line? $")
        if bet.isdigit():
            bet = int(bet)
            if MIN_BET <= bet <= MAX_BET:
                return bet
            else:
                print(f"Bet amount has to be between ${MIN_BET} - ${MAX_BET}")
        else:
            print("Please enter a number.")

def game(balance):
    noLines = getNumberOfLines()
    while True:
        bet = getBet()
        totalBet = bet * noLines
        if balance < totalBet:
            print(f"You do not have enough balance to bet that amount. Your current balance is ${balance}")
        else:
            break

    print(f"You are betting ${bet} on {noLines} lines. Total amount is ${totalBet}")

    slots = getSpin(ROWS, COLS, symbolCount)
    printSpin(slots)
    winnings, winLines = checkWinnings(slots, noLines, bet, symbolValue)

    print(f"You won ${winnings}")
    if winLines:
        print("You won on lines:", *winLines)
    else:
        print("No winning lines.")

    return winnings - totalBet

def main():
    balance = deposit()
    while True:
        print(f"Current balance is ${balance}")
        answer = input("Press enter to play (q to quit): ")
        if answer.lower() == "q":
            break
        balance += game(balance)
    print(f"You left with ${balance}")

main()
