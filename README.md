# computer-vision-rock-paper-scissors

## Milestone 2
- Created an image project model at https://teachablemachine.withgoogle.com/ with classes for rock, paper, scissors, nothing
- Had to update and retrain the model since it was not accurate enough at first
- Downloaded the model files, moved to the git directory and pushed to github

## Milestone 4
- Set up conda environment using ```conda create -n rps_env``` and activated the environment with ```conda activate rps_env```
- Installed pip with ```conda install pip``` then installed other packages using pip: tensorflow, opencv-python, ipykernel
- Implemented rock, paper, scissors in manual_rps.py using ```random.choice()``` to generate a choice from the computer and prompting a user input for the user's choice.

## Milestone 5
- Initial implementation is working but needs refactoring.
- Took code from RPS-Template to capture a single frame and adapated code from manual_rps for the computer choice and handling who won/loss each round
- Implemented the rock, paper, scissors game as a class
- First tried to implement the camera as a class but that seemed to exacerbate issues around only capturing a single frame.
- Moved camera to a while loop within which methods for the game class were called.
- Added text annotations to the camera frame to show the current user input move, the computer move once the user move had been locked in, running scores throughout the game, and a final score screen.
- Could tidy up class methods and formatting of annotations, among other things.
- The model itself isn't the most accurate - struggled to get it to take a user input for 'rock'.