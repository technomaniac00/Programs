import random

suits = ('Hearts', 'Diamonds', 'Spades', 'Clubs')
ranks = ('Two', 'Three', 'Four', 'Five', 'Six', 'Seven', 'Eight', 'Nine', 'Ten', 'Jack', 'Queen', 'King', 'Ace')
values = {'Two':2, 'Three':3, 'Four':4, 'Five':5, 'Six':6, 'Seven':7, 'Eight':8, 'Nine':9, 'Ten':10, 'Jack':10,'Queen':10, 'King':10, 'Ace':11}
playing=True

# card
class Card:
    # initialization
    def __init__(self,suit,rank):
        self.suit=suit
        self.rank=rank

    # output for print statements
    def __str__(self):
        return f"{self.rank} of {self.suit}"

# deck        
class Deck:
    # initialization
    def __init__(self):
        self.deck=[]
        for suit in suits:
            for rank in ranks:
                self.deck.append(Card(suit,rank))

    # output for print statements  
    def __str__(self):
        self.complete_deck=''
        for individualcard in self.deck:
            complete_deck+="\n"+individualcard.__str__()
        return "Cards present in the deck are\n"+complete_deck

    # to remove one card from the deck 
    def deal(self):
        onecard=self.deck.pop()
        return onecard

    # shuffle the deck    
    def shuff(self):
        random.shuffle(self.deck)

# create a hand for the players       
class Hand:
    # initialization
    def __init__(self):
        self.cards=[]
        self.value=0
        self.aces=0

    # to add cards into the hand
    def add_card(self,card):
        self.cards.append(card)
        self.value+=values[card.rank]
        if card.rank=="Ace":
            self.aces+=1

    # adjusting the ace value as 1 or 11    
    def adjust_for_aces(self):
        if self.value>21 and self.aces>0:
            self.value-=10
            self.aces-=1

# chips for placing bets
class Chips:
    # initialization
    def __init__(self):
        self.total=100
        self.bet=0

    def win_bet(self):
        self.total+=self.bet

    def lose_bet(self):
        self.total-=self.bet

# taking the chip amount for bet        
def take_bet(chip_class):
    while True:
        try:
            chip_class.bet=int(input("Enter the amount of bet"))
        except ValueError:
            print("Enter a valid number")
        else:
            if chip_class.bet>chip_class.total:
                print(f"Your current balance is {chip_class.total}. Do not excede the limit.")
            else:
                break

# function to implement hit
def hit(deck,hand):
    hand.add_card(deck.deal())
    hand.adjust_for_aces()
    
# function to check if player wants to hit or stand
def hit_or_stand(deck,hand):
    global playing
    # loop to fetch h or s else keep iterating
    while True:
        x=input("Want to Hit or Stand? (h or s) ")
        if x[0].lower()=='h':
            hit(deck,hand)
        elif x[0].lower()=='s':
            print("Player stands. Dealer is playing")
            playing=False
        else:
            print("Please enter a vaild input")
            continue
        break

# hide one card of dealer and show all for player
def show_one(player,dealer):
    print("="*25)
    print("Dealer's Hand")
    print("One card is hidden")
    print(dealer.cards[1])

    print("\nPlayer's Hand")
    for i in player.cards:
        print(i)
    print("="*25)

# show all for player and dealer 
def show_all(player,dealer):
    print("="*25)
    print(f"Dealers's Hand: {dealer.value}")
    for i in dealer.cards:
        print(i)

    print(f"Player's Hand: {player.value}")
    for i in player.cards:
        print(i) 
    print("="*25)

# player loses        
def player_busts(player,dealer,chips):
    print("Player Busts")
    chips.lose_bet()
 
# player wins   
def player_wins(player,dealer,chips):
    print("Player Wins")
    chips.win_bet()

# dealer loses   
def dealer_busts(player,dealer,chips):
    print("Player Wins! Dealer Busts")
    chips.win_bet()

# dealer wins    
def dealer_wins(player,dealer,chips):
    print("Dealer Wins")
    chips.lose_bet()

def push(player,dealer):
    print("Dealer and Player tie! It's a push.")
    
# main part to play the game
while True:
    print("Welcome to BLACKJACK!\nLets Begin the game.")
    temp=0
    player_chips=Chips()
    while True:
        # create and shuffle the deck
        deck=Deck()
        deck.shuff()
        # create player hand
        player_hand=Hand()
        player_hand.add_card(deck.deal())
        player_hand.add_card(deck.deal())

        # create dealer hand
        dealer_hand=Hand()
        dealer_hand.add_card(deck.deal())
        dealer_hand.add_card(deck.deal())

        take_bet(player_chips)
        print(f"${player_chips.total} available balance")
        print(f"${player_chips.bet} bet placed.")

        # showing cards
        show_one(player_hand,dealer_hand)
        
        # player to play
        while playing:
            # prompt to get hit or stand from player
            hit_or_stand(deck,player_hand)
            # showing cards
            show_one(player_hand,dealer_hand)
            # check if the player's hand value is greater than 21
            if player_hand.value>21:
                player_busts(player_hand,dealer_hand,player_chips)
                break

        # dealer to play    
        if player_hand.value<=21:
            while dealer_hand.value<17:
                hit(deck,dealer_hand)
            show_all(player_hand,dealer_hand)

            if dealer_hand.value>21:
                dealer_busts(player_hand,dealer_hand,player_chips)

            elif player_hand.value>dealer_hand.value:
                player_wins(player_hand,dealer_hand,player_chips)

            elif player_hand.value<dealer_hand.value:
                dealer_wins(player_hand,dealer_hand,player_chips)
            else:
                push(player_hand,dealer_hand)

        print(f"Total chips available {player_chips.total}")
        new_game=input("Do you want to continue ? (y or n) ")
        if new_game[0]=='y':
            playing=True
            continue
        elif new_game[0]=='n':
            new_game1=input("Do you want to play a new game ? (y or n) ")
            if new_game1[0]=='n':
                print("Thank you for playing")
                temp=1
                break
            elif new_game1[0]=='y':
                print("INITIATING NEW GAME...")
                break
        else:
            print("Exitting the game")
            temp=1
            break

    if temp==1:
        break
print("GAME END")