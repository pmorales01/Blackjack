# Pedro Morales
# CPSC 386-03
# 2022-03-16
# pedrom2@csu.fullerton.edu
# @pedromorales451
#
# Lab 03-00
#
# This file contains and defines the Blackjack class.
#

"""This module defines a Blackjack class to run the game and functions to
    pickle existing Player objects."""

import time
import pickle
import os.path
from .player import Player, ComputerDealer


def to_file(pickle_file, players):
    """Write the list player to the file pickle_file."""
    with open(pickle_file, "wb") as file_handle:
        pickle.dump(players, file_handle, pickle.HIGHEST_PROTOCOL)


def from_file(pickle_file):
    """Read the contents of pickle_file and return it as players."""
    with open(pickle_file, "rb") as file_handle:
        players = pickle.load(file_handle)
    return players


class Blackjack:
    """A Blackjack class which runs an instance of a Blackjack game."""

    def __init__(self):
        """Constuctor for Blackjack that creates an array of players."""
        self._players = []
        self._shoe = []
        self._busted = []
        self._play_again = True

    def check_if_dealer(self, player):
        """Returns True if player is the dealer."""
        if self.dealer.name == player.name:
            return True
        return False

    @property
    def dealer(self):
        """Returns an instance of a dealer object."""
        return self._players[len(self._players) - 1]

    @property
    def players(self):
        """Returns the current list of players."""
        return self._players

    @property
    def shoe(self):
        """Returns the shoe."""
        return self._shoe

    @shoe.setter
    def shoe(self, decks):
        """Sets and modifies the shoe."""
        self._shoe = decks

    @property
    def busted(self):
        """Returns a list of bools that represent the busted hands."""
        return self._busted

    def check_for_blackjack(self, player, hand_i):
        """Checks if a player has a Blackjack on one of their hands."""
        sums = self.sum_of_hand(player, hand_i)
        if 21 in sums:
            print("{}! You got a Blackjack!".format(player.name))
            player.cant_play(hand_i)

    def display_hand(self, player):
        """Displays the hands of the player or dealer, or both."""
        if self.check_if_dealer(player):
            print("\nDealer's Hand:")
            for _ in range(0, len(player.hand_i(0))):
                print("\t\t* ", player.hand_i_j(0, _))
                time.sleep(2)
        else:
            if len(player.hand2) == 0:
                num = 1
            else:
                num = 2

            for i in range(0, num):
                print("\thand #", i + 1, ":")
                time.sleep(2)
                for _ in range(0, len(player.hand_i(i))):
                    print("\t\t* ", player.hand_i_j(i, _))
                    time.sleep(2)

            time.sleep(2)

            self.dealer.get_hand()

        time.sleep(2)

    def search_list(self, name):
        """Searches the list from 'player.pickle' for name."""
        file_exists = os.path.exists("player.pickle")
        if file_exists:
            # Get players from pickle file
            players = from_file("player.pickle")

            player_found = False

            num = len(players)

            for i in range(0, num):
                if players[i].name == name:
                    self._players.append(players[i])
                    print("Welcome back {}!".format(players[i].name))
                    player_found = True
                    break

            if player_found is False:
                self._players.append(Player(name))
        else:
            self._players.append(Player(name))

    def initialize_players(self, num_players):
        """Creates plabyer objects for human players and the dealer."""

        # For each player...
        for i in range(num_players):
            # ask the user for their name.
            name = input("\nWhat is your name Player {}? ".format(i + 1))

            self.search_list(name)

            print("Your balance is ${}.".format(self._players[i].balance))

            # if current player is broke
            if self._players[i].balance <= 0:
                print("An anonymous donor has gifted you $10,000!")
                time.sleep(3)
                self._players[i].add_balance(10000)

            # ask the user to place a wager
            wager = int(input("{}, enter a wager: ".format(name)))

            while wager < 1 or wager > self._players[i].balance:
                wager = int(input("{}, enter a valid wager: ".format(name)))

            self._players[i].set_initial_wager(wager)

        # initialize lists
        self._busted = [[False] for i in range(0, num_players)]

        # Create a Dealer
        self._players.append(ComputerDealer(self))
        print(
            "\n{}".format(self._players[num_players].name),
            "is going to be your dealer today!",
        )
        print("\nPlayers by order: ", self._players)
        time.sleep(2)

    @staticmethod
    def can_split(player):
        """Returns True if player can split, False otherewise."""
        if len(player.hand2) != 0:
            return False

        if player.hand_i_j(0, 0).value == player.hand_i_j(0, 1).value:
            if player.balance - player.wager >= 0:
                return True
            print("\nSorry, you cannot afford to split.")

        return False

    def can_buy_insurance(self):
        """Returns True if players are able to buy insurance."""
        if self.dealer.hand_i_j(0, 0).value == 10:
            return True

        if self.dealer.hand_i_j(0, 0).value == 1:
            return True

        return False

    @staticmethod
    def sum_of_hand(player, hand_i):
        """Returns a list of the possible sums of a player's hand."""
        sum1 = 0
        sum2 = 0
        # calculate non-aces first
        for card in player.hand[hand_i]:
            if card[0].value in range(2, 11):
                sum1 += card[0].value

        ace_is_11 = False
        ace_exists = False

        for card in player.hand[hand_i]:
            if card[0].value == 1:
                ace_exists = True
                if sum1 == 10 and ace_is_11 is False:
                    ace_is_11 = True
                    sum1 += 11
                    return [sum1]

                sum1 += 1

        if ace_is_11 is False and ace_exists:
            # sum2 = sum - ace(1) + ace(11)
            sum2 = sum1 - 1 + 11
            return [sum1, sum2]

        # no aces were present
        return [sum1]

    def check_if_busted(self, player, hand_i):
        """Determines if player's hand is busted."""

        sums = self.sum_of_hand(player, hand_i)

        index = 0

        for i in range(0, len(self._players)):
            if self._players[i].name == player.name:
                index = i

        if 21 in sums:
            print("You got a 21!")
            player.cant_play(hand_i)
        else:
            minimum = sums[0]

            for _ in sums:
                if _ < minimum:
                    minimum = _

            for _ in sums:
                if _ > 21 and _ == minimum:
                    print("You busted!")
                    self._busted[index][hand_i] = True
                    player.cant_play(hand_i)

    def hit_or_stand(self, player):
        """Prompts the player if they want to hit or stand."""

        if len(player.hand2) == 0:
            num = 1
        else:
            num = 2

        start = 0

        # start asking player to hit or stand at hand start
        if player.can_play[0] is False:
            start = 1

        for _ in range(start, num):
            if player.can_play[_] is False:
                return

            while player.can_play[_]:
                answer = input(
                    "\nWould you like to hit for hand #{}?[Y/N] ".format(_ + 1)
                )

                if answer.lower() == "y":
                    self.dealer.hit(player, _)
                else:
                    print("You have chosen to stand.")
                    break

    def reset_play(self):
        """Resets and clears data members of game, dealer, and players."""
        # reset game's data members
        self._busted = [[False] for i in range(0, len(self._players) - 1)]
        self._play_again = True

        # Reset dealer's data members
        self.dealer.reset_data_members()

        for i in range(0, len(self._players) - 1):
            # reset player data member
            self._players[i].reset()

            print("\nHello {}!".format(self._players[i].name))
            time.sleep(2)

            print("Your balance is ${}.".format(self._players[i].balance))
            time.sleep(2)

            # if current player is broke
            if self._players[i].balance <= 0:
                print("An anonymous donor has gifted you $10,000!")
                self._players[i].add_balance(10000)

            name = self._players[i].name

            wager = int(input("{}, enter a wager: ".format(name)))

            while wager < 1 or wager > self._players[i].balance:
                wager = int(input("{}, enter a valid wager: ".format(name)))

            self._players[i].set_initial_wager(wager)

    def clear_for_pickle(self):
        """Resets data members of players before written to file."""

        # Delete dealer
        self._players.pop()

        for i in range(0, len(self._players)):
            # reset player's data members, except balance
            self._players[i].reset()

    def play_again(self):
        """Prompt Player 1 if everyone want to play again."""
        player = self._players[0]

        answer = input("\n{}, want to play again? [y/n] ".format(player.name))

        if answer.lower() == "y":
            self._play_again = True
            self.reset_play()
        else:
            self._play_again = False
            self.clear_for_pickle()
            print("\nWriting player(s) to 'player.pickle'...")
            time.sleep(2)
            lists = self._players
            to_file("player.pickle", lists)
            print("\nGoodbye!")

    def run(self):
        """Runs an instance of a Blackjack game."""

        # Prompt user for the number of players.
        num_players = int(input("\nHow many players? [1-4] "))

        # While user enters an invalid number of players...
        while num_players <= 0 or num_players > 4:
            # prompt the user to re-enter the number of players.
            print("Number of players entered was not valid. Try Again.")
            num_players = int(input("\nHow many players? [1-4] "))

        self.initialize_players(num_players)

        self.dealer.set_up_shoe()

        while self._play_again:

            # Deal 2 cards to each player
            self.dealer.deal_to_each_player()

            player_index = 0

            # Circular Queue
            while True:
                current_player = self._players[player_index]

                print("\n\n{} is up!".format(current_player))
                time.sleep(2)

                self.display_hand(current_player)

                if self.check_if_dealer(current_player) is False:
                    if self.can_buy_insurance():
                        self.dealer.buy_insurance(current_player)

                    if self.can_split(current_player):
                        self.dealer.split(current_player, player_index)

                    self.dealer.bet_double_down(current_player)

                    self.hit_or_stand(current_player)

                    print("\n----------------------------------------------")
                else:

                    self.dealer.hit_stand()

                    self.dealer.payout()

                    self.play_again()

                    break

                player_index = (player_index + 1) % len(self._players)
