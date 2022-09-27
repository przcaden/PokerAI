import os
import random
import pygame
import time

# Pair: two cards with the same value
# Flush: all cards have the same suit
# Straight: all cards are sequential
# Triple: all three cards have the same value
# Straight-flush: all cards are sequential and have the same suit
# Order of cards: Ace, King, Queen, Jack, Numbers

# Dimensions for card sprites
CARD_WIDTH = 100
CARD_HEIGHT = 150

CPU_MAX_BET_AMOUNT = 5000


# Card class has a value/face, suit, and can be face down
class Card:
    _cards = []
    def __init__(self, value, suit, visible, face):
        self._cards.append(self);
        self.suit = suit
        self.value = value
        self.face = face
        self.visible = visible

# Generate random card objects for the player and computer
# Pre: list of tuples is generated for each card. i.e., (king, hearts)
# Post: two random lists of three cards are generated for the player and computer
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

        if p_card_value[0] == "ace":
            p_val = 14
        elif p_card_value[0] == "king":
            p_val = 13
        elif p_card_value[0] == "queen":
            p_val = 12
        elif p_card_value[0] == "jack":
            p_val = 11
        else:
            p_val = int(p_card_value[0])

        if c_card_value[0] == "ace":
            c_val = 14
        elif c_card_value[0] == "king":
            c_val = 13
        elif c_card_value[0] == "queen":
            c_val = 12
        elif c_card_value[0] == "jack":
            c_val = 11
        else:
            c_val = int(c_card_value[0])

        if i<2:
            p_cards.append(Card(p_val, p_card_value[1], True, p_card_value[0]))
            c_cards.append(Card(c_val, c_card_value[1], True, c_card_value[0]))
        else:
            p_cards.append(Card(p_val, p_card_value[1], False, p_card_value[0]))
            c_cards.append(Card(c_val, c_card_value[1], False, c_card_value[0]))
    return (p_cards, c_cards)

# Load image based on the passed card's values.
# If the card is face down, load the back image. Otherwise load the actual card.
# Pre: card object is generated
# Post: corresponding image is loaded for the card object
def loadImage(card):
    if card.visible:
        img = pygame.image.load(os.path.join("assets", str(card.face)+"_of_"+card.suit+".png"))
    else:
        img = pygame.image.load(os.path.join("assets/back.png"))
    img = pygame.transform.scale(img, (CARD_WIDTH, CARD_HEIGHT))
    return img

def refreshImages(p_cards, c_cards, p_sprites, c_sprites):
    for i in range(3):
        p_sprites[i] = loadImage(p_cards[i])
        c_sprites[i] = loadImage(c_cards[i])


def check_pair_or_triple(cards):
    #loop through the different hands
    count = 0
    if cards[0].value == cards[1].value or cards[2].value == cards[1].value or cards[0].value == cards[2].value:
        count = 2
    elif cards[0].value == cards[1].value and cards[1].value == cards[2].value:
        count = 3
    return count

def check_straight(cards):
    if cards[0].value > cards[1].value > cards[2].value:
        return True
    elif cards[0].value < cards[1].value < cards[2].value:
        return True
    else: return False


def check_flush(cards):
    # a flush exists when all the cards are in the same suit
    if cards[0].suit == cards[1].suit and cards[1].suit == cards[2].suit:
        return True
    else: return False


#dhecks all the  hands the user or computer has
def checkAllHands(cards):
     #when it is a straight-flush.
    if check_straight(cards) == True and check_flush(cards) == True:
        return "straight-flush"
    #when there is a straight
    elif check_straight(cards) == True:
        return "straight"
    # when there is a flush
    elif check_flush(cards) == True:
        return "flush"
        # when there is a triple
    elif check_pair_or_triple(cards) == 3:
        return "triple"
    # when  a pair exists
    if check_pair_or_triple(cards) == 2:
        return "pair"
    else: return "none"


#checkrank of hands
def checkCardRanks(cards):
     # create a dictionary that has all the possible hands with their ranks
    poker_ranks = { "none": 0, "pair": 1, "flush": 2, "straight": 3, "triple": 4, "straight-flush": 5 }
    #we will then get hands and compare
    for key, value in poker_ranks.items():
        #if the hand is the same as the key, then we want to return the ranks
        if checkAllHands(cards) == key:
            # print('this is the rank', value)
            return value


