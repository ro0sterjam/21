from enum import Enum

class Card(Enum):

	def __new__(cls, *args, **kwds):
		value = len(cls.__members__) + 1
		obj = object.__new__(cls)
		obj._value_ = value
		return obj

	def __init__(self, display, val, alt_val=None):
		self.display = display
		self.val = val
		self.alt_val = alt_val

	def __str__(self):
		return self.display

	def __repr__(self):
		return self.__str__()

	ACE = 'A', 1, 11
	TWO = '2', 2
	THREE = '3', 3
	FOUR = '4', 4
	FIVE = '5', 5
	SIX = '6', 6
	SEVEN = '7', 7
	EIGHT = '8', 8
	NINE = '9', 9
	TEN = '10', 10
	JACK = 'J', 10
	QUEEN = 'Q', 10
	KING = 'K', 10