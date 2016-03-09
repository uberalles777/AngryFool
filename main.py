#!/usr/bin/python2.7
__author__ = 'mark'

import random

ranks = range(6, 15)
suits = ["D", "C", "H", "S"]
current_trump = ""
playernames = ["Player1", "Player2", "Player3", "Player4"]
players = []

rulelib = {
        1: "The first move is to do one card or several cards peers.",
        2: "Spades is not trump. Spades hit only spades.",
        3: "The card can only beat by senior in rank suited cards or any trump.",
        4: "Hidden trump is spades, spades can't be trump. Trump has remained the same",
        5: "Trump has remained the same.",
        6: '"Trump is changed. Current trump is %s" % current_trump',
        7: "Add yourself card is prohibited. Only other players can add cards on the table."
    }

#Class for playng card
class Card(object):
    def __init__(self, rank, suit):
        self.rank = rank
        self.suit = suit
        self.bit_by = ""
        self.status = "Free"

    def get_rank(self):
        return self.rank

    def get_suit(self):
        return self.suit

    def get_name(self):
        name = self.suit + str(self.rank)
        return name

    def set_status(self, status):
        self.status = status

    def get_status(self):
        return self.status

    def clear_status(self):
        self.status = "Free"
        self.bit_by = ""

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
        self.turn_status = ""
        self.table = []
        self.input_table = []
        self.hited = []

    def add_card(self, card, act):
        if act == "add":
            self.table.append(card)
        elif act == "bit":
            self.input_table(card)

    def get_table(self):
        return self.table

    def clear_table(self):
        self.table.clear()

    def bit_card(self):
        def bf(c_bot, c_top):
            if c_bot.get_rank() > c_top.get_rank():
                if c_bot.get_suit() == c_top.get_suit():
                    c_bot.set_status("Slave")
                    c_top.set_status("Master")
                elif (c_bot.get_suit() == "S" and c_top.get_suit() != "S") or (c_bot.get_suit() != "S" and c_top.get_suit() == "S"):
                    print(rulelib.get(2))
                elif c_top.get_suit() == current_trump:
                    c_bot.set_status("Slave")
                    c_top.set_status("Master")
            elif c_bot.get_rank() == c_top.get_rank():
                print(rulelib(7))
            else:
                if c_top.get_suit() == current_trump:
                    c_bot.set_status("Slave")
                    c_top.set_status("Master")
                elif (c_bot.get_suit() == "S" and c_top.get_suit() != "S") or (c_bot.get_suit() != "S" and c_top.get_suit() == "S"):
                    print(rulelib.get(2))
                else:
                    print(rulelib(3))

        if len(self.table) == len(self.input_table):
            for crd_bot in self.table:
                if crd_bot.get_status() == "Free":
                    for crd_top in self.input_table:
                        if crd_top.get.status == "Free":
                            bf(crd_bot, crd_top)

    def get_avaiable_ranks(self):
        rnks = set()
        for crd in self.table:
            rnks.add(int(crd.get_rank()))
        for crd in self.input_table:
            rnks.add(int(crd.get_rank()))
        ranks = list(rnks)
        return ranks



#Main game function. Provides gameplay.
def new_game():
    global current_trump
    deck = Deck()
    current_trump = deck.get_trump().get_suit()
    table = Table()
    players_dict = {}
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

    for h in playernames:
        players.append(Hand(h))

    print(players)

    for ghs in players:
        # print(ghs)
        fill_hand(ghs)
        begin_handset.append(ghs.show_cards())
        print(begin_handset)
        ghs_dict = dict.fromkeys([ghs.show_name()], ghs.show_cards())
        begin_handset_dict.update(ghs_dict)
        plrs_dict = dict.fromkeys([ghs.show_name()], ghs)
        players_dict.update(plrs_dict)

    print(begin_handset_dict)

    test_handset = begin_handset_dict.get(playernames[0])
    print(test_handset)

    def select_by_suit(hndst, st):
        cardlist = []
        for card in hndst:
            name = card.get_name()
            if name[0] == st:
                cardlist.append(card)
        return cardlist

    def select_by_rank(hndst, rnk):
        cardlist = []
        for card in hndst:
            rank = int(card.get_name()[1:])
            if rank == rnk:
                cardlist.append(card)
        return cardlist

    def select_youger(hndst):
        rnklst = []
        for card in hndst:
            rnk = int(card.get_name()[1:])
            rnklst.append(rnk)
        try:
            min_rank = min(rnklst)
        except:
            return None
        card_index = rnklst.index(min_rank)
        younger = hndst[card_index]
        return younger

    def first_turn(hndst_dct):
        # print(hndst_dct)
        first = {}
        values = []
        plrs = []

        for player in hndst_dct:
            trumps = select_by_suit(hndst_dct.get(player), current_trump)
            younger_trump = select_youger(trumps)
            yng_dct = dict.fromkeys([player], younger_trump)
            first.update(yng_dct)

        for plr in first:
            if first.get(plr):
                plrs.append(plr)
                val = int(first.get(plr)[0][1:])
                values.append(val)
                minval = min(values)
                index = values.index(minval)
        first_gamer = plrs[index]
        return first_gamer

    def f2f(plrlst, plr):
        index = plrlst.index(plr)
        while index:
            plrlst.append(plrlst.pop(0))
            index = plrlst.index(plr)

    first_turner = first_turn(begin_handset_dict)
    f2f(playernames, first_turner)
    print(first_turner)
    print(playernames)
    print(players_dict)

    for plr in playernames:
        print(players_dict.get(plr).show_cards())

    print(table.get_avaiable_ranks())

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

