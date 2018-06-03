from enum import Enum

PlayerAction = Enum('PlayerAction', 'BET STAY HIT DOUBLE')
GameState = Enum('GameState', 'PLAYING FINISHED')