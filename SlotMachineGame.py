# Assuming the slot machine is of 3X3 size and person will win if he gets 3 of a kind

import random  # Import the random module
import winsound

MAX_LINES = 3 # This is a constant value that will not change and it is convention in python to write it in all caps.
MAX_BET = 100 
MIN_BET = 1

ROWS = 3 # Describing the rows count for this slot machine will be 3
COLS = 3 # Describing the columns count for this slot machine will be 3

# Dictionary defining the number of times each symbol appears 
symbol_count = {
    "A":2, # Symbol A appears 2 times
    "B":4, # Symbol B appears 4 times
    "C":6, # Symbol C appears 6 times
    "D":8, # Symbol D appears 8 times
}

symbol_value = {
    "A": 2,
    "B": 4,
    "C": 6,
    "D": 8,
}



def check_winnings(columns, lines, bet, values):
    """
    Function to check for winning lines in a slot machine and calculate winnings.
    
    Parameters:
    - columns: List of lists representing the slot machine grid (each sublist is a column).
    - lines: Number of horizontal lines to check for winnings.
    - bet: The bet amount per line.
    - values: Dictionary mapping symbols to their payout values.

    Returns:
    - winnings: Total amount won.
    - winning_lines: List of line numbers where a win occurred.
    
    """
    
    winnings = 0 # Initialize winnings to 0
    winning_lines = [] # List to store winning line nubmers
    
    # Iterate through each line ( row ) to check for a win
    for line in range(lines):
        symbol = columns[0][line] # Take the first column's symbol as the reference for this line
        
        # Check if all symbols in this line ( across all columns ) match the reference symbol
        
        for column in columns:
            symbol_to_check = column[line] # Get the symbol at the current line from the current column
            
            if symbol != symbol_to_check: # If any symbol is different, it's not a winnig line
                break
        else:
            winnings += values[symbol] * bet
            winning_lines.append(line+1)
            
    return winnings, winning_lines



def get_slot_machine_spin(rows, cols, symbols):
    
    """
    Function to simulate a slot machine spin.
    Generates a grid of rows X cols with randomly selected symbols.
    Ensures that each column contains unique symbols.
    
    """
    
    # Create a list of all symbols with their respective counts
    all_symbols = []
    for symbol, symbol_count in symbols.items(): # Iterate over the symbol dictionary
        for _ in range(symbol_count): # _ is used here as a throwaway variable we don't need its value
            all_symbols.append(symbol) # Add each symbol 'count' times to the list
    
    # Initialize an empty list to store the final grid ( columns )
    columns = []
    
    # Generate 'cols' number of columns
    for _ in range(cols):
        column = []  # list to store symbols for the current column
        current_symbols = all_symbols[:] # Create a copy of all symobls for random selectionn
        
        # Select 'rows' unique symbols for this column
        
        for _ in range(rows):
            value = random.choice(current_symbols) # Pick a random symbol
            current_symbols.remove(value) # Remove the symbol to ensure uniqueness in the column
            column.append(value) # Add the symbol to the column
        
        # append the completed column to the final grid
        
        columns.append(column)
    
    return columns 


# Function to print the slot machine grid in a structured format
def print_slot_machine(columns):
    
    # Iterate over each row ( rows are determined by the length of first column)
    for row in range(len(columns[0])):
        
        # Iterate through each column in the slot machine
        for i, column in enumerate(columns):
            
            # print the symbol in the current row of the column
            # If it's not the last column, print with '|' separator
            if i != len(columns) - 1:
                print(column[row], end=' | ') # Prevents moving to a new line
                
                # If it's the last coloumn, just print the symbol and move to the next line
            else:
                print(column[row])


def deposit(): # This function will handle the deposit money
    while True:
        amount = input("What would you like to deposit? $ ")
        if amount.isdigit():   # this checks if amount inputed is number or not
            amount = int(amount) # this converts the inputed amount to integer
            if amount > 0:
                break  # if the amount is positive, this will break the loop and will move to next step
            else:
                print("Amount must be greater than 0.")
        else:
            print("Invalid input. Please input a number.")
    
    return amount


def get_number_of_lines(): # This function will handle the number of lines
    while True:
        lines = input("Enter the number of lines you want to bet on ( 1 -" + str(MAX_LINES) + " )? ") # This will ask the user to input the number of lines they want to bet on
        if lines.isdigit():
            lines = int(lines)
            if lines > 0 and lines <= MAX_LINES: # This will check if the number of lines is between 1 and MAX_LINES
                break
            else:
                print("Enter a valid number of lines.")
        else:
            print("Invalid input. Please input a number.")
    
    return lines


def bet_amount(): # This function will handle the bet amount
    while True:
        amount = input("What would you like to bet on each line? $ ")
        if amount.isdigit():
            amount = int(amount)
            if MIN_BET <= amount <= MAX_BET: # This will check if the bet amount is between MIN_BET and MAX_BET
                break
            else:
                print(f"Amount must be between ${MIN_BET} and ${100}.")
        else:
            print("Enter the valid amount.")

    return amount

def spin(balance):
    
    lines = get_number_of_lines()
    
    while True: # This will keep asking the user to input the bet amount until they input a valid amount, bascially this will check if the total bet is less than total balance or not
        bet = bet_amount()
        total_bet = bet * lines
        
        if total_bet > balance:
            print(f"Your bet is higher than your balance. Your current balance is ${balance}.")
        else:
            break
            
        
         
    print(f"You are betting ${bet} on {lines} lines. Total bet is equal to: $ {total_bet} ")
    
    slots = get_slot_machine_spin(ROWS, COLS, symbol_count)
    print_slot_machine(slots)
    winnings, winning_lines = check_winnings(slots, lines, bet, symbol_value)
    print (f"Your winnings are ${winnings}.")
    
    
    # Print the winning lines in a clean format by unpacking the list
    # Without *, it would print: Your winning lines are [1, 2, 3]
    # With *, it prints: Your winning lines are 1 2 3 (more readable)
    print(f"Your winning lines are", *winning_lines)
    
    return winnings - total_bet


def main():
    balance = deposit()
    
    while True:
        print(f"\nCurrent Balance: ${balance}")
        answer = input("Press Enter to spin the reels or 'q' to quit: ").strip().lower()
        if answer == "q":
            break
        
        balance += spin(balance)
            
    
    print(f"You left with ${balance}")
    
main()