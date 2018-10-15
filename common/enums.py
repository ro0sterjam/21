from enum import Enum

PlayerAction = Enum('PlayerAction', 'BET STAY HIT DOUBLE SPLIT')
GameState = Enum('GameState', 'PLAYING FINISHED')