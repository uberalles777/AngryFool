#!/usr/bin/python2.7
__author__ = 'mark'

import random

ranks = range(6, 15)
suits = ["D", "C", "H", "S"]
players = 2


class Card(object):
    def __init__(self, rank, suit):
         self.rank = rank
         self.suit = suit

    def get_rank(self):
        return self.rank

    def get_suit(self):
        return self.suit


class Hand(object):
    def __init__(self, name):
        self.name = name
        self.cards = []

    def add_card(self,card):
        self.cards.append(card)

    def pop_card(self,card):
        self.cards.pop(card)

    def show_cards(self):
        return self.cards

    def get_hand_len(self):
        return len(self.cards)


class Deck(object):
    def __init__(self):
        self.cards = [Card(r, s) for r in ranks for s in suits]
        random.shuffle(self.cards)
        self.trump = self.cards[1]
        self.hidden_trump = self.cards[0]

        while self.trump.get_suit() == 'S':
            random.shuffle(self.cards)
            self.trump = self.cards[1]
            self.hidden_trump = self.cards[0]

    def get_trump(self):
        return self.trump

    def get_hidden_trump(self):
        return self.hidden_trump

    def deal_card(self):
        return self.cards.pop()

    def get_deck_len(self):
        return len(self.cards)


class Table(object):
    def __init__(self):
        self.table = []

    def add_card(self, card):
        self.table.append(card)

    def get_table(self):
        return self.table


def new_game():
    deck = Deck()
    table = Table()
    player_hand1 = Hand("Player1")
    player_hand2 = Hand("Player2")

    def fill_hand(player):
        while player.get_hand_len() <= 5:
            player.add_card(deck.deal_card())

    def get_handset(player):
        handset = [(s.get_rank(), s.get_suit()) for s in player.show_cards()]
        handset = sorted(handset, key=lambda x: x[0])
        return handset

    fill_hand(player_hand1)
    fill_hand(player_hand2)

#    print(player_hand1.show_cards())

    handset1 = get_handset(player_hand1)
    turn_set = []


    answer = input("select card")
    if answer.isdigit():
        answer = int(answer)
#        print(handset1[answer])
        selected_card = player_hand1.show_cards()[answer]
        print(selected_card)
        table.add_card(player_hand1.pop_card(answer))
        print(player_hand1.get_hand_len())
        print(table.get_table())
        print(deck.get_deck_len())








new_game()

