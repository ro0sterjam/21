from card import Card

class Hand:

	def __init__(self, cards = []):
		self.cards = cards.copy()

	def take(self, card):
		self.cards.append(card)

	def val(self):
		return sum(card.val for card in self.cards)

	def alt_val(self):
		val = self.val()
		return val + 10 if val < 12 and Card.ACE in self.cards else None

	def best_val(self):
		return self.alt_val() or self.val()

	def busted(self):
		return self.best_val() > 21

	def is_starting_hand(self):
		return len(self.cards) == 2

	def is_pair(self):
		return self.is_starting_hand() and self.cards[0] == self.cards[1]

	def __str__(self):
		return str(self.cards)

	def __repr__(self):
		return self.__str__()

	def __hash__(self):
		return self.best_val()

	def __eq__(self, other):
		return self.best_val() == other.best_val() and self.alt_val() == other.alt_val() and self.is_pair() == other.is_pair()