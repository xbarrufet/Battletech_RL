from dataclasses import dataclass
from enum import Enum
import math
import random

from simulation.games.BTGame import PLAYER_1, PLAYER_2, BTGame, GamePhase, MoveAction
from simulation.model import mech_utils
from simulation.utils.utils import Axial, Facing, position_distance
import  simulation.utils.utils as utils
from simulation.model.board import Board 
from simulation.model.mech import Action, BattleMech, MovementDirection,MovementType, RotatetDirection, MechState



class BTBeginnerBoxGame(BTGame):
    
    def __init__(self, board: Board, p1_mech: BattleMech, p2_mech: BattleMech,max_turns=5) -> None:
        super().__init__(board=board,p1_mechs=[p1_mech],p2_mechs=[p2_mech],max_turns=max_turns)

    
    
    def get_allowed_movements(self, player):
        all_player_mech_movements = {}
        for mech in self.player_mechs[player].values():
            movements={}
            movements[MovementType.mv_walk] = self.board.allowed_movements(remaining_movement=mech.movement[MovementType.mv_walk.value],
                                                                        distance_from_origin=0,
                                                                        current_cell=mech.position, 
                                                                        current_facing=mech.facing,
                                                                        cells={},
                                                                        back_allowed=True)
            movements[MovementType.mv_run] = self.board.allowed_movements(remaining_movement=mech.movement[MovementType.mv_run.value],
                                                                        distance_from_origin=0,
                                                                        current_cell=mech.position, 
                                                                        current_facing=mech.facing,
                                                                        cells={},
                                                                        back_allowed=False)
            movements[MovementType.mv_jump]=self.board.allowed_jump_movements(jump_max_movement=mech.movement[MovementType.mv_jump.value],
                                                                        current_cell=mech.position)
            all_player_mech_movements[mech.mech_id] =movements
        return all_player_mech_movements


# class BTBeginnerBoxGameEnvironment:
    
#     def __init__(self, game:BTBeginnerBoxGame, random_player2:bool=True) -> None:
#         self.acum_rewards = [0,0]
#         self.game = game
#         self.obs_dim = 9
#         self.random_player2=random_player2
        
#         self.enc_tuple_int = {}
#         self.enc_int_tuple = [0] * game.board.height*game.board.width*len(Facing)*len(MovementType)
#         self._encoding_tuple()
                        
#     def _encoding_tuple(self):
#         counter= 0
#         for pos in self.game.board.cells.keys():
#             for f in range(6):
#                 facing = Facing(f)
#                 for mv in range(3):
#                     self.enc_tuple_int[(pos,facing,MovementType(mv))]=counter
#                     self.enc_int_tuple[counter]=(pos,facing,MovementType(mv))
#                     counter+=1
    
    
    
#     def reset(self):
#         super().reset()
#         self.acum_rewards = [0,0]
#         self.game.reset_turn()
#         first_player = self.game.run_initiative_phase(forced_player=PLAYER_1)
#         gameStatus =self.game.get_game_status()
#         mech1 = gameStatus.mechs[first_player][0]
#         mech2 =  gameStatus.mechs[self.game.get_next_player(first_player)][0]
#         d1, v1 = self.game.board.check_visibility(mech1.position,mech1.facing,mech2.position)
#         d2, v2 = self.game.board.check_visibility(mech2.position,mech2.facing,mech1.position)
#         return (self.build_observations(mech_player=mech1,mech_target=mech2,d1=d1,d2=d2,v1=v1,v2=v2), self.get_allowed_actions_bits(player=first_player))
    
