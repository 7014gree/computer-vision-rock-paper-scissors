import cv2
from keras.models import load_model
import numpy as np
import time
import random
from dataclasses import dataclass

@dataclass
class Camera():
    model = load_model('keras_model.h5')
    cap = cv2.VideoCapture(0)
    data = np.ndarray(shape=(1, 224, 224, 3), dtype=np.float32)
    ret, frame = cap.read()
    resized_frame = cv2.resize(frame, (224, 224), interpolation = cv2.INTER_AREA)
    cv2.imshow('frame', frame)

    def get_user_choice(self):
        image_np = np.array(self.resized_frame)
        normalized_image = (image_np.astype(np.float32) / 127.0) - 1 # Normalize the image
        data[0] = normalized_image
        prediction = model.predict(data)
        options = ["rock", "paper", "scissors", "Nothing"]
        return options[np.argmax(prediction[0])]
    
@dataclass
class Game():
    winning_score = 3

    computer_choice: int
    user_choice: int
    computer_score = 0
    user_score = 0

    camera = Camera()

    @property
    def computer_choice(self):
        return self.computer_choice

    @computer_choice.setter
    def computer_choice(self):
        self.computer_choice = random.choice(["rock", "paper", "scissors"])

    @property
    def user_choice(self):
        return self.user_choice

    @user_choice.setter()
    def user_choice(self):
        print("Getting user choice from camera/model")
        self.user_choice = 0

    def get_winner(self):
        print(self.computer_choice)
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
        while max(self.computer_wins, self.user_wins) < self.winning_score:
            result = self.new_turn()


    def new_turn(self):
        self.computer_choice()
        self.countdown()
        self.user_input = self.camera.get_user_choice()
        self.get_winner()
        self.game_status()

    @staticmethod
    def countdown():
        timer = time.time()
        seconds_remaining = 3
        while seconds_remaining > 0:
            # Every second, deduct 1 from seconds remaining and print
            if time.time() - timer  > 1:
                timer = time.time()
                seconds_remaining -= 1
                print(seconds_remaining)
        
g = Game()