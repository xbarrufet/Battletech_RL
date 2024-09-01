from abc import ABC
import copy
from dataclasses import dataclass
from enum import Enum
import random
from typing import List

from simulation.model.board import Board
from simulation.model.mech import BattleMech
from simulation.model.mech_utils import MovementType
from simulation.model.weapon import Weapon
from simulation.utils.utils import Axial, Facing


PLAYER_1=0
PLAYER_2=1


class BattleLogEntryType(Enum):
    log_move=1
    log_fire=2
    log_start_phase=3
    log_complete_phase=4
    log_end_phase=5
    log_start_turn=6
    log_end_turn=7
    log_mech_destroyed=8
    log_end_game=9


@dataclass
class BattleLogEntry:
    log_type:BattleLogEntryType
    log_params = dict[str,any]


@dataclass
class MoveAction:
    mech:BattleMech
    target_position:Axial
    target_facing:Facing
    movement_type:MovementType

class GamePhase(Enum):
    INITIAL_PHASE=0
    MOVEMENT_PHASE=1
    SHOOTING_PHASE=2
    END_PHASE=3
    


@dataclass
class GameStatus:
    mechs:list
    log:list[BattleLogEntry]
    current_turn:int
    current_phase:GamePhase
    current_player:int


log_entry_type = "EntryType" 

log_entry_move_mech="mech"   
log_entry_move_target_location="target_location"   
log_entry_move_target_face="target_face"   

log_entry_fire_mech="mech"  
log_entry_fire_target_mech="target_mech"   
log_entry_fire_weapon="weapon"   
log_entry_fire_GATOR="GATOR"   
log_entry_fire_damage="damage"

log_entry_mech_destroyed_mech="mech"   
log_entry_mech_destroyed_player="player"

log_entry_turn="turn"

log_entry_phase="phase"
   

def generate_move_action_log_entry(mech:BattleMech, target_location:Axial, target_face:Facing):
    res = {}
    res[log_entry_type] = BattleLogEntryType.log_move
    res[log_entry_move_mech]=mech
    res[log_entry_move_target_location]=target_location
    res[log_entry_move_target_face]=target_face
    return res

def generate_fire_action_log_entry(mech:BattleMech,mech_target:BattleMech, weapon:Weapon, damage:int, GATOR:list[int]):
    res = {}
    res[log_entry_type] = BattleLogEntryType.log_fire
    res[log_entry_fire_mech]=mech
    res[log_entry_fire_target_mech]=mech_target
    res[log_entry_fire_weapon]=weapon
    res[log_entry_fire_damage]=damage
    res[log_entry_fire_GATOR]=GATOR
    return res

def generate_mech_destroyed_log_entry(mech:BattleMech,player:int):
    res = {}
    res[log_entry_type] = BattleLogEntryType.log_mech_destroyed
    res[log_entry_mech_destroyed_mech]=mech
    res[log_entry_mech_destroyed_player]=player
    return res



def generate_start_turn_log_entry(turn:int):
    res = {}
    res[log_entry_type] = BattleLogEntryType.log_start_turn
    res[log_entry_turn]=turn
    return res

def generate_end_turn_log_entry(turn:int):
    res = {}
    res[log_entry_type] = BattleLogEntryType.log_end_turn
    res[log_entry_turn]=turn
    return res


def generate_start_phase_log_entry(phase:GamePhase):
    res = {}
    res[log_entry_type] = BattleLogEntryType.log_start_phase
    res[log_entry_phase]=phase
    return res

def generate_complete_phase_log_entry(phase:GamePhase):
    res = {}
    res[log_entry_type] = BattleLogEntryType.log_complete_phase
    res[log_entry_phase]=phase
    return res


def generate_end_phase_log_entry(phase:GamePhase):
    res = {}
    res[log_entry_type] = BattleLogEntryType.log_end_phase
    res[log_entry_phase]=phase
    return res

    

