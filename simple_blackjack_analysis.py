import numpy as np
from hand import Hand
from card import Card
from enums import PlayerAction
from enums import GameState
from simple_blackjack import Blackjack
from printer import print_best_actions

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
	Hand([Card.TWO, Card.TWO]),
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
	Hand([Card.THREE, Card.THREE])
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

avg_rewards = {}

def running_avg(avg, n, val):
	return (1 - 1.0 / n) * avg + 1.0 / n * val

for hand in hands:
	avg_rewards[hand] = {}
	for dealers_hand in dealers_hands:
		avg_rewards[hand][dealers_hand] = {
			PlayerAction.HIT: 0.0,
			PlayerAction.STAY: 0.0,
			PlayerAction.DOUBLE: 0.0 if hand.is_starting_hand() else -999
		}
		for i in range(10000):
			hit_result = Blackjack(state=GameState.PLAYING, dealers_hand=Hand(dealers_hand.cards), hand=Hand(hand.cards), wager=1).act(PlayerAction.HIT)
			reward = max(avg_rewards[hit_result.hand][dealers_hand].values()) if hit_result.state == GameState.PLAYING else hit_result.reward - 1
			avg_rewards[hand][dealers_hand][PlayerAction.HIT] = running_avg(avg_rewards[hand][dealers_hand][PlayerAction.HIT], i + 1, reward)

			stay_result = Blackjack(state=GameState.PLAYING, dealers_hand=Hand(dealers_hand.cards), hand=Hand(hand.cards), wager=1).act(PlayerAction.STAY)
			avg_rewards[hand][dealers_hand][PlayerAction.STAY] = running_avg(avg_rewards[hand][dealers_hand][PlayerAction.STAY], i + 1, stay_result.reward - 1)

			if hand.is_starting_hand():
				double_result = Blackjack(state=GameState.PLAYING, dealers_hand=Hand(dealers_hand.cards), hand=Hand(hand.cards), wager=1).act(PlayerAction.DOUBLE, wager=1)
				avg_rewards[hand][dealers_hand][PlayerAction.DOUBLE] = running_avg(avg_rewards[hand][dealers_hand][PlayerAction.DOUBLE], i + 1, double_result.reward - 2)

print_best_actions(avg_rewards)