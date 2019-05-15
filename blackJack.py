import random

suits = ('Hearts', 'Diamonds', 'Spades', 'Clubs')

ranks = ('Two', 'Three', 'Four', 'Five', 'Six', 'Seven', 'Eight', 'Nine', 'Ten', 'Jack', 'Queen', 'King', 'Ace')

values = {'Two': 2, 'Three':3, 'Four':4, 'Five':5, 'Six':6, 'Seven':7, 'Eight':8, 'Nine':9, 'Ten':10, 'Jack':10, 'Queen':10, 'King':10, 'Ace':11}

playing = True

class Card():

    def __init__(self, suit, rank):
        self.suit = suit 
        self.rank = rank
        
    def __str__(self):
        return self.rank +" of "+ self.suit

class Deck():
    
    def __init__(self):
        self.deck = []
        for suit in suits:
            for rank in ranks:
                self.deck.append(Card(suit, rank))
    
    def __str__(self):
        deck_string = ''
        for card in self.deck:
            deck_string += '\n' + card.__str__()
        return "The deck has:" + deck_string
    
    def __len__(self):
        return len(self.deck)
    

    def shuffle(self):
        random.shuffle(self.deck)
        
    def deal(self):
        return self.deck.pop(0)

class Hand():

    def __init__(self):
        self.cards = []
        self.value = 0
        self.aces = 0
        
    def add_card(self, card):
        self.cards.append(card)
        self.value += values[card.rank]
        
        #track aces
        if card.rank == 'Ace':
            self.aces += 1
            
    def adjust_for_ace(self):
        while (self.value > 21) and (self.aces):
            self.value -= 10
            self.aces -= 1

class Chips:
    
    def __init__(self, total = 100):
        self.total = 100 
        self.bet = 0
        
    def win_bet(self):
        self.total += self.bet
        
    def lose_bet(self):
        self.total -= self.bet

def take_bet(chips):
    while True:
        try:
            chips.bet = int(input(f"Place your bet, maximum({chips.total}): "))
        except:
            print("Whoops! That was not a valid bet \nPlease try again")
        else:
            if chips.bet > chips.total:
                print(f"Whoops! Bet can't be more than {player_chips.total} \nPlease try again")
                continue
            else:
                print(f"Thank you, your bet is: {chips.bet}")
                break

def hit(deck, hand):

    single_card = deck.deal()
    hand.add_card(single_card)
    hand.adjust_for_ace()

def hit_or_stand(deck,hand):
    global playing  # to control an upcoming while loop
    
    while True:
        decision = input("Hit or Stand?: ")
        decision = decision.lower()
        if (decision != 'hit') and (decision != 'stand'):
            print("Whoops! \nPlease try again")
            continue
        elif decision == 'hit':
            hit(deck, hand)
            break
        else:
            playing = False
            break

def player_busts(player, dealer, chips):
    print("BUST PLAYER")
    chips.lose_bet()

def player_wins(player, dealer, chips):
    print("PLAYER WINS!")
    chips.win_bet()

def dealer_busts(player, dealer, chips):
    print("PLAYER WINS! DEALER BUSTED!")
    chips.win_bet()

def dealer_wins(player, dealer, chips):
    print("DEALER WINS!")
    chips.lose_bet()

def push(player, dealer):
    print("Dealer and player tie! Push")

def show_some(player, dealer):

    print("DEALER'S HAND:")
    print("one card hidden!")
    print(dealer.cards[1])
    print("\n")
    print("PLAYER HAND:")
    for card in player.cards:
        print(card)
    print(f"PLAYER HAND VALUE: \n{player.value}")
    

def show_all(player, dealer):

    print("DEALERS HAND:")
    for card in dealer.cards:
        print(card)
    print(f"DEALER HAND VALUE: \n{dealer.value}")
    print("\n")
    print("PLAYER HAND:")
    for card in player.cards:
        print(card)
    print(f"PLAYER HAND VALUE: \n{player.value}")

#Print an opening statement
print("WELCOME TO BLACKJACK")

#Set up the Player's chips
player_chips = Chips()

#GAME PLAY:
while True:

    #Create and shuffle the deck
    deck = Deck()
    deck.shuffle()

    player = Hand()
    player.add_card(deck.deal())
    player.add_card(deck.deal())

    dealer = Hand()
    dealer.add_card(deck.deal())
    dealer.add_card(deck.deal())


    #Prompt the player for their bet
    take_bet(player_chips)

    #show cards (but keep one dealer card hidden)
    show_some(player, dealer)

    while playing:
        #Prompt for Player to hit or stand
        hit_or_stand(deck, player)

        #Show cards (but keep one dealer card hidden)
        show_some(player, dealer)

        #if player's hand exceeds 21, run player_busts() and break out of loop
        if player.value > 21:
            break

        #if player hasn't busted, play dealer's hand until dealer reaches 17
    if player.value <= 21:

        while dealer.value < 17:
            hit(deck,dealer)

    #Show all cards
    show_all(player,dealer)

    #Run different winning scenarios
    if dealer.value > 21:
        dealer_busts(player,dealer,player_chips)
    elif player.value > 21:
        player_busts(player,dealer,player_chips)
    elif (dealer.value > player.value) and (dealer.value <= 21):
        dealer_wins(player,dealer,player_chips)
    elif (player.value > dealer.value) and (player.value <= 21):
        player_wins(player,dealer,player_chips)
    else:
        push(player,dealer)

    # Inform Player of their chips total
    print(f"\nPlayer's total chips: {player_chips.total}")
    
    if player_chips.total == 0:
        print("Whoops! You have run out of chips, better luck next time.")
        break

    #Ask to play again
    new_game = input("would you like to play another hand? y/n")

    if new_game[0].lower() == 'y':
        playing = True
        continue
    else:
        print("Thank you for playing!")
        break    