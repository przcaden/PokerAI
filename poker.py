

import os
import tkinter as tk
import random
import pygame

# Pair: two cards with the same value
# Flush: all cards have the same suit
# Straight: all cards are sequential
# Triple: all three cards have the same value
# Straight-flush: all cards are sequential and have the same suit

# Card class has a value/face, suit, and can be face down
class Card:
    def __init__(self, value, suit, visible):
        self.suit = suit
        self.value = value
        self.visible = visible

# Obtain a random card, removing it from the deck
def getRandomCard(card_value_list, visible):
    val = random.randrange(52)
    card_value = card_value_list(val)
    card_value_list.pop(val)
    c = Card(card_value[0], card_value[1], visible)
    return c

# Change card's image.
# Pass in card's value and its corresponding sprite
def editCard(card, s):
    img = pygame.image.load(os.path.join("assets/", card.value, "_of_", card.suit, ".png"))
    s.image = img

# Initialize GUI window
pygame.init()
pygame.display.set_caption("Poker")
win = pygame.display.set_mode((1000, 800))
FPS = 60

def main():
    clock = pygame.time.Clock()
    begin = False

    # Create a list of all possible suit/face values based on cards.txt
    card_value_list = [[]]
    data = open("cards.txt", "r")
    for d in data:
        card_value = d.split("_of_")
        card_value_list.append(card_value)
    data.close()

    font = pygame.font.Font(None, 32)
    mainlabel = font.render('Welcome to a completely fair game of Poker', True, (255,255,255))
    secondlabel = font.render('Press start to begin', True, (255,255,255))
    start_button = font.render('Start', True, (255,255,255))

    print('hello')
    # Run following block if game is in main menu
    while not begin:
        pygame.display.update()
        clock.tick(FPS)
        
        win.blit(mainlabel, (300, 250))
        win.blit(secondlabel, (400, 300))
        pygame.draw.rect(win, pygame.Color('green'), pygame.Rect(430, 380, 140, 40))
        win.blit(start_button, (430, 380, 140, 40))

        for event in pygame.event.get():
            if event.type == pygame.MOUSEBUTTONUP:
                pos = pygame.mouse.get_pos()
                print(pos)
                if 800 <= pos[0] <= 940 and 250 <= pos[1] <= 290:
                    begin = True
                if event.type == pygame.QUIT:
                    pygame.quit()
    print('jizz')
    player_cards = []
    player_card_sprites = []
    for i in range(3):
        player_cards.append(getRandomCard(card_value_list, False))
        player_card_sprites.append(pygame.sprite())
        editCard(player_cards[i], player_card_sprites[i])
        player_card_sprites[i].pack()

    # If game has started, run the else block
    while begin:
        pygame.display.update()
        clock.tick(FPS)
        # Get three random cards for the player
        
        for event in pygame.event.get():
            if event.type == pygame.MOUSEBUTTONUP:
                pos = pygame.mouse.get_pos()
                # if bet_button.rect.collidepoint(pos):
                #     begin = True
                if event.type == pygame.QUIT:
                    pygame.quit()

if __name__ == '__main__':
    main()