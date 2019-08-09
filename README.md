# 21


Casino:
- Tables
- Players

Table:
- Players
- Seats
- DealerSeat
- Shoe
- State [WAITING, PLAYING, DONE]
- Actions:
	- add_player(player)					->			self.players.push(player)
	- remove_player(player)				->			self.players.remove(player)
  - settle(hand)								->			if hand.beats(self.dealer_seat.hand) then hand.seat.player.bankroll.fund(2 * hand.wager) + hand.seat.remove(hand)

Seat:
- Player
- Hands
- State [WAITING, SKIPPED, PLAYING, DONE]
- Actions:
  - seat_player(player)					->			self.player = player
  - remove_player(player)				->			self.player = None
  - skip_round()								->			no-op
  - add_bet(wager)							->			self.hands.push(Hand(wager))

DealerSeat:
- Dealer
- Hand
- Actions:
	- clear_hand()								->			self.hand.cards.clear()

Shoe:
- Cards
- State [READY, DONE]
- Actions:
	- pop_card()									->			return self.cards.pop()

Player:
- State [PLAYING, WATCHING]
- Actions:
	- watch_table(table)					->			table.add_player(self)
	- leave_table(table)					->			table.remove_player(self)
  - sit_in_seat(seat)						->			seat.seat_player(self)
  - rise_from_seat(seat)				->			seat.remove_player(self)
  - skip_round_for_seat(seat)		->			seat.skip_round()
  - bet_on_seat(seat, wager)		->			seat.add_bet(wager)
  - stay_on_hand(hand)					->			hand.stay()
  - hit_on_hand(hand)						->			hand.hit()
  - double_on_hand(hand, wager)	->			hand.double(wager)
  - split_on_hand(hand, wager)	->			hand.split(wager)

Hand:
- Wager
- Cards
- State [WAITING, READY, BUSTED, DONE]
- Actions:
	- take_card(card)							->			self.cards.push(card) + if self.is_busted(cards)
  - stay()											->			self.state = DONE
  - hit()												->			self.state = WAITING
  - double(wager)								->			self.wager += wager
  - 

Dealer:
- State [WAITING, DEALING, SETTLING, DONE]
- Actions:
  - take_from_shoe(shoe)				->			return shoe.pop_card()
  - flip_card(card)							->			card.flip()
  - deal_card(card, hand)				->			hand.take_card(card)
  - settle_hand(hand)						->			hand.seat.table.settle(hand)

Card:
- Value
- State [SHOWING, HIDDEN]