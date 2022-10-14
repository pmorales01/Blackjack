#!/usr/bin/env python3
# Pedro Morales
# CPSC 386-03
# 2022-03-16
# pedrom2@csu.fullerton.edu
# @pedromorales451
#
# Lab 03-00
#
# This file creates and runs a Blackjack game object.
#

"""This module creates, then runs an instance of a Blackjack game."""

from blackjackgame import game

if __name__ == "__main__":
    GAME = game.Blackjack()
    GAME.run()
