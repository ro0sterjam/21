import sys
sys.path.append("..")

from common.continuous_deck import Deck
from common.hand import Hand
from common.enums import GameState, PlayerAction

'''
This is an extremely stripped down, simple version of blackjack with the following changes:

1) There is no running "shoe", each card dealt has a constant probability regardless of how many times it has already been dealt prior
2) The only available actions are STAY and HIT (i.e. no DOUBLING DOWN, no SPLITS, no SURRENDERS, etc.)
3) The dealer must stay on soft 17
4) There are no bets, only a -1 for a loss, a 0 for a tie, and a 1 for a win
'''

class Blackjack:

	def __init__(self, deck=Deck(), state=GameState.FINISHED, dealers_hand=None, hands=None, hand=None):
		self.deck = deck
		self.state = state
		self.dealers_hand = dealers_hand
		self.hands = hands
		self.hand = hand

	def perform_action(self, action, wager=None):
		if action == PlayerAction.BET:
			if self.state != GameState.FINISHED: raise ValueError('Cannot bet mid game')
			if wager == None: raise ValueError('Wager must be provided when action is BET')
			if wager <= 0: raise ValueError('Wager must be positive')
			self.state = GameState.PLAYING
			self.dealers_hand = Hand(self.deck.deal(), self.deck.deal())
			self.hands = [Hand(self.deck.deal(), wager)]
			self.hand = 0
			return self.state, self.hands, 0, self.dealers_hand, None

		elif action == PlayerAction.STAY:
			if self.state != GameState.PLAYING: raise ValueError('Cannot STAY when GameState is not PLAYING')
			if self.hand + 1 < len(self.hands):
				self.hand = self.hand + 1
				return self.state, self.hands, self.hand, self.dealers_hand, None
			while self.dealers_hand.best_val() < 17 and not self.dealers_hand.is_busted():
				self.dealers_hand = self.dealers_hand.hit(self.deck.deal())
			if self.dealers_hand.is_busted():
				self.state = GameState.FINISHED
				return self.state, self.hands, self.hand, self.dealers_hand, sum(map(lambda hand: hand.wager * 2, self.hands))
			else:
				self.state = GameState.FINISHED
				reward = sum(map(lambda hand: 0 if self.dealers_hand.best_val() > hand.best_val() else hand.wager * 2 if hand.best_val() > self.dealers_hand.best_val() else hand.wager, self.hands))
				return self.state, self.hands, self.hand, self.dealers_hand, reward

		elif action == PlayerAction.HIT:
			if self.state != GameState.PLAYING: raise ValueError('Cannot HIT when GameState is not PLAYING')
			self.hands[self.hand] = self.hands[self.hand].hit(self.deck.deal())
			if self.hands[self.hand].is_busted():
				if self.hand + 1 < len(self.hands):
					self.hand = self.hand + 1
					return self.state, self.hands, self.hand, self.dealers_hand, None
				else:
					self.state = GameState.FINISHED
					return self.state, self.hands, self.hand, self.dealers_hand, 0
			else:
				return self.state, self.hands, self.hand, self.dealers_hand, None

		elif action == PlayerAction.DOUBLE:
			if self.state != GameState.PLAYING: raise ValueError('Cannot DOUBLE when GameState is not PLAYING')
			self.hands[self.hand] = self.hands[self.hand].double(self.deck.deal(), wager)
			if self.hands[self.hand].is_busted():
				if self.hand + 1 < len(self.hands):
					self.hand = self.hand + 1
					return self.state, self.hands, self.hand, self.dealers_hand, None
				else:
					self.state = GameState.FINISHED
					return self.state, self.hands, self.hand, self.dealers_hand, 0
			else:
				return self.perform_action(PlayerAction.STAY)

		elif action == PlayerAction.SPLIT:
			if self.state != GameState.PLAYING: raise ValueError('Cannot SPLIT when GameState is not PLAYING')
			left_hand, right_hand = self.hands[self.hand].split([self.deck.deal(), self.deck.deal()], wager)
			self.hands[self.hand] = left_hand
			self.hands.append(right_hand)
			return self.state, self.hands, self.hand, self.dealers_hand, None