#     def run_action_return(self, player=PLAYER_1):
#         gameStatus =self.game.get_game_status()
#         mech_player = gameStatus.mechs[player][0]
#         mech_target =  gameStatus.mechs[self.game.get_next_player(player)][0]
#         d1, v1 = self.game.board.check_visibility(mech_player.position,mech_player.facing,mech_target.position)
#         d2, v2 = self.game.board.check_visibility(mech_target.position,mech_target.facing,mech_player.position)
#         return  (self.build_observations(mech_player=mech_player,mech_target=mech_target,d1=d1,d2=d2,v1=v1,v2=v2), self.get_allowed_actions_bits(player=player)),\
#                 self.build_reward(mech_player=mech_player,mech_target=mech_target,d1=d1,d2=d2,v1=v1,v2=v2), \
#                 self.build_is_done(), \
#                 self.build_info()
    
    
#     def build_observations(self,mech_player:BattleMech, mech_target:BattleMech, d1:int,v1:int,d2:int,v2:int):
        
#         obs = []
#         obs.append(mech_player.facing.value)
#         obs.append(mech_target.facing.value)
#         obs.append(mech_player.position.q)
#         obs.append(mech_player.position.r)
#         obs.append(mech_player.movementType.value)
#         obs.append(mech_target.movementType.value)
#         obs.append(d1)
#         obs.append(1 if utils.is_in_frontal_act(mech_player.position,mech_player.facing,mech_target.position) else 0)
#         obs.append(1 if utils.is_in_frontal_act(mech_target.position,mech_target.facing,mech_player.position) else 0)
        
#         return obs
        
#     def build_reward(self,mech_player:BattleMech, mech_target:BattleMech, d1:int,v1:int,d2:int,v2:int,player:int=PLAYER_1):
        
#         g1 = mech_player.gunner_skill
#         g2 = mech_target.gunner_skill
#         # r1 = table_range_modfier(d1)
#         # r2 = table_range_modfier(d2)
#         a1 = mech_utils.table_attacker_movement(mech_player.movementType)
#         a2 = mech_utils.table_attacker_movement(mech_target.movementType)
#         o1 = mech_utils.table_other_modifiers(v1)
#         o2 = mech_utils.table_other_modifiers(v2)
#         rew1 = (mech_utils.dice_2D6_prob(g1 + a1 + o1 ) -  mech_utils.dice_2D6_prob(g2 + a2 + o2))
#         rew2 = (mech_utils.dice_2D6_prob(g2 + a2 + o2) -  mech_utils.dice_2D6_prob(g1 + a1 + o1))
#         self.acum_rewards[player]+=rew1
#         self.acum_rewards[(player+1)%2]+=rew2
#         return rew1
        
    
#     def build_is_done(self):
#         base = 5
#         return self.acum_rewards[0]>base or self.acum_rewards[1]>base
    
#     def build_info(self):
#         info = [0]*2
#         info[0] = self.acum_rewards[0]
#         info[1] = self.acum_rewards[1]
#         return info
    
#     def run(self,action:int, player:int) -> tuple:
#         ''' TODO tipus de accio depend de la fase on estiguis'''
#         if player==self.game.current_player:
#             if self.game.current_phase==GamePhase.MOVEMENT_PHASE:
#                 return self.run_movement_action(action, player)
#         else:
#             raise f"Not valid player turn, received {player}, expected {self.current_player}"    
    
#     def run_movement_action(self, action:int, player:int) -> tuple:
#         pos, facing,mov_type = self.enc_int_tuple[action]
#         mech_player = self.game.get_game_status().mechs[player][0]
#         self.game.run_move_action(action=MoveAction(mech=mech_player,target_position=pos,target_facing=facing,movement_type=mov_type))
#         return self.run_action_return()
    
    
#     def get_action_space(self):
#         return len(self.enc_int_tuple)    
    
#     def get_allowed_actions_bits(self, player:int):
#         allowed_actions = self.game.get_allowed_movements(player=player)
#         ''' allwed_actions is a dictionay  [Movemnt][(cell, Facing)]=1'''
#         bits = [0]*self.get_action_space()
#         for mv,cells in allowed_actions.items():
#             for position,facing in cells:
#                 position = self.enc_tuple_int[(position, facing, mv)]
#                 bits[position]=1
#         return bits

    