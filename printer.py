import pickle
from hand import Hand
from card import Card
from enums import PlayerAction

class Header:

	def __init__(self, label, hand):
		self.label = label
		self.hand = hand

hands_headers = [
	Header('A A', Hand([Card.ACE, Card.ACE])),
	Header('10 10', Hand([Card.TEN, Card.TEN])),
	Header('9 9', Hand([Card.NINE, Card.NINE])),
	Header('8 8', Hand([Card.EIGHT, Card.EIGHT])),
	Header('7 7', Hand([Card.SEVEN, Card.SEVEN])),
	Header('6 6', Hand([Card.SIX, Card.SIX])),
	Header('5 5', Hand([Card.FIVE, Card.FIVE])),
	Header('4 4', Hand([Card.FOUR, Card.FOUR])),
	Header('3 3', Hand([Card.THREE, Card.THREE])),
	Header('2 2', Hand([Card.TWO, Card.TWO])),
	Header('21', Hand([Card.TEN, Card.ACE])),
	Header('20', Hand([Card.TEN, Card.TEN])),
	Header('19', Hand([Card.TEN, Card.NINE])),
	Header('18', Hand([Card.TEN, Card.EIGHT])),
	Header('17', Hand([Card.TEN, Card.SEVEN])),
	Header('16', Hand([Card.TEN, Card.SIX])),
	Header('15', Hand([Card.TEN, Card.FIVE])),
	Header('14', Hand([Card.TEN, Card.FOUR])),
	Header('13', Hand([Card.TEN, Card.THREE])),
	Header('12', Hand([Card.TEN, Card.TWO])),
	Header('11', Hand([Card.TWO, Card.NINE])),
	Header('10', Hand([Card.TWO, Card.EIGHT])),
	Header('9', Hand([Card.TWO, Card.SEVEN])),
	Header('8', Hand([Card.TWO, Card.SIX])),
	Header('7', Hand([Card.TWO, Card.FIVE])),
	Header('6', Hand([Card.TWO, Card.FOUR])),
	Header('5', Hand([Card.TWO, Card.THREE])),
	Header('4', Hand([Card.TWO, Card.TWO])),
	Header('A 9', Hand([Card.ACE, Card.NINE])),
	Header('A 8', Hand([Card.ACE, Card.EIGHT])),
	Header('A 7', Hand([Card.ACE, Card.SEVEN])),
	Header('A 6', Hand([Card.ACE, Card.SIX])),
	Header('A 5', Hand([Card.ACE, Card.FIVE])),
	Header('A 4', Hand([Card.ACE, Card.FOUR])),
	Header('A 3', Hand([Card.ACE, Card.THREE])),
	Header('A 2', Hand([Card.ACE, Card.TWO]))
]

dealers_hands_headers = [
	Header('A', Hand([Card.ACE])),
	Header('10', Hand([Card.TEN])),
	Header('9', Hand([Card.NINE])),
	Header('8', Hand([Card.EIGHT])),
	Header('7', Hand([Card.SEVEN])),
	Header('6', Hand([Card.SIX])),
	Header('5', Hand([Card.FIVE])),
	Header('4', Hand([Card.FOUR])),
	Header('3', Hand([Card.THREE])),
	Header('2', Hand([Card.TWO]))
]

display_map = {
	PlayerAction.STAY: '\x1b[0;37;41m' + ' S ' + '\x1b[0m',
	PlayerAction.HIT: '\x1b[0;37;42m' + ' H ' + '\x1b[0m',
	PlayerAction.DOUBLE: '\x1b[0;37;43m' + ' D ' + '\x1b[0m',
	PlayerAction.SPLIT: '\x1b[0;37;44m' + ' P ' + '\x1b[0m'
}

def print_best_actions(avg_rewards):
	print(' ' * 7 + '  '.join(header.label for header in dealers_hands_headers))
	for hand_header in hands_headers:
		print('{0: <5}'.format(hand_header.label), end = ' ')
		for dealers_hands_header in dealers_hands_headers:
			best_action = max(avg_rewards[hand_header.hand][dealers_hands_header.hand], key=lambda action: avg_rewards[hand_header.hand][dealers_hands_header.hand][action])
			print(display_map[best_action], end = '')
		print('')

def save_avg_rewards(avg_rewards):
	with open('avg_rewards.pkl', 'wb') as f:
		pickle.dump(avg_rewards, f, pickle.HIGHEST_PROTOCOL)

def load_avg_rewards():
  with open('avg_rewards.pkl', 'rb') as f:
    return pickle.load(f)