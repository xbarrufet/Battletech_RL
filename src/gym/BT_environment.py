import copy
from enum import Enum
import math

import pygame
from simulation.UI.hex_grid_board import HexGrid
from simulation.utils.utils import axial_to_oddq,position_distance
from simulation.games.BT_Beginner_box_game import  BTGame, GamePhase, MechState
from simulation.model.board import Board
from simulation.model.mech import Action, BattleMech, MovementType, MovementDirection


class BTEnvironment:

    def __init__(self, game:BTGame) -> None:
        self.game = game
        
    def reset(self)->any:
        pass
    
    def run(self,action:int, player:int) -> tuple[any,any,any]:
        pass
    
    def get_action_space(self):
        pass
    
    def get_observation_space(self):
        pass
            