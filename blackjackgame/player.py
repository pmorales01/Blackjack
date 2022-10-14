# Pedro Morales
# CPSC 386-03
# 2022-03-16
# pedrom2@csu.fullerton.edu
# @pedromorales451
#
# Lab 03-00
#
# This file contains and defines the Player and ComputerDealer classes.
#

"""This module defines the human player and computer player AI classes."""

import time
from .cards import Deck


class Player:
    """A player class to represent human players."""

    def __init__(self, name):
        """Constructor for a Player."""
        self._name = name
        self._wager = 0
        self._balance = 10000
        self._hand = [[], []]
        self._insurance = 0
        self._double_down = [[], []]
        self._can_play = [True, True]

    @property
    def name(self):
        """Returns the name of the player."""
        return self._name

    @property
    def wager(self):
        """Returns the original wager of the player."""
        return self._wager

    @property
    def can_play(self):
        """Returns if the player should continue playing in the game."""
        return self._can_play

    def cant_play(self, _):
        """Sets a bool to False to indicate player should stop playing."""
        self._can_play[_] = False

    @property
    def hand(self):
        """Returns all of the player's hands."""
        return self._hand

    def hand_i(self, i):
        """Returns a player's ith hand."""
        return self._hand[i]

    def hand_i_j(self, i, j):
        """Returns the jth card from the ith hand."""
        return self._hand[i][j][0]

    @property
    def balance(self):
        """Returns the player's balance."""
        return self._balance

    @property
    def hand1(self):
        """Returns the player's first hand."""
        return self._hand[0]

    @property
    def hand2(self):
        """Returns the player's second hand."""
        return self._hand[1]

    @property
    def insurance(self):
        """Returns player's insurance bet."""
        return self._insurance

    @insurance.setter
    def insurance(self, bet):
        self._insurance = bet

    @property
    def double_down(self):
        """Returns list of player's double down bets."""
        return self._double_down

    def subtract_balance(self, amount):
        """Subtracts the amount lost from balance."""
        self._balance -= amount
        print("New Balance: ${}".format(self.balance))

    def add_balance(self, amount):
        """Adds the amount won to balance."""
        self._balance += amount
        print("\t+ ${}!".format(amount))
        print("\n\tNew Balance: ${}".format(self.balance))

    def set_initial_wager(self, wager):
        """Sets the player's initial wager."""
        self._wager = wager
        self._balance -= wager
        print("New Balance: ${}".format(self._balance))

    def reset(self):
        """Resets the values of the data members of a player object."""
        self._wager = 0
        self._hand = [[], []]
        self._insurance = 0
        self._double_down = [[], []]
        self._can_play = [True, True]

    def __str__(self):
        """Converts Player to printable string."""
        return self._name

    def __repr__(self):
        """Python representation of Player."""
        return 'Player("{}")'.format(self._name)


