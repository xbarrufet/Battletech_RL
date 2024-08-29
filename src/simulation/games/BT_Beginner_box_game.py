from dataclasses import dataclass
from enum import Enum
import math
import random

from simulation.model import mech_utils
from simulation.utils.utils import Axial, Facing, position_distance
import  simulation.utils.utils as utils
from simulation.model.board import Board 
from simulation.model.mech import Action, BattleMech, MovementDirection,Movement, RotatetDirection, MechState



PLAYER_1=0
PLAYER_2=1




class GamePhase(Enum):
    INITIAL_PHASE=0
    MOVEMENT_PHASE=1
    SHOOTING_PHASE=2



class BTBeginnerBoxGame:
    
    def __init__(self, board: Board, p1_mech: BattleMech, p2_mech: BattleMech,num_turns=5) -> None:
        self.board = board
        self.battle_mechs = [p1_mech,p2_mech]
        
        self.board.deploy_mech(p1_mech)
        self.board.deploy_mech(p2_mech)
        
        self.num_turns=num_turns 
        
        self.current_phase = GamePhase.INITIAL_PHASE
        self.player_movement_complete=[False,False]
        self.player_firing_complete=[False,False]


    def reset_turn(self):
        self.current_phase = GamePhase.INITIAL_PHASE
        self.player_movement_complete=[False,False]
        self.player_firing_complete=[False,False]
    
    def run_initiative_phase(self,forced_player:int=-1)->int:
        ''' start new turn, moves to MOVEMENT phase, return the owner of the initiative''' 
        if self.current_phase!=GamePhase.INITIAL_PHASE:
            raise f"Invalid action, start_turn is not valid in {self.current_phase.name}"   
        self.current_phase=GamePhase.MOVEMENT_PHASE
        self.player_movement_complete=[False,False]
        self.player_firing_complete=[False,False]
        if forced_player<0: 
            self.current_turn_initiative = random.choice([PLAYER_1,PLAYER_2])
        else:
            self.current_turn_initiative = forced_player
        self.current_player = self.current_turn_initiative
        return self.current_turn_initiative
     
    def move_to_firing_phase(self):
        self.current_phase=GamePhase.SHOOTING_PHASE
        self.current_player = self.current_turn_initiative
    
        self.current_phase=GamePhase.INITIAL_PHASE
        self.run_initiative_phase(forced_player=PLAYER_1)
            

    def run_movement_action(self,player:int, destination:Axial, end_facing:Facing, mov_type:Movement ):
        if self.current_phase!=GamePhase.MOVEMENT_PHASE:
            raise f"Invalid action, run_movement_action is not valid in {self.current_phase.name}"   
        if player!=self.current_player:
            raise f"Not valid player turn, received {player}, expected {self.current_player}"    
        if player!=self.current_player:
            raise f"{destination} is not a valid end position"    
        self.battle_mechs[player].position=destination
        self.battle_mechs[player].facing=end_facing
        self.battle_mechs[player].movementType=mov_type
        self.player_movement_complete[player]=True
        if not all(self.player_movement_complete):
            self.current_player =(player + 1) %2
        else:
            self.move_to_firing_phase()

    def get_allowed_movements(self, player):
        movements = {}
        mech = self.battle_mechs[player]
        movements[Movement.mv_walk] = self.board.allowed_movements(remaining_movement=mech.movement[Movement.mv_walk.value],
                                                                    current_cell=mech.position, 
                                                                    current_facing=mech.facing,
                                                                    cells={},
                                                                    back_allowed=True)
        movements[Movement.mv_run] = self.board.allowed_movements(remaining_movement=mech.movement[Movement.mv_run.value],
                                                                    current_cell=mech.position, 
                                                                    current_facing=mech.facing,
                                                                    cells={},
                                                                    back_allowed=False)
        movements[Movement.mv_jump]=self.board.allowed_jump_movements(jump_max_movement=mech.movement[Movement.mv_jump.value],
                                                                      current_cell=mech.position)
        return movements


