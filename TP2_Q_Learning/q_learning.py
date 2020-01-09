from time import sleep

import pygame
import numpy as np
import random

from config import score_map, item_map, actions, position_map, action_text
from fix_me import *

#### GRAPHICAL PYGAME FUNCTION
def display_board(win, item_map_edit, posX, posY, background_img):
    win.fill((0, 0, 0))
    win.blit(background_img, (0, 0))

    mouse_img = pygame.image.load("images/mouse.png").convert_alpha()
    mouse_img = pygame.transform.scale(mouse_img, (100, 100))

    cheese_img = pygame.image.load("images/cheese.png").convert_alpha()
    cheese_img = pygame.transform.scale(cheese_img, (100, 100))

    cheese2_img = pygame.image.load("images/cheese2.png").convert_alpha()
    cheese2_img = pygame.transform.scale(cheese2_img, (100, 100))

    cheese3_img = pygame.image.load("images/cheese3.png").convert_alpha()
    cheese3_img = pygame.transform.scale(cheese3_img, (100, 100))

    poison_img = pygame.image.load("images/poison.png").convert_alpha()
    poison_img = pygame.transform.scale(poison_img, (100, 100))

    for y in range(0, len(item_map_edit[0])):
        for x in range(0, len(item_map_edit[1])):
            if (item_map_edit[y][x] == "C1"):
                win.blit(cheese_img, position_map[y][x])
            elif (item_map_edit[y][x] == "C2"):
                win.blit(cheese2_img, position_map[y][x])
            elif (item_map_edit[y][x] == "C3"):
                win.blit(cheese3_img, position_map[y][x])
            elif (item_map_edit[y][x] == "P"):
                win.blit(poison_img, position_map[y][x])
    win.blit(mouse_img, position_map[posY][posX])


def display_info(x, y, q_table, r, epochs, action, epsilon):
    font = pygame.font.SysFont("arial", 24)
    textEpochs = font.render("Epochs: " + str(epochs), True, (255, 255, 255), None)
    textPos = font.render("X: " + str(x) + "  Y" + str(y), True, (255, 255, 255), None)
    textEpsilon = font.render("Exploration Rate (epsilon): " + "{:.4f}".format(epsilon), True, (255, 255, 255), None)
    textAction = font.render("Action: " + action_text[action], True, (255, 255, 255), None)
    textReward = font.render("Reward: " + str(r), True, (255, 255, 255), None)



    h = 500
    w = 1000
    for i in range(0, q_table.shape[0]):
        for j in range(0, q_table.shape[1]):
            rd = font.render("{:.4f}".format(q_table[i][j]), True, (255, 255, 255))
            win.blit(rd, (w, h))
            w += 70
        h += 30
        w = 1000

    win.blit(textEpochs, (1000, 50))
    win.blit(textEpsilon, (1000, 100))
    win.blit(textPos, (1000, 200))
    win.blit(textReward, (1000, 300))
    win.blit(textAction, (1000, 400))

    pygame.display.flip()


def event_loop():
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            exit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                exit()


def reset():
    x = 0
    y = 0
    score_map_edit = np.copy(score_map)
    item_map_edit = np.copy(item_map)
    return x, y, y * 3 + x * 1, score_map_edit, item_map_edit


###########  DO NOT TOUCH ABOVE ############

def is_alive(score_map_edit, x, y):
    done = False
    if score_map_edit[y][x] == 10:
        done = True
    return done


def step(action, x, y, score_map_edit, item_map_edit):
    reward = 0
    y = max(0, min(y + actions[action][0], 2))
    x = max(0, min(x + actions[action][1], 2))

    done = is_alive(score_map_edit, x, y)
    if score_map_edit[y][x] != 0:
        reward = score_map_edit[y][x]
        score_map_edit[y][x] = 0
        item_map_edit[y][x] = "0"
    return x, y, (y * 3 + x * 1), reward, done, score_map_edit

if __name__ == "__main__":
    ### pygame
    pygame.init()
    win = pygame.display.set_mode((1400, 900))
    background_img = pygame.image.load("images/background_img.png").convert()

    reward = 0
    Gamma = 0.9  # next action impact
    epsilon = 1  # exploration rate

    q_table = create_Q_table()

    for epochs in range(100):
        done = False
        x, y, state, score_map_edit, item_map_edit = reset()
        it = 15
        while done == False:
            display_board(win, item_map_edit, x, y, background_img)
            event_loop()

            ## Choose An action
            action = choose_action(state, q_table, epsilon)

            x, y, stateNext, reward, done, score_map_edit = step(action, x, y, score_map_edit, item_map_edit)

            # Use Q Table to choose nextAction
            actionNext = choose_action(stateNext, q_table, 0.0)

            # Update Q function
            q_table = update(q_table, state, action, reward, Gamma, stateNext, actionNext)

            state = stateNext
            it = it - 1
            if it == 0:
                break
            epsilon = reduce_epsilon(epsilon)
            display_info(x, y, q_table, reward, epochs, action, epsilon)

            # Uncomment to wait after each action
            # sleep(0.1)
