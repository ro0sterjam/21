from continuous_deck import Deck
from hand import Hand
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

	def __init__(self, state, hands, hand, dealers_hand, reward=None):
		self.state = state
		self.hands = hands
		self.hand = hand
		self.dealers_hand = dealers_hand
		self.reward = reward

class Blackjack:

	def __init__(self, deck=Deck(), state=GameState.FINISHED, dealers_hand=None, hands=None, hand=None):
		self.deck = deck
		self.state = state
		self.dealers_hand = dealers_hand
		self.hands = hands
		self.hand = hand

	def act(self, action, wager=None):
		if action == PlayerAction.BET:
			if self.state != GameState.FINISHED: raise ValueError('Cannot bet mid game')
			if wager == None: raise ValueError('Wager must be provided when action is BET')
			if wager <= 0: raise ValueError('Wager must be positive')
			self.state = GameState.PLAYING
			self.dealers_hand = Hand(self.deck.deal(), self.deck.deal())
			self.hands = [Hand(self.deck.deal(), wager)]
			self.hand = 0
			return ActionResult(self.state, self.hands, 0, self.dealers_hand)

		elif action == PlayerAction.STAY:
			if self.state != GameState.PLAYING: raise ValueError('Cannot STAY when GameState is not PLAYING')
			if self.hand + 1 < len(self.hands):
				self.hand = self.hand + 1
				return ActionResult(self.state, self.hands, self.hand, self.dealers_hand)
			while self.dealers_hand.best_val() < 17 and not self.dealers_hand.busted():
				self.dealers_hand.take(self.deck.deal())
			if self.dealers_hand.busted():
				self.state = GameState.FINISHED
				return ActionResult(self.state, self.hands, self.hand, self.dealers_hand, sum(map(lambda hand: hand.wager * 2, self.hands)))
			else:
				self.state = GameState.FINISHED
				reward = sum(map(lambda hand: 0 if self.dealers_hand.best_val() > hand.best_val() else hand.wager * 2 if hand.best_val() > self.dealers_hand.best_val() else hand.wager, self.hands))
				return ActionResult(self.state, self.hands, self.hand, self.dealers_hand, reward)

		elif action == PlayerAction.HIT:
			if self.state != GameState.PLAYING: raise ValueError('Cannot HIT when GameState is not PLAYING')
			self.hands[self.hand].take(self.deck.deal())
			if self.hands[self.hand].busted():
				if self.hand + 1 < len(self.hands):
					self.hand = self.hand + 1
					return ActionResult(self.state, self.hands, self.hand, self.dealers_hand)
				else:
					self.state = GameState.FINISHED
					return ActionResult(self.state, self.hands, self.hand, self.dealers_hand, 0)
			else:
				return ActionResult(self.state, self.hands, self.hand, self.dealers_hand)

		elif action == PlayerAction.DOUBLE:
			if self.state != GameState.PLAYING: raise ValueError('Cannot DOUBLE when GameState is not PLAYING')
			if not self.hands[self.hand].is_starting_hand(): raise ValueError('Cannot DOUBLE when not starting hand')
			if wager == None: raise ValueError('Wager must be provided when action is DOUBLE')
			if wager <= 0 or wager > self.hands[self.hand].wager: raise ValueError('Wager must be positive but not greater than original wager')
			self.hands[self.hand].wager = self.hands[self.hand].wager + wager
			self.hands[self.hand].take(self.deck.deal())
			if self.hands[self.hand].busted():
				if self.hand + 1 < len(self.hands):
					self.hand = self.hand + 1
					return ActionResult(self.state, self.hands, self.hand, self.dealers_hand)
				else:
					self.state = GameState.FINISHED
					return ActionResult(self.state, self.hands, self.hand, self.dealers_hand, 0)
			else:
				return self.act(PlayerAction.STAY)

		elif action == PlayerAction.SPLIT:
			if self.state != GameState.PLAYING: raise ValueError('Cannot SPLIT when GameState is not PLAYING')
			if not self.hands[self.hand].is_pair(): raise ValueError('Cannot SPLIT when not a pair')
			if wager == None: raise ValueError('Wager must be provided when action is DOUBLE')
			if wager != self.hands[self.hand].wager: raise ValueError('Wager must be equal to original wager')
			self.hands.append(Hand([self.hands[self.hand].cards.pop(), self.deck.deal()], wager))
			self.hands[self.hand].take(self.deck.deal())
			return ActionResult(self.state, self.hands, self.hand, self.dealers_hand)