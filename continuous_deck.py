import random
from card import Card

'''
Simple implementation of a Deck of infinite cards with constant unchanging equal distribution
'''
class Deck:

	def __init__(self):
		self.__deck = [Card.TWO, Card.THREE, Card.FOUR, Card.FIVE, Card.SIX, Card.SEVEN, Card.EIGHT, Card.NINE, Card.TEN, Card.JACK, Card.QUEEN, Card.KING, Card.ACE]

	def deal(self):
		return random.choice(self.__deck)