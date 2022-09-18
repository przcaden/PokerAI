

import os
import tkinter as tk
import random
import pygame

# Pair: two cards with the same value
# Flush: all cards have the same suit
# Straight: all cards are sequential
# Triple: all three cards have the same value
# Straight-flush: all cards are sequential and have the same suit

CARD_WIDTH = 100
CARD_HEIGHT = 150

# Card class has a value/face, suit, and can be face down
class Card:
    def __init__(self, value, suit, visible):
        self.suit = suit
        self.value = value
        self.visible = visible

# Generate random cards for the player and computer
def getRandomCards(card_value_list):
    vals = [] # random card index in deck
    p_cards = []
    c_cards = []

    for i in range(6):
        vals.append(random.randrange(52))
    # Create player cards
    for i in range(3):
        card_value = card_value_list[vals[i]]
        card_value_list.pop(vals[i]) # prevent card from being used again
        if i<2:
            p_cards.append(Card(card_value[0], card_value[1], True))
        else:
            p_cards.append(Card(card_value[0], card_value[1], False))
    # Create computer cards
    for i in range(3):
        card_value = card_value_list[vals[3+i]]
        card_value_list.pop(vals[i]) # prevent card from being used again
        if i<2:
            c_cards.append(Card(card_value[0], card_value[1], True))
        else:
            c_cards.append(Card(card_value[0], card_value[1], False))
    return (p_cards, c_cards)

def getCardSprites(p_cards, c_cards):
    p_sprites = []
    c_sprites = []
    for p in p_cards:
        if p.visible:
            img = pygame.image.load(os.path.join("assets", p.value+"_of_"+p.suit+".png"))
        else:
            img = pygame.image.load(os.path.join("assets/back.png"))
        img = pygame.transform.scale(img, (CARD_WIDTH, CARD_HEIGHT))
        p_sprites.append(img)
    for c in c_cards:
        if c.visible:
            img = pygame.image.load(os.path.join("assets", c.value+"_of_"+c.suit+".png"))
        else:
            img = pygame.image.load(os.path.join("assets/back.png"))
        img = pygame.transform.scale(img, (CARD_WIDTH, CARD_HEIGHT))
        c_sprites.append(img)
    return p_sprites, c_sprites
    

# Change card's image.
# Pass in card's value and its corresponding sprite
def editCard(card, s):
    img = pygame.image.load(os.path.join("assets", card.value + "_of_" + card.suit + ".png"))
    s.image = img

# Initialize GUI window
pygame.init()
pygame.display.set_caption("Poker")
win = pygame.display.set_mode((1000, 600))
FPS = 60

# Initialize fonts, labels, etc.
font = pygame.font.Font(None, 32)
mainlabel = font.render('Welcome to a completely fair game of Poker', True, (255,255,255))
secondlabel = font.render('Press start to begin', True, (255,255,255))
start_button = font.render('Start', True, (255,255,255))

def main():
    clock = pygame.time.Clock()
    run = False
    begin = True

    # Create a list of all possible suit/face values based on cards.txt
    card_value_list = [[]]
    data = open("cards.txt", "r")
    for d in data:
        d = d.strip()
        card_value = d.split("_of_")
        card_value_list.append(card_value)
    data.close()

    # Run following block if game is in main menu
    while not run:
        pygame.display.update()
        clock.tick(FPS)
        
        # Display labels and start button
        win.blit(mainlabel, (290, 250))
        win.blit(secondlabel, (400, 300))
        pygame.draw.rect(win, pygame.Color('green'), pygame.Rect(468, 380, 70, 40))
        win.blit(start_button, (475, 387, 70, 40))

        # Check for if player quit or if start button is clicked
        for event in pygame.event.get():
            if event.type == pygame.MOUSEBUTTONUP:
                pos = pygame.mouse.get_pos()
                if 398 <= pos[0] <= 538 and 340 <= pos[1] <= 420:
                    run = True
                if event.type == pygame.QUIT:
                    run = True

    # If game has started, run the else block
    while run:
        player_sprites = []
        cpu_sprites = []

        # Generate card objects for the player and computer
        (player_cards, cpu_cards) = getRandomCards(card_value_list)
        # Gather sprites based on card objects
        (player_sprites, cpu_sprites) = getCardSprites(player_cards, cpu_cards)

        # Run while game is being played
        while begin:
            pygame.display.update()
            clock.tick(FPS)
            
            # Display player cards on left, cpu cards on right
            for i in range(3):
                win.blit(player_sprites[i], (100+130*i, 100))
                win.blit(cpu_sprites[i], (100+130*i, 400))

            # Check for events caused by the player
            for event in pygame.event.get():
                if event.type == pygame.MOUSEBUTTONUP:
                    pos = pygame.mouse.get_pos()
                    # if bet_button.rect.collidepoint(pos):
                    #     begin = True
                    if event.type == pygame.QUIT:
                        begin = False

if __name__ == '__main__':
    main()