#checks winners
def checkWinners(p_cards, c_cards, p_sprites, c_sprites):
    # we will first display the last card in both the computer and c- cards
    p_cards[2].visible = True 
    p_sprites[2] = loadImage(p_cards[2])

    c_cards[2].visible = True  #make all cards visible?
    c_sprites[2] = loadImage(c_cards[2])

    #check rank of computer and user hands and determine the winner
    p_rank = checkCardRanks(p_cards)
    c_rank = checkCardRanks(c_cards)

    print('player hand rank: ' + str(p_rank))
    print('cpu hand rank: ' + str(c_rank))

    if p_rank == c_rank:
        p_top = 0
        c_top = 0
        for i in range(3):
            if p_cards[i].value > p_top:
                p_top = p_cards[i].value
            if c_cards[i].value > c_top:
                c_top = c_cards[i].value
            if p_top > c_top:
                print('same hand, player won')
                return 0
            elif p_top < c_top:
                print('same hand, cpu won')
                return 1
            else:
                print('same hand, split pot')
                return 2
    elif p_rank > c_rank:
        print('player won')
        return 0
    else:
        print('cpu won')
        return 1
        

# Decion-making AI function. Runs after each turn is ended by the player.
# Pre: user has decided to raise their bet for their turn
# Post: the function will decide whether to fold, match the user's bet, or match and raise above the bet.
#       function will return -1 if deciding to fold
#       function will return 0 if deciding to match the bet
#       otherwise, the function will return a number indicating how much to raise above the player's bet.
def makeComputerDecision(p_cards, c_cards, c_bet):
    p_hand = checkAllHands(p_cards)
    c_hand = checkAllHands(c_cards)

    # Fold if player has bet more than allowed by the cpu (might change later)
    # if p_bet >= CPU_MAX_BET_AMOUNT:
    #     return -1
    print('player hand: ' + p_hand)
    print('cpu hand: ' + c_hand)
    # Decision making for when the player has a pair.
    if p_hand == "none":
        if c_hand == "none":
            c_cards[2].value = c_cards[0].value
            return determineRaiseAmount(c_bet)
        else: return determineRaiseAmount(c_bet)
    if p_hand == "pair":
        # If the CPU has a worse hand, change its face down card
        if c_hand == "none":
            if c_cards[0].value > c_cards[1].value:
                c_cards[2].value = c_cards[0].value
            else: c_cards[2].value = c_cards[1].value
            return 0
        if c_hand == "pair":
            # Try to change to triple
            if c_cards[0].value == c_cards[1].value:
                c_cards[2].value == c_cards[1].value
                return determineRaiseAmount(c_bet)
            # Try to change to flush
            elif c_cards[0].suit == c_cards[1].suit:
                c_cards[2].suit == c_cards[1].suit
                return determineRaiseAmount(c_bet)
            # If cheating is not possible, match user's bet
            else: return 0
        # If CPU has a better hand, raise above user's bet
        else: return determineRaiseAmount(c_bet)

    # Make decision for when the player has a flush.
    elif p_hand == "flush":
        # Check if the computer has a worse hand (cheat)
        if c_hand == "none":
            # Change computer's hand to a flush if possible
            if c_cards[0].value == c_cards[1].value-1:
                c_cards[2].value = c_cards[1].value+1
                return 0
            elif c_cards[0].value == c_cards[1].value+1:
                c_cards[2].value = c_cards[1].value-1
                return 0
            # Fold if discreet cheating is not possible
            else: return -1
        elif c_hand == "pair":
            # If the two face up cards are a pair, change the third to make a triple
            if c_cards[0].value == c_cards[1].value:
                c_cards[2].value == c_cards[1].value
                return determineRaiseAmount(c_bet)
        elif c_hand == "flush":
            # Check if hand can be made sequential (try to straight-flush)
            if c_cards[0].value == c_cards[1].value-1:
                c_cards[2].value = c_cards[1].value+1
                return determineRaiseAmount(c_bet)
            elif c_cards[0].value == c_cards[1].value+1:
                c_cards[2].value = c_cards[1].value-1
                return determineRaiseAmount(c_bet)
            # Check if hand can be made into triple
            elif c_cards[0].value == c_cards[1].value:
                c_cards[2].value == c_cards[1].value
                return determineRaiseAmount(c_bet)
            # Match user's raise if cheating is not possible
            else: return 0
        # If computer has a better hand, raise above player's bet
        else: return determineRaiseAmount(c_bet)

    # Make decision for when the player has a straight.
    elif p_hand == "straight":
        if c_hand == "pair":
            # Try to change to triple
            if c_cards[0].value == c_cards[1].value:
                c_cards[2].value == c_cards[1].value
                return determineRaiseAmount(c_bet)
            else: return -1
        elif c_hand == "flush":
            # Try to get straight-flush
            if c_cards[0].value == c_cards[1].value-1:
                c_cards[2].value = c_cards[1].value+1
                return determineRaiseAmount(c_bet)
            else: return -1
        elif c_hand == "straight":
            # Try to get straight-flush
            if c_cards[0].suit == c_cards[1].suit:
                c_cards[2].suit == c_cards[1].suit
            else: return 0
        else: return determineRaiseAmount(c_bet)

    # Make decision for when the player has a triple.
    elif p_hand == "triple":
        if c_hand == "straight-flush":
            return determineRaiseAmount(c_bet)
        elif c_hand == "triple":
            return 0
        else: return -1

    # Make decision for when the player has a straight-flush.
    elif p_hand == "straight-flush":
        if c_hand == "straight-flush":
            return 0
        else: return -1

