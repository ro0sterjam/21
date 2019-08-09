class Player:

	def __init__(self, bankroll):
		self.bankroll = bankroll

	def sit(self, seat):
		seat.seat(self)

	def leave(self, seat):
		seat.remove(self)

	def bet(self, seat, wager):
		if seat.actor != self: raise PlayerNotOccupyingSeatError()
		wager = self.bankroll.take(wager)
		try:
			seat.add_wager(wager)
		except:
			self.bankroll.fund(wager)
			raise

	def skip_round(self, seat):
		if seat.actor != self: raise PlayerNotOccupyingSeatError()
		seat.skip_round()

	def stay(self, hand):
		if hand.seat.actor != self: raise PlayerDoesNotOwnHandError()
		hand.stay()

	def hit(self, hand):
		if hand.seat.actor != self: raise PlayerDoesNotOwnHandError()
		hand.hit()

	def double(self, hand, wager):
		if hand.seat.actor != self: raise PlayerDoesNotOwnHandError()
		wager = self.bankroll.take(wager)
		try:
			hand.double(wager)
		except:
			self.bankroll.fund(wager)
			raise

	def split(self, hand):
		if hand.seat.actor != self: raise PlayerDoesNotOwnHandError()
		wager = self.bankroll.take(hand.wager)
		try:
			hand.split(wager)
		except:
			self.bankroll.fund(wager)
			raise