class BTBeginnerBoxGameEnvironment:
    
    def __init__(self, game:BTBeginnerBoxGame, random_player2:bool=True) -> None:
        self.acum_rewards = [0,0]
        self.game = game
        self.obs_dim = 9
        self.random_player2=random_player2
        
        self.enc_tuple_int = {}
        self.enc_int_tuple = [0] * game.board.height*game.board.width*len(Facing)*len(Movement)
        self._encoding_tuple()
                        
    def _encoding_tuple(self):
        counter= 0
        for pos in self.game.board.cells.keys():
            for f in range(6):
                facing = Facing(f)
                for mv in range(3):
                    self.enc_tuple_int[(pos,facing,Movement(mv))]=counter
                    self.enc_int_tuple[counter]=(pos,facing,Movement(mv))
                    counter+=1
    
    
    
    def reset(self):
        self.acum_rewards = [0,0]
        self.game.reset_turn()
        first_player = self.game.run_initiative_phase(forced_player=PLAYER_1)
        mech1 = self.game.battle_mechs[first_player]
        mech2 = self.game.battle_mechs[(first_player+1)%2]
        d1, v1 = self.game.board.check_visibility(mech1.position,mech1.facing,mech2.position)
        d2, v2 = self.game.board.check_visibility(mech2.position,mech2.facing,mech1.position)
        return (self.build_observations(mech_player=mech1,mech_target=mech2,d1=d1,d2=d2,v1=v1,v2=v2), self.get_allowed_actions_bits(player=first_player))
    
    def run_action_return(self, player=PLAYER_1):
        mech_player = self.game.battle_mechs[player]
        mech_target = self.game.battle_mechs[(player+1)%2]
        d1, v1 = self.game.board.check_visibility(mech_player.position,mech_player.facing,mech_target.position)
        d2, v2 = self.game.board.check_visibility(mech_target.position,mech_target.facing,mech_player.position)
        return  (self.build_observations(mech_player=mech_player,mech_target=mech_target,d1=d1,d2=d2,v1=v1,v2=v2), self.get_allowed_actions_bits(player=player)),\
                self.build_reward(mech_player=mech_player,mech_target=mech_target,d1=d1,d2=d2,v1=v1,v2=v2), \
                self.build_is_done(), \
                self.build_info()
    
    
    def build_observations(self,mech_player:BattleMech, mech_target:BattleMech, d1:int,v1:int,d2:int,v2:int):
        
        obs = []
        obs.append(mech_player.facing.value)
        obs.append(mech_target.facing.value)
        obs.append(mech_player.position.q)
        obs.append(mech_player.position.r)
        obs.append(mech_player.movementType.value)
        obs.append(mech_target.movementType.value)
        obs.append(d1)
        obs.append(1 if utils.is_in_frontal_act(mech_player.position,mech_player.facing,mech_target.position) else 0)
        obs.append(1 if utils.is_in_frontal_act(mech_target.position,mech_target.facing,mech_player.position) else 0)
        
        return obs
        
    def build_reward(self,mech_player:BattleMech, mech_target:BattleMech, d1:int,v1:int,d2:int,v2:int,player:int=PLAYER_1):
        
        g1 = mech_player.gunner_skill
        g2 = mech_target.gunner_skill
        # r1 = table_range_modfier(d1)
        # r2 = table_range_modfier(d2)
        a1 = mech_utils.table_attacker_movement(mech_player.movementType)
        a2 = mech_utils.table_attacker_movement(mech_target.movementType)
        o1 = mech_utils.table_other_modifiers(v1)
        o2 = mech_utils.table_other_modifiers(v2)
        rew1 = (mech_utils.dice_2D6_prob(g1 + a1 + o1 ) -  mech_utils.dice_2D6_prob(g2 + a2 + o2))
        rew2 = (mech_utils.dice_2D6_prob(g2 + a2 + o2) -  mech_utils.dice_2D6_prob(g1 + a1 + o1))
        self.acum_rewards[player]+=rew1
        self.acum_rewards[(player+1)%2]+=rew2
        return rew1
        
    
    def build_is_done(self):
        base = 5
        return self.acum_rewards[0]>base or self.acum_rewards[1]>base
    
    def build_info(self):
        info = [0]*2
        info[0] = self.acum_rewards[0]
        info[1] = self.acum_rewards[1]
        return info
    
    def run(self,action:int, player:int) -> tuple:
        if player==self.game.current_player:
            pos, facing,mov_type = self.enc_int_tuple[action]
            action_valid = True
            self.game.run_movement_action(player=player,destination=pos,end_facing=facing,mov_type=mov_type)
            self.current_player =(player + 1) %2
            if self.random_player2 and self.game.current_player==PLAYER_2:
                self.run_random_movement(player=PLAYER_2)
            return self.run_action_return()
        else:
            raise f"Not valid player turn, received {player}, expected {self.current_player}"    
    
    def get_action_space(self):
        return len(self.enc_int_tuple)
    
    def run_random_movement(self, player:int):
        allowed_actions = self.game.get_allowed_movements(player=player)
        mov_type = random.choice([Movement.mv_walk,Movement.mv_run,Movement.mv_jump]) # movement types
        pos, facing = random.choice(list(allowed_actions[mov_type].keys()))
        self.game.run_movement_action(player=player,destination=pos,end_facing=facing,mov_type=mov_type)
        
    
    def get_allowed_actions_bits(self, player:int):
        allowed_actions = self.game.get_allowed_movements(player=player)
        ''' allwed_actions is a dictionay  [Movemnt][(cell, Facing)]=1'''
        bits = [0]*self.get_action_space()
        for mv,cells in allowed_actions.items():
            for position,facing in cells:
                position = self.enc_tuple_int[(position, facing, mv)]
                bits[position]=1
        return bits

    