class ComputerDealer(Player):
    """A ComputerDealer class to represent a dealer AI."""

    def __init__(self, game):
        """Constructor for a ComputerDealer object."""
        super().__init__("Luigi")
        self._balance = 999999
        self._game = game
        self._dealer_bust = False
        self._check_win = True

    @property
    def dealer(self):
        """Returns the dealer from a Blackjack game instance."""
        return self._game.dealer

    @property
    def players(self):
        """Returns a player list from a Blackjack game instance."""
        return self._game.players

    def get_hand(self):
        """Prints the dealer's hand."""
        print("\n\tDealer's hand : ")
        if len(self.hand1) == 2:
            print("\t\t* ", self.hand[0][0][0])
            print("\t\t* ", "Face Down Card")

        else:
            for _ in range(0, len(self.hand1)):
                print("\t\t* ", self.hand[0][_][0])

    def set_up_shoe(self):
        """Sets up the shoe for the current Blackjack game instance."""
        print("\nSetting up the decks...\n")
        time.sleep(2)

        deck = Deck()
        for _ in range(0, 7):
            new_decks = Deck()
            deck.merge(new_decks)

        self._game.shoe = deck

        # shuffle the decks 8 times
        self._game.shoe.shuffle(8)

        # cut the deck
        self._game.shoe.cut()

    def deal_card(self, player, hand):
        """Deal a card to player to a hand."""
        card = self._game.shoe.deal()
        if card[0] == "CUT CARD":
            print("\nCut card reached...shuffling the deck")
            time.sleep(2)
            self.set_up_shoe()
            card = self._game.shoe.deal()
            player.hand[hand].append(card)
            print("\n{} is given to".format(card[0]), player.name)
            time.sleep(2)

        else:
            player.hand[hand].append(card)
            print("\n{} is given to".format(card[0]), player.name)
            time.sleep(2)

    def deal_hidden_card(self):
        """Deals a card to dealer, whose rank and suit are not printed."""
        card = self._game.shoe.deal()

        if card[0] == "CUT CARD":
            print("\nCut card reached...shuffling the deck")
            time.sleep(2)
            self.set_up_shoe()
            card = self._game.shoe.deal()
            self._hand[0].append(card)
            print("\nA Face Down Card is given to {}".format(self.dealer.name))
            time.sleep(2)

        else:
            self._hand[0].append(card)
            print("\nA Face Down Card is given to {}".format(self.dealer.name))
            time.sleep(2)

    def deal_to_each_player(self):
        """Deals 2 cards to each player in order."""
        # hand every player 1 card
        for i in range(0, len(self.players) - 1):
            self.deal_card(self.players[i], 0)

        # Dealer gets a card
        self.deal_card(self, 0)

        # hand every player 1 card
        for i in range(0, len(self.players) - 1):
            self.deal_card(self.players[i], 0)
            self._game.check_for_blackjack(self.players[i], 0)

        # Dealer gets a card
        self.deal_hidden_card()

    def split(self, player, player_index):
        """Splits player's hand from 1 to 2 and deals a card to each hand."""
        answer = input("\nWould you like to split? [Y/N] ")

        if answer.lower() == "y":
            # Convert 1 hand into two hands
            card = player.hand1[1]
            player.hand1.pop()
            player.hand2.append(card)
            self._game.busted[player_index].append(False)

            # Add an additional card to each hand
            for _ in range(0, 2):
                self.deal_card(player, _)
                self._game.display_hand(player)
                self._game.check_for_blackjack(player, _)

            print("\nDoubling your wager because you split...")
            player.subtract_balance(player.wager)

    @staticmethod
    def buy_insurance(player):
        """Determines if player wants to purchase insurance."""

        if player.can_play[0] is False:
            return

        answer = input("\nDo you want to purchase insurance? [Y/N] ")

        if answer.lower() == "y":
            if player.balance == 0:
                print("\nSorry, you can't afford insurance.")
            else:
                print("\nYour current balance: ${}".format(player.balance))
                bet = int(input("\nHow much insurance do you want to buy? "))
                while bet > player.balance or bet < 1:
                    bet = int(input("Enter a valid insurance bet amount: "))
                player.insurance = bet
                player.subtract_balance(bet)

    def bet_double_down(self, player):
        """Determines if player wants to double down for each hand."""
        if len(player.hand2) == 0:
            num = 1
        else:
            num = 2

        for _ in range(0, num):
            sums = self._game.sum_of_hand(player, _)
            minimum = min(sums)
            if 21 not in sums and (minimum < 21):
                answer = input(
                    "\nWant to double down on hand #{}? [Y/N] ".format(_ + 1)
                )
                if answer.lower() == "y":
                    if player.balance - player.wager >= 0:
                        player.double_down[_].append(player.wager)
                        player.subtract_balance(player.wager)
                        self.deal_card(player, _)
                        self._game.display_hand(player)
                        self._game.check_if_busted(player, _)
                        player.cant_play(_)
                    else:
                        print("\nSorry, you cannot afford to double down.")

    def hit(self, player, hand_i):
        """A card is dealt to player, then checks if player busted."""
        self.deal_card(player, hand_i)
        self._game.display_hand(player)
        self._game.check_if_busted(player, hand_i)

    def hit_stand(self):
        """Determines if the dealer should hit or stand."""
        sums = self._game.sum_of_hand(self, 0)

        if 21 in sums:
            print("\n{} reached 21!".format(self.name))
            time.sleep(2)

        all_busted = True

        for i in range(0, len(self._game.busted)):
            if False in self._game.busted[i]:
                all_busted = False
                break

        if all_busted:
            print("\n{} has chosen to stand!".format(self.name))
            return

        seen = False
        for _ in sums:
            if _ in range(17, 22):
                print("\n{} has chosen to stand!".format(self.name))
                time.sleep(2)
                seen = True
                break

        if seen is False:
            maximum = max(sums)
            if maximum > 21:
                maximum = min(sums)
            for _ in sums:
                if _ < 17 and _ == maximum:
                    print("\n{} has chosen to hit!".format(self.name))
                    time.sleep(2)
                    self.deal_card(self, 0)
                    self._game.display_hand(self)
                    self.hit_stand()

        minimum = min(sums)

        for _ in sums:
            if _ > 21 and seen is False and minimum == _:
                print("\n{} busted!".format(self.name))
                self._dealer_bust = True
                time.sleep(2)
                break

    def player_is_busted(self, current_player, _):
        """Determines player's earnings after busting."""
        self._check_win = False
        print("\n\tYou lose! You busted!")
        time.sleep(3)
        print("\n\tThe house kept your original wager!")
        time.sleep(3)
        if len(current_player.double_down[_]) == 1:
            print("\n\tThe house kept your double down wager!")
            time.sleep(3)

        print("\n\tYour current balance: ${}".format(current_player.balance))

        time.sleep(3)

    def neither_busted(self, dealer_sums, player, i, _):
        """Determines earnings after neither player or dealer busted."""
        player_sums = self._game.sum_of_hand(player, _)

        max_player_sum = max(player_sums)

        # dealer did not bust and player beat the dealer
        for j in dealer_sums:
            if 17 <= j < max_player_sum < 21:
                self._check_win = False
                print("Your Score:", max_player_sum, "\tDealer's Score:", j)
                print("\n\tYou win! You had a higher score than the dealer!")
                print("\n\tYou won! You won your original wager!")
                time.sleep(3)
                player.add_balance(player.wager * 2)

                # determine double down
                if len(player.double_down[_]) == 1:
                    print("\n\tYou won your double down bet!")
                    time.sleep(3)
                    player.add_balance(player.wager * 2)
                return

        # dealer did not bust but player did not beat dealer
        for j in player_sums:
            for k in dealer_sums:
                if j < k <= 21:
                    if self._game.busted[i][_] is False:
                        self._check_win = False

                        print("Your Score:", j, "\tDealer's Score:", k)

                        print(
                            "\n\tYou lose! The dealer beat you",
                            "by getting a higher score!",
                        )
                        time.sleep(3)
                        print("\n\tThe house kept your original wager!")
                        time.sleep(3)
                        if len(player.double_down[_]) == 1:
                            print("\n\tThe house kept your double down wager!")
                            time.sleep(3)
                        balance = player.balance
                        print("\n\tYour current balance: ${}".format(balance))
                        return

    def player_won_dealer_bust(self, current_player, i, _):
        """Determines earnings after player wins by dealer busting."""
        if self._dealer_bust and (self._game.busted[i][_] is False):
            self._check_win = False
            print("\n\tYou win! The dealer busted!")
            print("\n\tYou won! You won your original wager!")
            time.sleep(3)
            current_player.add_balance(current_player.wager * 2)

            # determine double down
            if len(current_player.double_down[_]) == 1:
                print("\n\tYou won your double down bet!")
                time.sleep(3)
                current_player.add_balance(current_player.wager * 2)

    def push(self, dealer_sums, current_player, _):
        """Determines earnings after player and dealer push."""
        if self._check_win:
            player_sums = self._game.sum_of_hand(current_player, _)

            # Determine if push
            for j in player_sums:
                for k in dealer_sums:
                    if j == k:
                        self._check_win = False
                        print("Your Score:", j, "\tDealer's Score:", k)
                        print("\n\tPush! Your original wager is returned!")
                        time.sleep(3)
                        current_player.add_balance(current_player.wager)
                        if len(current_player.double_down[_]) == 1:
                            print("\n\tThe house kept your double down wager!")
                            time.sleep(3)
                        return

    def player_won_dealer_not_busted(self, player, _):
        """Determines earnings after player got 21 and dealer did not bust."""
        if self._check_win:
            player_sums = self._game.sum_of_hand(player, _)
            if 21 in player_sums:
                self._check_win = False
                print("\n\tYou win! You got 21!")
                print("\n\tYou won! You won your original wager!")
                time.sleep(3)
                player.add_balance(player.wager * 2)

                # determine double down
                if len(player.double_down[_]) == 1:
                    print("\n\tYou won your double down bet!")
                    time.sleep(3)
                    player.add_balance(player.wager * 2)
                return

    def not_busted_or_won(self, dealer_sums, current_player, _):
        """Determines earnings after player did not bust or beat dealer."""
        if self._check_win:

            player_sums = self._game.sum_of_hand(current_player, _)

            maximum = max(player_sums)

            if maximum > 21:
                maximum = min(player_sums)

            for k in dealer_sums:
                if maximum < k:
                    if 17 <= k <= 21:
                        print("Your Score:", maximum, "\tDealer's Score:", k)
                        time.sleep(3)

                        print("\n\tYou lose! The dealer beat you!")
                        time.sleep(3)
                        print("\n\tThe house kept your original wager!")
                        time.sleep(3)
                        if len(current_player.double_down[_]) == 1:
                            print("\n\tThe house kept your double down wager!")
                            time.sleep(3)
                        return

    def payout(self):
        """Determines and distribute each player's earnings."""

        print("\n-----------------------------------------------------------")

        dealer_sums = self._game.sum_of_hand(self, 0)

        for i in range(0, len(self._game.players) - 1):
            current_player = self._game.players[i]

            print("\n{}'s Earnings:".format(current_player.name))
            time.sleep(2)

            if len(current_player.hand2) == 0:
                num = 1
            else:
                num = 2

            # for each of the current player's hand
            for _ in range(0, num):
                print("\nHand # {}:".format(_ + 1))
                time.sleep(2)

                # if player is busted
                if self._game.busted[i][_]:
                    self.player_is_busted(current_player, _)

                # The dealer and the player push
                self.push(dealer_sums, current_player, _)

                # The dealer busted, but the player did not bust
                if self._check_win:
                    self.player_won_dealer_bust(current_player, i, _)

                # The dealer did not bust, but the player beat the dealer
                self.player_won_dealer_not_busted(current_player, _)

                # Determine if player has higher value hand than dealer,
                # but both dealer and player haven't busted
                if self._check_win:
                    self.neither_busted(dealer_sums, current_player, i, _)

                # The player did not bust or beat the dealer
                # The dealer has a score between 17 and 21
                # The player has a score less than 17.
                if self._check_win:
                    self.not_busted_or_won(dealer_sums, current_player, _)

                # reset self._check_win
                self._check_win = True

            # insurance
            if 21 in dealer_sums and len(self._hand[0]) == 2:
                if current_player.insurance != 0:
                    print("\n\tYou've won Insurance!")
                    time.sleep(3)
                    current_player.add_balance(current_player.insurance * 2)
            elif current_player.insurance == 0:
                time.sleep(3)
            else:
                print("\n\nDid not collect insurance!")
                time.sleep(3)

            print("\nFinal Balance: ${}".format(current_player.balance))
            time.sleep(2)
            print("\n------------------------------------------------------")

    def reset_data_members(self):
        """Resets the values of Dealer's data members."""
        self._hand = [[], []]
        self._dealer_bust = False
        self._check_win = True
