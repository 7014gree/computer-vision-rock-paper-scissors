import random


choices = ["Rock", "Paper", "Scissors"]

def get_computer_choice() -> str:
    return random.choice(["Rock", "Paper", "Scissors"])

def get_user_choice() -> str:
    while True:
        choice = str(input("Select 'Rock', 'Paper', or 'Scissors': ")).lower()
        if choice in ("rock", "paper", "scissors"):
            return choice

