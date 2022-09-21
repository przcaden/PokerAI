

import os
import random
import pygame

# Pair: two cards with the same value
# Flush: all cards have the same suit
# Straight: all cards are sequential
# Triple: all three cards have the same value
# Straight-flush: all cards are sequential and have the same suit

# Dimensions for card sprites
CARD_WIDTH = 100
CARD_HEIGHT = 150

# Card class has a value/face, suit, and can be face down
class Card:
    def __init__(self, value, suit, visible):
        self.suit = suit
        self.value = value
        self.visible = visible

# Generate random card objects for the player and computer
def getRandomCards(card_value_list):
    vals = [] # random card index in deck
    p_cards = [] # holds card objects for player
    c_cards = [] # holds card objects for computer

    # Create random card values
    for i in range(6):
        vals.append(random.randrange(52))

    # Create player cards
    for i in range(3):
        p_card_value = card_value_list[vals[i]]
        c_card_value = card_value_list[vals[3+i]]

        # Prevent cards from being used again (in progress)
        # card_value_list.pop(vals[i])
        # card_value_list.pop(vals[2+i])

        if i<2:
            p_cards.append(Card(p_card_value[0], p_card_value[1], True))
            c_cards.append(Card(c_card_value[0], c_card_value[1], True))
        else:
            p_cards.append(Card(p_card_value[0], p_card_value[1], False))
            c_cards.append(Card(c_card_value[0], c_card_value[1], False))
    return (p_cards, c_cards)

# Load image based on the passed card's values.
# If the card is face down, load the back image. Otherwise load the actual card.
def loadImage(card):
    if card.visible:
        img = pygame.image.load(os.path.join("assets", card.value+"_of_"+card.suit+".png"))
    else:
        img = pygame.image.load(os.path.join("assets/back.png"))
    img = pygame.transform.scale(img, (CARD_WIDTH, CARD_HEIGHT))
    return img

##checks winners
def checkWinners(p_cards, c_cards, p_sprites, c_sprites):
    # we will first display the last card in both the computer and c- cards
    p_cards[2].visible = True 
    p_sprites[2] = loadImage(p_cards[2])

    c_cards[2].visible = True  #make all cards visible?
    c_sprites[2] = loadImage(c_cards[2])

    # TO-DO
    # we are  then going to check the cards and determine who's the winner
    # what are the conditions for when someone wins? 
    # have a rank based on the cards that they have
    # we will then display who the winner is.





# Generate lists of sprites for each player card and computer card.
# Indexes are in the same order.
def getCardSprites(p_cards, c_cards):
    p_sprites = []
    c_sprites = []
    for p in p_cards:
        img = loadImage(p)
        p_sprites.append(img)
    for c in c_cards:
        img = loadImage(c)
        c_sprites.append(img)
    return p_sprites, c_sprites

# Initialize GUI window
pygame.init()
pygame.display.set_caption("Poker")
win = pygame.display.set_mode((1000, 600))
FPS = 60

# Initialize fonts, labels, etc.
font = pygame.font.Font(None, 32)
mainlabel = font.render('Welcome to a completely fair game of Poker', True, (255,255,255))
secondlabel = font.render('Type a bet to begin', True, (255,255,255))
start_label = font.render('Bet', True, (255,255,255))
player_cards_label = font.render('Player\'s Cards', True, (255,255,255))
cpu_cards_label = font.render('Computer\'s Cards', True, (255,255,255))
bet_label = font.render('Raise Bet', True, (255,255,255))
fold_label = font.render('Fold', True, (255,255,255))

def main():
    clock = pygame.time.Clock()
    run = False
    begin = True
    bet_input = '$ '

    # Create a list of all possible suit/face values based on cards.txt
    card_value_list = [[]]
    data = open("cards.txt", "r")
    for d in data:
        d = d.strip()
        card_value = d.split("_of_")
        card_value_list.append(card_value)
    data.close()
    card_value_list.pop(0)

    # Run following block if game is in main menu
    while not run:
        pygame.display.update()
        clock.tick(FPS)
        
        # Display labels
        win.blit(mainlabel, (290, 250))
        win.blit(secondlabel, (400, 300))
        pygame.draw.rect(win, pygame.Color('green'), pygame.Rect(468, 380, 70, 40))
        pygame.draw.rect(win, pygame.Color('white'), pygame.Rect(431, 450, 140, 40))
        bet_surface = font.render(bet_input, True, (0,0,0))
        win.blit(bet_surface, (450, 460))
        win.blit(start_label, (483, 390, 70, 40))

        # Check for if player quit or if start button is clicked
        for event in pygame.event.get():
            if event.type == pygame.MOUSEBUTTONUP:
                pos = pygame.mouse.get_pos()
                if 398 <= pos[0] <= 538 and 340 <= pos[1] <= 420:
                    run = True
                if event.type == pygame.QUIT:
                    run = True
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_BACKSPACE:
                    bet_input = bet_input[:-1]
                elif len(bet_input)<8 and event.unicode.isnumeric():
                    bet_input += event.unicode

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
            win.fill(pygame.Color('black'))
            clock.tick(FPS)
            
            # Display player cards on left, cpu cards on right
            for i in range(3):
                win.blit(player_sprites[i], (100+130*i, 100))
                win.blit(cpu_sprites[i], (100+130*i, 400))

            # Display labels and buttons
            win.blit(player_cards_label, (200, 50))
            win.blit(cpu_cards_label, (180, 350))
            pygame.draw.rect(win, pygame.Color('green'), pygame.Rect(700, 380, 130, 40))
            pygame.draw.rect(win, pygame.Color('red'), pygame.Rect(728, 450, 70, 40))
            win.blit(bet_label, (715, 388))
            win.blit(fold_label, (740, 458))

            # Check for events caused by the player
            for event in pygame.event.get():
                if event.type == pygame.MOUSEBUTTONUP:
                    pos = pygame.mouse.get_pos()
                    # Check if fold button was clicked
                    if 650 <= pos[0] <= 798 and 410 <= pos[1] <= 490:
                        checkWinners(player_cards, cpu_cards, player_sprites, cpu_sprites)
                    if event.type == pygame.QUIT:
                        begin = False

if __name__ == '__main__':
    main()
