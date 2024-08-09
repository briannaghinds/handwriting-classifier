# https://www.youtube.com/watch?v=h2uRcZUfyqM

# import pygame
import pygame
import Button
import cv2
import torch
import matplotlib.pyplot as plt


## FUNCTIONS ######################################################################################################

# method to create the paint toolbar
def draw_menu(size, color):
    # create rectangle and place on screen
    pygame.draw.rect(screen, "gray", [0, 0, WIDTH, 70])

    pygame.draw.line(screen, "black", (0, 70), (WIDTH, 70), 3)

    ## BRUSH SIZES ##
    largeBrush = pygame.draw.rect(screen, "black", [10, 10, 50, 50])  # square menu
    pygame.draw.circle(screen, "white", (35, 35), 15)  # circle showing brush size

    mediumBrush = pygame.draw.rect(screen, "black", [70, 10, 50, 50])
    pygame.draw.circle(screen, "white", (95, 35), 10)  # circle showing brush size

    smallBrush = pygame.draw.rect(screen, "black", [130, 10, 50, 50])  # square menu
    pygame.draw.circle(screen, "white", (155, 35), 5)  # circle showing brush size

    brushList = [largeBrush, mediumBrush, smallBrush]

    # adding a border the size buttons so the user knows that they pressed
    if size == 15:
        pygame.draw.rect(screen, "red", [10, 10, 50, 50], 5)  # square menu
    elif size == 10:
        pygame.draw.rect(screen, "red", [70, 10, 50, 50], 5)  # square menu
    else:
        pygame.draw.rect(screen, "red", [130, 10, 50, 50], 5)  # square menu

    # this circle is just an indicator that shows the user what color they have actively selected
    pygame.draw.circle(screen, color, (400, 35), 30)
    pygame.draw.circle(screen, "dark gray", (400, 35), 30, 5)


    ## COLORS (r, g, b) ##
    blue = pygame.draw.rect(screen, (0, 0, 255), [WIDTH - 35, 10, 25, 25])
    red = pygame.draw.rect(screen, (255, 0, 0), [WIDTH - 35, 35, 25, 25])
    green = pygame.draw.rect(screen, (0, 255, 0), [WIDTH - 60, 10, 25, 25])
    yellow = pygame.draw.rect(screen, (255, 255, 0), [WIDTH - 60, 35, 25, 25])
    teal = pygame.draw.rect(screen, (0, 255, 255), [WIDTH - 85, 10, 25, 25])
    purple = pygame.draw.rect(screen, (255, 0, 255), [WIDTH - 85, 35, 25, 25])
    white = pygame.draw.rect(screen, (0, 0, 0), [WIDTH - 110, 10, 25, 25])
    black = pygame.draw.rect(screen, (255, 255, 255), [WIDTH - 110, 35, 25, 25])

    colorList = [blue, red, green, yellow, teal, purple, white, black]
    rgbList = [(0, 0, 255), (255, 0, 0), (0, 255, 0), (255, 255, 0), (0, 255, 255), (255, 0, 255), (0, 0, 0), (255, 255, 255)]


    return brushList, colorList, rgbList


def drawPainting(items):
    for i in range(len(items)):
        pygame.draw.circle(screen, items[i][0], items[i][1], items[i][2])


# take screenshot function, this runs whenever the user presses the done button
# v1: add the prediction part
def takeScreenshot():
    print("screenshot button pressed")
    global picture

    # take a part of the canvas that we want the program to read
    rect = pygame.Rect(0, 70, WIDTH, 530)
    subScreen = screen.subsurface(rect)
    

    # take screenshot of canvas subScreen
    pygame.image.save(subScreen, f"handwriting/image{picture}.png")
    path = f"handwriting/image{picture}.png"
    print(path)
    predict(path)


    # increment picture so the next picture saves under different name
    picture += 1


def predict(image_path:str):
    # get image, grayscale, resize 
    img = cv2.imread(image_path, cv2.IMREAD_GRAYSCALE)
    img = cv2.resize(img, (28,28))

    # turn to tensor
    data = torch.from_numpy(img).unsqueeze(0).float() / 255.0
    data = torch.reshape(data, (1, 28, 28))

    # load model
    model = torch.load("./model/handwritten_CNN_model.pth")
    model.eval()

    output = model(data)
    pred = output.argmax(dim=1, keepdim=True)

    plt.imshow(img, cmap="gray")

    print(f"Model Predicts...{pred.item()}")


def clearScreen():
    print("clear button pressed")
    screen.fill("white")
    painting.clear()
###############################################################################################################

# ## MAIN ##
pygame.init()
# initialize pen size and color befor 
penSize = 0
penColor = "white"


# set frames per second and clock to run 
FPS = 120
timer = pygame.time.Clock()

# set width and height to screen to display paint gui
WIDTH = 800
HEIGHT = 600
screen = pygame.display.set_mode([WIDTH, HEIGHT])
pygame.display.set_caption("Paint")
painting = []
picture = 0
run = True

## CLEAR BUTTON ##
# load the image
CLEAR = pygame.image.load("buttons/clear.png").convert_alpha()
SCREENSHOT = pygame.image.load("buttons/screenshot.png").convert_alpha()

# call the Button class and set the image as the button
clearButton = Button.Button(625, 9, CLEAR, 0.16)
screenshotButton = Button.Button(550, 9, SCREENSHOT, 0.16)

while run:
    timer.tick(FPS)
    screen.fill("black")

    # track mouse position
    mouse = pygame.mouse.get_pos()

    # get left mouse action
    left = pygame.mouse.get_pressed()[0]  # tells us if left mouse button has been clicked (true or false)
    
    # mouse[0] = x, mouse[1] = y
    if left and mouse[1] > 70:
        painting.append((penColor, mouse, penSize))

    drawPainting(painting)

    if mouse[1] > 70:  # checking if the mouse is off of the menu (since we don't want to draw on the menu)
        pygame.draw.circle(screen, penColor, mouse, penSize)


    # drawing the toolbar
    brushes, color, rgbCode = draw_menu(penSize, penColor)

    # put the buttons on the screen
    clearButton.draw(screen)
    screenshotButton.draw(screen)


    for event in pygame.event.get():
        # exit the gui when the user presses the red X
        if event.type == pygame.QUIT:
            run = False

        if event.type == pygame.MOUSEBUTTONDOWN:  # this just means the mouse is being pressed down
            # draw the Button on the screen
            if clearButton.draw(screen): clearScreen()
            if screenshotButton.draw(screen): takeScreenshot()
            
            # check through the two lists to see if we clicked anyone of them
            for i in range(len(brushes)):
                # check if brush square at i is at the same point as the mouse press
                if brushes[i].collidepoint(event.pos):  # event.pos is an x,y coordinate
                    penSize = 15 - (i * 5)

            for i in range(len(color)):
                if color[i].collidepoint(event.pos):
                    penColor = rgbCode[i]


    
    pygame.display.flip()


pygame.quit()
