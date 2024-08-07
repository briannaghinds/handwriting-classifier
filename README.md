## Python Paint Application with MNIST ANN Model
Breakdown of files:

(1) Button.py: Button class (from YouTuber CodingWithRuss)

(2) mnist_model.ipynb: Jupyter Notebook where the MNIST dataset model is built, trained, and tested.

(3) paint.py: file that handles all of the GUI
- creates the GUI window
- FUNCTIONALITIES: change paint size, change paint color, clear screen button, screenshot/predict button
- v1 (August 7th): the screenshot method takes a screenshot of the GUI window canvas and prints out the model's prediction

---
#### Ideas for Improvement?
- make the user input what the actual answer was so that answers can be compared
- instead of just printing the model prediction, find a way to display it on the GUI window