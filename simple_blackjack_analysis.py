from hand import Hand
from card import Card
from enums import PlayerAction
from enums import GameState
from simple_blackjack import Blackjack
from printer import print_best_actions
from printer import save_avg_rewards
from printer import load_avg_rewards

hands = [
	Hand([Card.TEN, Card.TEN, Card.ACE]),
	Hand([Card.TEN, Card.FIVE, Card.FIVE]),
	Hand([Card.TEN, Card.NINE]),
	Hand([Card.TEN, Card.EIGHT]),
	Hand([Card.TEN, Card.SEVEN]),
	Hand([Card.TEN, Card.SIX]),
	Hand([Card.TEN, Card.FIVE]),
	Hand([Card.TEN, Card.FOUR]),
	Hand([Card.TEN, Card.THREE]),
	Hand([Card.TEN, Card.TWO]),
	Hand([Card.NINE, Card.TWO]),
	Hand([Card.ACE, Card.TEN]),
	Hand([Card.EIGHT, Card.TWO]),
	Hand([Card.ACE, Card.NINE]),
	Hand([Card.SEVEN, Card.TWO]),
	Hand([Card.ACE, Card.EIGHT]),
	Hand([Card.SIX, Card.TWO]),
	Hand([Card.ACE, Card.SEVEN]),
	Hand([Card.FIVE, Card.TWO]),
	Hand([Card.ACE, Card.SIX]),
	Hand([Card.FOUR, Card.TWO]),
	Hand([Card.ACE, Card.FIVE]),
	Hand([Card.THREE, Card.TWO]),
	Hand([Card.ACE, Card.FOUR]),
	Hand([Card.ACE, Card.THREE]),
	Hand([Card.ACE, Card.TWO]),
	Hand([Card.ACE, Card.ACE]),
	Hand([Card.TEN, Card.TEN]),
	Hand([Card.NINE, Card.NINE]),
	Hand([Card.EIGHT, Card.EIGHT]),
	Hand([Card.SEVEN, Card.SEVEN]),
	Hand([Card.SIX, Card.SIX]),
	Hand([Card.FIVE, Card.FIVE]),
	Hand([Card.FOUR, Card.FOUR]),
	Hand([Card.THREE, Card.THREE]),
	Hand([Card.TWO, Card.TWO])
]

dealers_hands = [
	Hand([Card.ACE]),
	Hand([Card.KING]),
	Hand([Card.QUEEN]),
	Hand([Card.JACK]),
	Hand([Card.TEN]),
	Hand([Card.NINE]),
	Hand([Card.EIGHT]),
	Hand([Card.SEVEN]),
	Hand([Card.SIX]),
	Hand([Card.FIVE]),
	Hand([Card.FOUR]),
	Hand([Card.THREE]),
	Hand([Card.TWO])
]

def running_avg(avg, n, val):
	return (1 - 1.0 / n) * avg + 1.0 / n * val

def calculate_avg_rewards():
	avg_rewards = {}
	for hand in hands:
		avg_rewards[hand] = {}
		for dealers_hand in dealers_hands:
			avg_rewards[hand][dealers_hand] = {
				PlayerAction.HIT: 0.0,
				PlayerAction.STAY: 0.0,
				PlayerAction.DOUBLE: 0.0 if hand.is_starting_hand() else -999,
				PlayerAction.SPLIT: 0.0 if hand.is_pair() else -999
			}
			for i in range(10000):
				hit_result = Blackjack(state=GameState.PLAYING, dealers_hand=Hand(dealers_hand.cards), hands=[Hand(hand.cards, 1)], hand=0).act(PlayerAction.HIT)
				reward = max(avg_rewards[hit_result.hands[hit_result.hand]][dealers_hand].values()) if hit_result.state == GameState.PLAYING else hit_result.reward - 1
				avg_rewards[hand][dealers_hand][PlayerAction.HIT] = running_avg(avg_rewards[hand][dealers_hand][PlayerAction.HIT], i + 1, reward)

				stay_result = Blackjack(state=GameState.PLAYING, dealers_hand=Hand(dealers_hand.cards), hands=[Hand(hand.cards, 1)], hand=0).act(PlayerAction.STAY)
				avg_rewards[hand][dealers_hand][PlayerAction.STAY] = running_avg(avg_rewards[hand][dealers_hand][PlayerAction.STAY], i + 1, stay_result.reward - 1)

				if hand.is_starting_hand():
					double_result = Blackjack(state=GameState.PLAYING, dealers_hand=Hand(dealers_hand.cards), hands=[Hand(hand.cards, 1)], hand=0).act(PlayerAction.DOUBLE, wager=1)
					avg_rewards[hand][dealers_hand][PlayerAction.DOUBLE] = running_avg(avg_rewards[hand][dealers_hand][PlayerAction.DOUBLE], i + 1, double_result.reward - 2)

				if hand.is_pair():
					split_result = Blackjack(state=GameState.PLAYING, dealers_hand=Hand(dealers_hand.cards), hands=[Hand(hand.cards, 1)], hand=0).act(PlayerAction.SPLIT, wager=1)
					reward = max(avg_rewards[split_result.hands[0]][dealers_hand].values()) + max(avg_rewards[split_result.hands[1]][dealers_hand].values())
					avg_rewards[hand][dealers_hand][PlayerAction.SPLIT] = running_avg(avg_rewards[hand][dealers_hand][PlayerAction.SPLIT], i + 1, reward)
	return avg_rewards

avg_rewards = load_avg_rewards()
# avg_rewards = calculate_avg_rewards()
print_best_actions(avg_rewards)
save_avg_rewards(avg_rewards)