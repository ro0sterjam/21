import sys
sys.path.append("..")

from common.continuous_deck import Deck
from common.hand import Hand
from common.enums import GameState, PlayerAction

class Seat:

	def __init__(self, player=None, hands=[], wager=0, state=SeatState.EMPTY, rules=BasicSeatRules()):
		self.player = player
		self.hands = hands
		self.wager = wager
		self.state = state
		self.rules = rules

	def seat(self, player):
		if self.player != None: raise SeatNotAvailableError()
		self.player = player

	def remove(self, player):
		if self.player != player: raise PlayerNotOccupyingSeatError()

	def add_wager(self, wager):
		if len(hands) != 0: raise IllegalSeatState()
		self.rules.verify_wager(wager)
		self.wager = wager

	def skip_round(self):
		


