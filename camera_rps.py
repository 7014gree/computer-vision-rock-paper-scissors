import cv2
from keras.models import load_model
import numpy as np
import time
import random
from dataclasses import dataclass


print("Game loading...")

class Camera():
    def __init__(self):
        self.model = load_model('keras_model.h5')
        self.cap = cv2.VideoCapture(0)
        self.data = np.ndarray(shape=(1, 224, 224, 3), dtype=np.float32)


    def get_user_choice(self):
        ret, frame = self.cap.read()
        resized_frame = cv2.resize(frame, (224, 224), interpolation = cv2.INTER_AREA)
        
        image_np = np.array(resized_frame)
        normalized_image = (image_np.astype(np.float32) / 127.0) - 1 # Normalize the image
        self.data[0] = normalized_image
        prediction = self.model.predict(self.data)
        print(prediction)
        choice = ["rock", "paper", "scissors", "Nothing"][np.argmax(prediction[0])]
        cv2.putText(frame, choice, (50, 50), 0, 1.5, (250, 225, 120))
        cv2.imshow('frame', frame)
        print(43)
        cv2.waitKey()
        print(44)
        cv2.destroyAllWindows()
        return choice
    
@dataclass
class Game():
    winning_score = 3

    computer_choice = -1
    user_choice = -1
    computer_score = 0
    user_score = 0

    camera = Camera()

    def get_winner(self):
        print(self.computer_choice, self.user_choice)
        if self.computer_choice == self.user_choice or self.user_choice == "Nothing":
            print("Tie")
        elif self.computer_choice == "rock":
            if self.user_choice == "paper":
                self.user_score += 1
            else:
                self.computer_score += 1
        elif self.computer_choice == "paper":
            if self.user_choice == "scissors":
                self.user_score += 1
            else:
                self.computer_score += 1
        elif self.computer_choice == "scissors":
            if self.user_choice == "rock":
                self.user_score += 1
            else:
                self.computer_score += 1
    
    def game_status(self):
        if max(self.computer_score, self.user_score) < self.winning_score:
            self.new_turn()
        else:
            print(f"Final score: {self.computer_score} : {self.user_score}")


    def new_turn(self):
        self.computer_choice = random.choice(["rock", "paper", "scissors"])
        self.countdown()
        self.user_choice = self.camera.get_user_choice()
        print(f"from camera: {self.user_choice}")
        self.get_winner()
        print(f"current score: computer: {self.computer_score} vs user: {self.user_score}")
        self.game_status()

    @staticmethod
    def countdown():
        timer = time.time()
        seconds_remaining = 4
        while seconds_remaining > 0:
            # Every second, deduct 1 from seconds remaining and print
            if time.time() - timer  > 1:
                timer = time.time()
                seconds_remaining -= 1
                print(seconds_remaining)

print("Game starting...") 
g = Game()
g.game_status()
