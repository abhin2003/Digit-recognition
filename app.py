import pygame
import sys
from pygame.locals import *
import numpy as np
from keras.models import load_model
import cv2

WINDOWSIZEX = 640
WINDOWSIZEY = 480

BOUNDARYINC = 5  # Fixed typo: BOUNDRYINC -> BOUNDARYINC

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)

IMAGESAVE = False
PREDICT = True  # Added missing variable

image_cnt = 1

MODEL = load_model("bestmodel.h5")

LABELS = {0: "Zero", 1: "One", 2: "Two", 3: "Three", 4: "Four", 
          5: "Five", 6: "Six", 7: "Seven", 8: "Eight", 9: "Nine"}

# Initialize pygame
pygame.init()
FONT = pygame.font.Font(None, 36)  # Fixed: removed quotes around None, increased size

# Create the window
DISPLAYSURF = pygame.display.set_mode((WINDOWSIZEX, WINDOWSIZEY))
pygame.display.set_caption("Digit Recognition")

# Fill initial background
DISPLAYSURF.fill(BLACK)

iswriting = False  # Fixed typo: iswritting -> iswriting
number_xcord = []
number_ycord = []

# Main loop
while True:
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()

        if event.type == MOUSEMOTION and iswriting:
            xcord, ycord = event.pos
            pygame.draw.circle(DISPLAYSURF, WHITE, (xcord, ycord), 4, 0)
            number_xcord.append(xcord)
            number_ycord.append(ycord)

        if event.type == MOUSEBUTTONDOWN:
            iswriting = True

        if event.type == MOUSEBUTTONUP:
            iswriting = False
            
            if len(number_xcord) > 0 and len(number_ycord) > 0:  # Check if we have drawn something
                # Fixed variable names and sorting
                number_xcord_sorted = sorted(number_xcord)
                number_ycord_sorted = sorted(number_ycord)

                # Fixed variable names and boundary calculation
                rect_min_x = max(number_xcord_sorted[0] - BOUNDARYINC, 0)
                rect_max_x = min(WINDOWSIZEX, number_xcord_sorted[-1] + BOUNDARYINC)
                rect_min_y = max(number_ycord_sorted[0] - BOUNDARYINC, 0)
                rect_max_y = min(WINDOWSIZEY, number_ycord_sorted[-1] + BOUNDARYINC)

                # Clear coordinate arrays
                number_xcord = []
                number_ycord = []

                # Fixed array extraction - corrected syntax
                img_arr = np.array(pygame.PixelArray(DISPLAYSURF))[rect_min_x:rect_max_x, rect_min_y:rect_max_y].T.astype(np.float32)

                if IMAGESAVE:
                    cv2.imwrite(f"image_{image_cnt}.png", img_arr)  # Fixed: added filename and format
                    image_cnt += 1

                if PREDICT:
                    # Fixed variable name: imge_ar -> img_arr
                    image = cv2.resize(img_arr, (28, 28))
                    image = np.pad(image, (10, 10), 'constant', constant_values=0)  # Fixed: constant_value -> constant_values
                    image = cv2.resize(image, (28, 28)) / 255

                    # Predict the digit
                    prediction = MODEL.predict(image.reshape(1, 28, 28, 1))
                    label = str(LABELS[np.argmax(prediction)])

                    # Display the prediction
                    textSurface = FONT.render(label, True, RED, WHITE)
                    textRecObj = textSurface.get_rect()  # Fixed: testing -> textSurface
                    textRecObj.left, textRecObj.bottom = rect_min_x, rect_max_y

                    DISPLAYSURF.blit(textSurface, textRecObj)

        # Fixed: moved KEYDOWN outside of MOUSEBUTTONUP
        if event.type == KEYDOWN:
            if event.unicode == "n":
                DISPLAYSURF.fill(BLACK)

    pygame.display.update()