# Determine how much the CPU should raise above player's bet
def determineRaiseAmount(c_bet):
    if c_bet + 50 > CPU_MAX_BET_AMOUNT:
        return CPU_MAX_BET_AMOUNT - c_bet
    return 50

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
smallfont = pygame.font.Font(None, 24)
mainlabel = font.render('Welcome to a completely fair game of Poker', True, (255,255,255))
secondlabel = font.render('Type a bet to begin', True, (255,255,255))
start_label = font.render('Bet', True, (255,255,255))
player_cards_label = font.render('Player\'s Cards', True, (255,255,255))
cpu_cards_label = font.render('Computer\'s Cards', True, (255,255,255))
bet_label = font.render('Raise Bet', True, (255,255,255))
fold_label = font.render('Fold', True, (255,255,255))
yes_label = font.render('Yes', True, (255,255,255))
no_label = font.render('No', True, (255,255,255))

# Main game function. Displays all GUI components and runs game logic functions.
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

        if time.time() % 1 > 0.5:
            text_rect = bet_surface.get_rect()
            cursor = pygame.Rect((text_rect.topright[0]+452,text_rect.topright[1]+458), (3, text_rect.height + 2))
            pygame.draw.rect(win, pygame.Color('black'), cursor)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                    pygame.quit()
            # Check if user clicked bet button
            if event.type == pygame.MOUSEBUTTONUP and len(bet_input) > 2:
                pos = pygame.mouse.get_pos()
                if 468 <= pos[0] <= 538 and 380 <= pos[1] <= 420:
                    run = True
            # Check if user types into box
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_BACKSPACE and len(bet_input) > 2:
                    bet_input = bet_input[:-1]
                elif len(bet_input)<8 and event.unicode.isnumeric():
                    bet_input += event.unicode

    player_winnings = 0
    cpu_winnings = 0

    # If game has started, run the else block
    while run:
        begin = True
        player_sprites = []
        cpu_sprites = []
        turnEnded = False
        cpu_bet = int(bet_input[2:])
        player_bet = int(bet_input[2:])
        bet_raise = '+$ '
        game_status = ''
        winner = -1
        win_msg = ''

        # Generate card objects for the player and computer
        (player_cards, cpu_cards) = getRandomCards(card_value_list)
        # Gather sprites for card objects
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

            # Display general labels
            win.blit(player_cards_label, (200, 50))
            win.blit(cpu_cards_label, (180, 350))
            plabel = font.render('Player Bet Amount: $'+str(player_bet), True, (255,255,255))
            clabel = font.render('CPU Bet Amount: $'+str(cpu_bet), True, (255,255,255))
            win.blit(plabel, (630, 60))
            win.blit(clabel, (630, 110))
            game_status_label = font.render(game_status, True, pygame.Color('red'))
            win.blit(game_status_label, (630, 200))
            if player_winnings > 0 or cpu_winnings > 0:
                p_winnings_label = smallfont.render('Player winnings: $' + str(player_winnings), True, (255,255,255))
                c_winnings_label = smallfont.render('CPU winnings: $' + str(cpu_winnings), True, (255,255,255))
                win.blit(p_winnings_label, (500, 550))
                win.blit(c_winnings_label, (500, 570))

            # Display the following labels if the deal is ongoing
            if winner == -1:
                if turnEnded:
                    pygame.draw.rect(win, pygame.Color('gray'), pygame.Rect(700, 330, 130, 40))
                else:
                    pygame.draw.rect(win, pygame.Color('green'), pygame.Rect(700, 330, 130, 40))
                
                pygame.draw.rect(win, pygame.Color('red'), pygame.Rect(728, 460, 70, 40))
                win.blit(bet_label, (715, 338))
                win.blit(fold_label, (740, 468))

                # Display text box and cursor
                pygame.draw.rect(win, pygame.Color('white'), pygame.Rect(694, 385, 140, 40))
                raise_text_surface = font.render(bet_raise, True, (0,0,0))
                win.blit(raise_text_surface, (709, 393))
                if time.time() % 1 > 0.5 and turnEnded == False:
                    text_rect = raise_text_surface.get_rect()
                    cursor = pygame.Rect((text_rect.topright[0]+711,text_rect.topright[1]+391), (3, text_rect.height + 2))
                    pygame.draw.rect(win, pygame.Color('black'), cursor)

            # Display the following labels if the deal has ended
            else:
                win_msg_surface = font.render(win_msg, True, (255,255,255))
                win.blit(win_msg_surface, (600, 280))
                pygame.draw.rect(win, pygame.Color('green'), pygame.Rect(730, 330, 80, 40))
                pygame.draw.rect(win, pygame.Color('red'), pygame.Rect(620, 330, 80, 40))
                win.blit(yes_label, (750, 340))
                win.blit(no_label, (645, 340))

            # Check for events caused by the player
            for event in pygame.event.get():
                if event.type == pygame.MOUSEBUTTONUP:
                    pos = pygame.mouse.get_pos()
                    # Check if in-game buttons were clicked
                    if winner == -1:
                        # Check if fold button was clicked
                        if 728 <= pos[0] <= 798 and 460 <= pos[1] <= 500:
                            winner = checkWinners(player_cards, cpu_cards, player_sprites, cpu_sprites)
                            print('win value: ' + str(winner))
                            turnEnded = True
                            bet_raise = '+$ '
                            if winner == 0:
                                win_msg = 'You won! Deal again?'
                                player_winnings += player_bet
                            elif winner == 1:
                                win_msg = 'CPU won. Deal again?'
                                cpu_winnings += cpu_bet
                            else:
                                win_msg = 'Tie, split pot. Deal again?'
                                player_winnings += player_bet
                                cpu_winnings += cpu_bet
                        # Check if bet button was clicked; if so, run AI decisionmaking
                        if 700 <= pos[0] <= 830 and 330 <= pos[1] <= 370 and turnEnded == False and len(bet_raise) > 3:
                            player_bet += int(bet_raise[3:])
                            bet_raise = '+$ '
                            decision = makeComputerDecision(player_cards, cpu_cards, cpu_bet)
                            refreshImages(player_cards, cpu_cards, player_sprites, cpu_sprites)

                            # Change bet and conditions based on what decision was made.
                            print('decision: ' + str(decision))
                            if decision == -1:
                                turnEnded = True
                                game_status = 'CPU folded.'
                                winner = checkWinners(player_cards, cpu_cards, player_sprites, cpu_sprites)
                                print('win value: ' + str(winner))
                                turnEnded = True
                                bet_raise = '+$ '
                                if winner == 0:
                                    win_msg = 'You won! Deal again?'
                                    player_winnings += player_bet
                                elif winner == 1:
                                    win_msg = 'CPU won. Deal again?'
                                    cpu_winnings += cpu_bet
                                else:
                                    win_msg = 'Tie, split pot. Deal again?'
                                    player_winnings += player_bet
                                    cpu_winnings += cpu_bet
                            elif decision == 0:
                                cpu_bet = player_bet
                                game_status = 'CPU matched your bet.'
                            else:
                                cpu_bet = player_bet + decision
                                game_status = 'CPU raised above your bet.'

                    # Check if buttons were clicked when game over screen is displayed
                    else:
                        # Check if yes button was clicked; if so, restart deal
                        if 730 <= pos[0] <= 810 and 330 <= pos[1] <= 370:
                            begin = False
                        # Check if no button was clicked; if so, close window
                        if 620 <= pos[0] <= 700 and 330 <= pos[1] <= 370:
                            begin = False
                            run = False
                # Check if user types into box
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_BACKSPACE and len(bet_raise) > 3:
                        bet_raise = bet_raise[:-1]
                    elif len(bet_raise) < 8 and event.unicode.isnumeric() and turnEnded == False:
                        bet_raise += event.unicode
                # Check if player closed the game
                if event.type == pygame.QUIT:
                    pygame.quit()

if __name__ == '__main__':
    main()
