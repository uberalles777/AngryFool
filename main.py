#!/usr/bin/python2.7
__author__ = 'mark'

import random

ranks = range(6, 15)
suits = ["D", "C", "H", "S"]
current_trump = ""
playernames = ["Player1", "Player2", "Player3"]
players = []

rulelib = {
        1: "The first move is to do one card or several cards peers.",
        2: "Spades is not trump. Spades hit only spades.",
        3: "The card can only beat by senior in rank suited cards or any trump.",
        4: "Hidden trump is spades, spades can't be trump. Trump has remained the same",
        5: "Trump has remained the same.",
        6: '"Trump is changed. Current trump is %s" % current_trump'
    }

#Class for playng card
class Card(object):
    def __init__(self, rank, suit):
         self.rank = rank
         self.suit = suit

    def get_rank(self):
        return self.rank

    def get_suit(self):
        return self.suit

    def get_name(self):
        name = self.suit + str(self.rank)
        return name


#Class for playng deck. It contains the playing cards and two trumps.
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

#Class for player
class Hand(object):
    def __init__(self, name):
        self.name = name
        self.cards = []

    def show_name(self):
        return self.name

    def add_card(self,card):
        namedcard = [card.get_name(), card]
        self.cards.append(namedcard)

    def pop_card(self,card):
        self.cards.pop(card)

    def show_cards(self):
        return self.cards

    def get_hand_len(self):
        return len(self.cards)

#Class for playng table.
class Table(object):
    def __init__(self):
        self.table = []
        self.input_table = []
        self.hited = []

    def add_card(self, card, act):
        if act == "add":
            self.table.append(card)

    def get_table(self):
        return self.table

    def bit_card(self):
        for sf in self.table:
            for it in self.input_table:
                if sf.get_rank() > it.get_rank() or sf.get_suit() != it.get_suit():
                    print(rulelib.get(3))
                elif sf.get_suit() != 'S' and it.get_suit() == 'S':
                    print(rulelib.get(2))
                elif sf.get_suit() == 'S' and it.get_suit() != 'S':
                    print(rulelib.get(2))
                elif sf.get_rank() < it.get_rank() and sf.get_suit() == it.get_suit() or sf.get_suit() == current_trump:
                    self.hited.append(self.table.pop(0))
                    self.hited.append(self.input_table.pop(0))

    def clear_table(self):
        self.table.clear()

#Main game function. Provides gameplay.
def new_game():
    global current_trump
    deck = Deck()
    current_trump = deck.get_trump().get_suit()
    table = Table()
    begin_handset = []
    begin_handset_dict = {}

    def fill_hand(player):
        global current_trump
        while player.get_hand_len() <= 5:
            player.add_card(deck.deal_card())
            if deck.get_deck_len() == 0:
                if deck.get_hidden_trump().get_suit() == "S":
                    print(rulelib.get(4))
                    break
                elif deck.get_hidden_trump().get_suit() == current_trump:
                    print(rulelib.get(5))
                    break
                else:
                    current_trump = deck.get_hidden_trump().get_suit()
                    print("Trump is changed. Current trump is %s" % current_trump)
                    break

    def get_handset(hndst_dict):
        handset_parsed_dict = {}
        for plr in hndst_dict:
            hndst = hndst_dict.get(plr)
            handset = [(s.get_rank(), s.get_suit()) for s in hndst]
            handset = sorted(handset, key=lambda x: x[0])
            hndst_prst = dict.fromkeys([plr], handset)
            handset_parsed_dict.update(hndst_prst)
        return handset_parsed_dict




    print("Current trump is %s" % current_trump)



    # test_player = Hand("Test")
    # print(deck.deal_card().get_name())
    # print(deck.get_deck_len())
    # print(deck.get_trump().get_name())
    # print(deck.get_hidden_trump().get_name())


    for h in playernames:
        players.append(Hand(h))

    for ghs in players:
        fill_hand(ghs)
        begin_handset.append(ghs.show_cards())
        ghs_dict = dict.fromkeys([ghs.show_name()], ghs.show_cards())
        begin_handset_dict.update(ghs_dict)

    # print(begin_handset_dict)

    test_handset = begin_handset_dict.get(playernames[0])

    print(test_handset)

    def select_by_suit(hndst, st):
        cardlist = []
        for card in hndst:
            name = card[0]
            if name[0] == st:
                cardlist.append(card)
        return cardlist

    def select_by_rank(hndst, rnk):
        cardlist = []
        for card in hndst:
            rank = int(card[0][1:])
            if rank == rnk:
                cardlist.append(card)
        return cardlist

    def select_youger(hndst):
        rnklst = []
        for card in hndst:
            rnk = int(card[0][1:])
            rnklst.append(rnk)
        try:
            min_rank = min(rnklst)
        except:
            min_rank = None
            return min_rank
        card_index = rnklst.index(min_rank)
        younger = hndst[card_index]
        return younger

    test_cardlist_suited = select_by_suit(test_handset, current_trump)
    test_cardlist_ranked = select_by_rank(test_handset, 6)
    # print(test_cardlist_suited)
    print(select_youger(test_cardlist_suited))
#    print(test_cardlist_ranked)



#     answer = input("select card \n")
#     if answer.isdigit():
#         answer = int(answer)
# #        print(handset1[answer])
#         selected_card = player_hand1.show_cards()[answer]
#         print(selected_card)
#         table.add_card(player_hand1.pop_card(answer), "add")
#         print(player_hand1.get_hand_len())
#         print(table.get_table())
#         print(deck.get_deck_len())
#     else:
#         print("Select card by digit")








new_game()