class BTGame(ABC):
    
    def __init__(self, board:Board, p1_mechs:list[BattleMech],p2_mechs:list[BattleMech], max_turns:int):
        self.board = board
        self.original_mechs =[copy.deepcopy(p1_mechs),copy.deepcopy(p2_mechs)]
        self.player_mechs=[dict([(mech.mech_id, mech) for mech in p1_mechs]),dict([(mech.mech_id, mech) for mech in p2_mechs])]
        self.max_turns = max_turns
        self.has_mech_alrady_moved = [{},{}]
        self.has_weapon_alrady_fired = [{},{}]
        
        for player in [PLAYER_1,PLAYER_2]:
           for mech in self.get_player_all_mechs(player):
                 board.deploy_mech(mech) 
                 self.has_mech_alrady_moved[player][mech.mech_id]=False
                 for weapon in mech.weapons:
                     self.has_weapon_alrady_fired[player][weapon.weapon_id]=False
        self.reset_game()
        
            
    
    def reset_game(self):
        p1_mechs,p2_mechs = copy.deepcopy(self.original_mechs[PLAYER_1]),copy.deepcopy(self.original_mechs[PLAYER_2])
        self.player_mechs = [dict([(mech.mech_id, mech) for mech in p1_mechs]),dict([(mech.mech_id, mech) for mech in p2_mechs])]
        self.log = []
        self.current_phase = GamePhase.INITIAL_PHASE
        self.current_turn = 0
        self.current_turn_initiative=-1
        self.phases_completed = dict([(phase, False) for phase in GamePhase])   
        self.has_mech_alrady_moved=  [{mech_id: False for mech_id in self.has_mech_alrady_moved[PLAYER_1]},{mech_id: False for mech_id in self.has_mech_alrady_moved[PLAYER_2]}]
        self.has_weapon_alrady_fired=  [{weapon_id: False for weapon_id in self.has_weapon_alrady_fired[PLAYER_1]},{weapon_id: False for weapon_id in self.has_weapon_alrady_fired[PLAYER_2]}]    
            
        
    def get_player_all_mechs(self,player: int)->list[BattleMech]:
       return list(self.player_mechs[player].values())
    
    def get_player_mech(self, player:int, mech_id:str)->BattleMech:
        if mech_id not in self.player_mechs[player]:
            raise f"{mech_id} mech dosn't exist in player army"
        else:
            return self.player_mechs[player][mech_id]
    
    
    def is_all_mechs_already_moved(self):
        res = True
        for player in range(2):
            res =res and  all(list(self.has_mech_alrady_moved[player].values()))
        return res
    
    def get_board(self)->Board:
        return self.board
    
    def is_phase_completed(self):
        return self.phases_completed[self.current_phase]
    
    
    def complete_current_player_phase(self, next_player=-1):
        if next_player<0:
            next_player = self.get_next_player()
        self.current_player=next_player
        
    def complete_current_phase(self):
        self.phases_completed[self.current_phase]=True
        self.entry_log(generate_complete_phase_log_entry(self.current_phase))
        
    def complete_current_phase_and_start_next(self):
        self.complete_current_phase()
        self.next_phase()
            
    def next_phase(self):
        if not self.is_phase_completed():
            raise f"Phase {self.current_phase.name} is not completed"
        self.entry_log(generate_end_phase_log_entry(self.current_phase))
        self.current_phase=GamePhase(min(3, self.current_phase.value+1))
        self.current_player = self.current_turn_initiative
        self.entry_log(generate_start_phase_log_entry(self.current_phase))

    def next_turn(self):
        self.entry_log(generate_end_turn_log_entry(self.current_turn))
        self.phases_completed = dict([(phase, False) for phase in GamePhase])
        self.has_mech_alrady_moved=  [{mech_id: False for mech_id in self.has_mech_alrady_moved[PLAYER_1]},{mech_id: False for mech_id in self.has_mech_alrady_moved[PLAYER_2]}]
        self.has_weapon_alrady_fired=  [{weapon_id: False for weapon_id in self.has_weapon_alrady_fired[PLAYER_1]},{weapon_id: False for weapon_id in self.has_weapon_alrady_fired[PLAYER_2]}]
        self.entry_log(generate_start_turn_log_entry(self.current_turn))
        self.current_phase = GamePhase.INITIAL_PHASE
        self.entry_log(generate_start_phase_log_entry(self.current_phase))
        self.current_turn+=1
   
    def entry_log(self,entry:BattleLogEntry):
        self.log.append(entry)
    
    def run_move_action(self,player:int, action:MoveAction):
        if self.current_phase!=GamePhase.MOVEMENT_PHASE:
            raise Exception(f"Invalid action, run_movement_action is not valid in {self.current_phase.name}")   
        if player!=self.current_player:
            raise  Exception(f"Not valid player turn, received {player}, expected {self.current_player}")    
        if player!=self.current_player:
            raise Exception( f"{action.target_position} is not a valid end position")    
        if self.has_mech_alrady_moved[player][action.mech.mech_id]:
            raise  Exception(f"Mech {action.mech.mech_id} has already moved")    
        action.mech.position=action.target_position
        action.mech.facing=action.target_facing
        action.mech.movementType=action.movement_type
        self.has_mech_alrady_moved[player][action.mech.mech_id]=True
        if self.is_all_mechs_already_moved():
            self.complete_current_phase_and_start_next()
        elif all(list(self.has_mech_alrady_moved[player].values())):
            self.complete_current_player_phase()
        self.entry_log(generate_move_action_log_entry(action.mech, target_location=action.target_position, target_face=action.target_facing))
    
    
    def run_initative_action(self,forced_player=-1):
        if forced_player<0: 
            self.current_turn_initiative = random.choice([PLAYER_1,PLAYER_2])
        else:
            self.current_turn_initiative = forced_player
        self.current_player = self.current_turn_initiative
        self.complete_current_phase_and_start_next()
        return self.current_player
        
    def run_end_turn_action(self):
        self.complete_current_phase()
        self.next_turn()
    
    def get_game_status(self):
        return GameStatus(mechs=self.player_mechs,log=self.log,current_turn=self.current_turn, current_phase=self.current_phase, current_player=self.current_player)

    def get_next_player(self,player:int=-1)->int:
        if player<0:
            player=self.current_player
        return (player + 1) %2