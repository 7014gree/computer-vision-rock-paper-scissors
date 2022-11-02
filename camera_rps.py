import cv2
from keras.models import load_model
import numpy as np
import time
import random
model = load_model('keras_model.h5')
cap = cv2.VideoCapture(0)
data = np.ndarray(shape=(1, 224, 224, 3), dtype=np.float32)

def capture(model_, cap_, data_) -> np.array:
    ret, frame = cap.read()
    resized_frame = cv2.resize(frame, (224, 224), interpolation = cv2.INTER_AREA)
    image_np = np.array(resized_frame)
    normalized_image = (image_np.astype(np.float32) / 127.0) - 1 # Normalize the image
    data[0] = normalized_image
    prediction = model.predict(data)
    cv2.imshow('frame', frame)
    # Press q to close the window
    return prediction

def countdown():
    a = time.time()
    n = 4
    while n > 0:
        if time.time() - a > 1:
            a = time.time()
            n -= 1
            print(n)

def get_prediction(input: np.array) -> str:
    list = ["rock", "paper", "scissors", "Nothing"]
    #return f"You chose {list[np.argmax(input[0])]}."
    return list[np.argmax(input[0])]

def get_computer_choice() -> str:
    return random.choice(["rock", "paper", "scissors"])

def get_winner(computer_choice: str, user_choice: str) -> str:
    print(computer_choice)
    u_w = "User wins"
    c_w = "Computer wins"
    if computer_choice == user_choice:
        return "Tie"
    elif computer_choice == "rock":
        if user_choice == "paper":
            return u_w
        else:
            return c_w
    elif computer_choice == "paper":
        if user_choice == "scissors":
            return u_w
        else:
            return c_w
    else:
        if user_choice == "rock":
            return u_w
        else:
            return c_w

def play(model_, cap_, data_):
    user_choice = get_prediction(capture(model_, cap_, data_))
    computer_choice = get_computer_choice()
    print(user_choice, computer_choice)

    countdown()
    return get_winner(computer_choice, user_choice)

computer_wins = 0
user_wins = 0

while max(computer_wins, user_wins) < 3:
    result = play(model, cap, data)
    if result == "User wins":
        user_wins += 1
    elif result == "Computer wins":
        computer_wins += 1
    print(f"{result}. Computer: {computer_wins} vs User: {user_wins}.")



