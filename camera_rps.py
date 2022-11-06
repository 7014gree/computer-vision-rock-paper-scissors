import cv2
from keras.models import load_model
import numpy as np
import time
import random
from dataclasses import dataclass


print("Game loading...")

model = load_model('keras_model.h5')
cap = cv2.VideoCapture(0)
data = np.ndarray(shape=(1, 224, 224, 3), dtype=np.float32)

    
@dataclass
class Game(): 
    # Game will end once either user or computer has won 3 times.
    winning_score = 3

    # Is it worth implementing getters and setters for these?
    computer_choice = random.choice(["rock", "paper", "scissors"])
    user_choice = "Awaiting input."
    computer_score = 0
    user_score = 0

    game_active = True

    # Logic for determining winner. If no input is received from user "Tie" is returned and nothing happens.
    # Returns the string for who won the turn to eventually end up on the frame.
    def get_winner(self):
        if self.computer_choice == self.user_choice or self.user_choice == "Nothing":
            return("Tie")
        elif self.computer_choice == "rock":
            if self.user_choice == "paper":
                self.user_score += 1
                return "User Wins"
            else:
                self.computer_score += 1
                return "Computer Wins"
        elif self.computer_choice == "paper":
            if self.user_choice == "scissors":
                self.user_score += 1
                return "User Wins"
            else:
                self.computer_score += 1
                return "Computer Wins"
        elif self.computer_choice == "scissors":
            if self.user_choice == "rock":
                self.user_score += 1
                return "User Wins"
            else:
                self.computer_score += 1
                return "Computer Wins"
    
    # Could probably combine this with get_winner()
    def new_turn(self):
        self.computer_choice = random.choice(["rock", "paper", "scissors"])
        return self.get_winner()

# Counts down from "start" to zero.
def countdown_generator(start: int):
    assert start > 0
    while True:
        countdown_numbers = [n for n in range(start, -1, -1)]
        for number in countdown_numbers:
            yield number


print("Game starting...") 

g = Game()

start_time = time.time()

# Generator yields 2, 1, 0 because the counter is manually reset to 3 each time.
# Otherwise the counter would show 3 for two seconds (one for manual reset, another from generator).
counter = countdown_generator(2)
current_countdown = 3

# while loop to keep camera frame open.
while True:
    # For camera window/frame and model prediction.
    ret, frame = cap.read()
    resized_frame = cv2.resize(frame, (224, 224), interpolation = cv2.INTER_AREA)
    image_np = np.array(resized_frame)
    normalized_image = (image_np.astype(np.float32) / 127.0) - 1 # Normalize the image
    data[0] = normalized_image
    # verbose = 0 reduces spam to terminal
    prediction = model.predict(data, verbose = 0)

    # If statement checks that neither player has won the game yet.
    # Could use assertion instead of the if statement? Unsure of the difference/benefit.
    if max(g.computer_score, g.user_score) < g.winning_score:
        # Updates countdown each second.
        if time.time() - start_time > 1:
            current_countdown = next(counter)
            start_time = time.time()

        # Selects rock, paper, scissors, or nothing from highest weighted prediction per the model and input from camera.
        camera_choice = ["rock", "paper", "scissors", "Nothing"][np.argmax(prediction[0])]

        # Annotates frame with current user input and current state of game (i.e. countdown, scores, result of turn if countdown is zero).
        cv2.putText(frame, f"User: {camera_choice}", (20, 50), 0, 1.5, (255, 250, 205))
        cv2.putText(frame, str(current_countdown), (20, 100), 0, 1.5, (255, 250, 205))
        cv2.putText(frame, f"Computer score: {g.computer_score}", (20, 150), 0, 1.5, (255, 250, 205))
        cv2.putText(frame, f"User score: {g.user_score}", (20, 200), 0, 1.5, (255, 250, 205))
        if current_countdown == 0:
            g.user_choice = camera_choice
            cv2.putText(frame, g.new_turn(), (20, 300), 0, 1.5, (255, 250, 205))
            cv2.putText(frame, f"Computer: {g.computer_choice}", (20, 250), 0, 1.5, (255, 250, 205))
    else:
        # Annotates frame for final results.
        cv2.putText(frame, f"Final scores:", (20, 50), 0, 1.5, (255, 250, 205))
        cv2.putText(frame, f"Computer score: {g.computer_score}", (20, 100), 0, 1.5, (255, 250, 205))
        cv2.putText(frame, f"User score: {g.user_score}", (20, 150), 0, 1.5, (255, 250, 205))
        # Pulls from the tuple 'User' if g.user_score < g.computers_score is False (i.e. take 0 index from the tuple). Takes 'Computer' if True.
        cv2.putText(frame, f"{('User', 'Computer')[g.user_score < g.computer_score]} wins!", (20, 200), 0, 1.5, (255, 250, 205))
        cv2.putText(frame, f"Press 'q' to exit.", (20, 250), 0, 1.5, (255, 250, 205))

    # Displays annotated frame.
    cv2.imshow('frame', frame)

    # Closes frame on 'q' key press.
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

    # Freeze frame for 1.5s once move has been made.
    if current_countdown == 0:
        while time.time() - start_time < 1.5:
            pass
        start_time = time.time()
        current_countdown = 3

# After the loop release the cap object
cap.release()
# Destroy all the windows
cv2.destroyAllWindows()