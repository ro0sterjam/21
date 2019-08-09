from common.card import Card
from common.enums import PlayerAction

class Hand:

	def __init__(self, cards = [], wager=None):
		self.cards = cards.copy()
		self.wager = wager

	def hit(self, card):
		if self.is_busted(): raise ValueError('Cannot hit a busted hand')
		return Hand(self.cards + [card], self.wager)

	def double(self, card, wager):
		if not self.is_starting_hand(): raise ValueError('Cannot double when not starting hand')
		if wager == None: raise ValueError('Wager must be provided when doubling')
		if wager <= 0 or wager > self.wager: raise ValueError('Wager must be positive but not greater than original wager when doubling')
		return Hand(self.cards + [card], self.wager + wager)

	def split(self, cards, wager):
		if not self.is_pair(): raise ValueError('Cannot split when not a pair')
		if wager != self.wager: raise ValueError('Wager must be equal to original wager when splitting')
		if len(cards) != 2: raise ValueError('Must provide 2 cards for the new hands when splitting')
		return [Hand([self.cards[0], cards[0]], self.wager), Hand([self.cards[1], cards[1]], wager)]

	def val(self):
		return sum(card.val for card in self.cards)

	def alt_val(self):
		val = self.val()
		return val + 10 if val < 12 and Card.ACE in self.cards else None

	def best_val(self):
		return self.alt_val() or self.val()

	def is_busted(self):
		return self.best_val() > 21

	def is_starting_hand(self):
		return len(self.cards) == 2

	def is_pair(self):
		return self.is_starting_hand() and self.cards[0] == self.cards[1]

	def can_perform_action(self, action):
		return action == PlayerAction.STAY \
			or (action == PlayerAction.HIT and not self.is_busted()) \
			or (action == PlayerAction.DOUBLE and self.is_starting_hand()) \
			or (action == PlayerAction.SPLIT and self.is_pair())

	def __str__(self):
		return str(self.cards)

	def __repr__(self):
		return self.__str__()

	def __hash__(self):
		return self.best_val()

	def __eq__(self, other):
		return self.best_val() == other.best_val() and self.alt_val() == other.alt_val() and self.is_pair() == other.is_pair()