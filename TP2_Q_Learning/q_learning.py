import pygame
from config import *
import numpy as np
import random

def display_board(win, item_map_edit):
    mouse_img = pygame.image.load("mouse.png").convert_alpha()
    mouse_img = pygame.transform.scale(mouse_img, (200, 200))
    
    cheese_img = pygame.image.load("cheese.png").convert_alpha()
    cheese_img = pygame.transform.scale(cheese_img, (200, 200))
    
    cheese2_img = pygame.image.load("cheese2.png").convert_alpha()
    cheese2_img = pygame.transform.scale(cheese2_img, (200, 200))
    
    cheese3_img = pygame.image.load("cheese3.png").convert_alpha()
    cheese3_img = pygame.transform.scale(cheese3_img, (200, 200))

    poison_img = pygame.image.load("poison.png").convert_alpha()
    poison_img = pygame.transform.scale(poison_img, (200, 200))

    for y in range(0, item_map_edit.shape[0]):
        for x in range(0, item_map_edit.shape[1]):
            if (item_map_edit[y][x] == "M"):
                win.blit(mouse_img, position_map[y][x])
            elif (item_map_edit[y][x] == "C1"):
                win.blit(cheese_img, position_map[y][x])
            elif (item_map_edit[y][x] == "C2"):
                win.blit(cheese2_img, position_map[y][x])
            elif (item_map_edit[y][x] == "C3"):
                win.blit(cheese3_img, position_map[y][x])
            elif (item_map_edit[y][x] == "P"):
                win.blit(poison_img, position_map[y][x])


def  create_Q_table():  # create q table with zeros and size 
    q_table = np.zeros((6, 4)) #  number of states, number of actions
    return q_table

def choose_random(item_map_edit, x, y):
    x, y = np.where(item_map_edit == "M")
    while (True):
        action = random.choice(action_list)
        if  action == "R" and x + 1 < 3:
            return "R"     
        elif action  == "L" and x - 1 > 0:
            return "L"
        elif action == "T" and y - 1 > 0:
            return "T"
        elif action == "B" and y + 1 < 3:
            return "B"


def choose_action():
    if np.random.rand() < epsilon:
        return (choose_random())
     #else
        


def event_loop():
    for event in pygame.event.get():
        if event.type == pygame.QUIT:     
            exit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                exit()

if __name__ == "__main__":
    pygame.init()
    win = pygame.display.set_mode((1200, 800))
    background_img = pygame.image.load("background_img.png").convert()
    reward = 0
    score_map_edit = score_map
    item_map_edit = item_map
    q_table = create_Q_table()
    epsilon = 1 # exploration rate
    

    while True:
        win.blit(background_img, (0,0))
        display_board(win, item_map_edit)


        epsilon = epsilon * 0.995
        epsilon = max(epsilon, 0.05)
        pygame.display.flip()
        event_loop()
