from continuous_deck import Deck
from enums import GameState
from enums import PlayerAction

'''
This is an extremely stripped down, simple version of blackjack with the following changes:

1) There is no running "shoe", each card dealt has a constant probability regardless of how many times it has already been dealt prior
2) The only available actions are STAY and HIT (i.e. no DOUBLING DOWN, no SPLITS, no SURRENDERS, etc.)
3) The dealer must stay on soft 17
4) There are no bets, only a -1 for a loss, a 0 for a tie, and a 1 for a win
'''

class ActionResult:

	def __init__(self, state, hand, dealers_hand, reward=None):
		self.state = state
		self.hand = hand
		self.dealers_hand = dealers_hand
		self.reward = reward

class Blackjack:

	def __init__(self, deck=Deck(), state=GameState.FINISHED, dealers_hand=None, hand=None, wager=None):
		self.deck = deck
		self.state = state
		self.dealers_hand = dealers_hand
		self.hand = hand
		self.wager = wager

	def act(self, action, wager=None):
		if action == PlayerAction.BET:
			if self.state != GameState.FINISHED: raise ValueError('Cannot bet mid game')
			if wager == None: raise ValueError('Wager must be provided when action is BET')
			if wager <= 0: raise ValueError('Wager must be positive')
			self.state = GameState.PLAYING
			self.hand = Hand(self.deck.deal())
			self.dealers_hand = Hand(self.deck.deal(), self.deck.deal())
			self.wager = wager
			return ActionResult(self.state, self.hand, self.dealers_hand)

		elif action == PlayerAction.STAY:
			if self.state != GameState.PLAYING: raise ValueError('Cannot STAY when GameState is not PLAYING')
			self.dealers_hand.take(self.deck.deal())
			if self.dealers_hand.busted():
				self.state = GameState.FINISHED
				return ActionResult(self.state, self.hand, self.dealers_hand, 2 * self.wager)
			elif self.dealers_hand.best_val() >= 17:
				self.state = GameState.FINISHED
				reward = 0 if self.dealers_hand.best_val() > self.hand.best_val() else 2 * self.wager if self.hand.best_val() > self.dealers_hand.best_val() else self.wager
				return ActionResult(self.state, self.hand, self.dealers_hand, reward)
			else:
				return self.act(PlayerAction.STAY)

		elif action == PlayerAction.HIT:
			if self.state != GameState.PLAYING: raise ValueError('Cannot HIT when GameState is not PLAYING')
			self.hand.take(self.deck.deal())
			if self.hand.busted():
				self.state = GameState.FINISHED
				return ActionResult(self.state, self.hand, self.dealers_hand, 0)
			else:
				return ActionResult(self.state, self.hand, self.dealers_hand)

		elif action == PlayerAction.DOUBLE:
			if self.state != GameState.PLAYING: raise ValueError('Cannot DOUBLE when GameState is not PLAYING')
			if not self.hand.is_starting_hand(): raise ValueError('Cannot DOUBLE when not starting hand ')
			if wager == None: raise ValueError('Wager must be provided when action is DOUBLE')
			if wager <= 0 or wager > self.wager: raise ValueError('Wager must be positive but less than original wager')
			self.wager = self.wager + wager
			self.hand.take(self.deck.deal())
			if self.hand.busted():
				self.state = GameState.FINISHED
				return ActionResult(self.state, self.hand, self.dealers_hand, 0)
			else:
				return self.act(PlayerAction.STAY)