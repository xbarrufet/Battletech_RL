from typing import NamedTuple
from dataclasses import dataclass
from enum import Enum

from simulation.model.mech_utils import Action, MechState, Movement, MovementDirection, RotatetDirection,allowed_state_actions
from simulation.model.weapon import Weapon
from simulation.utils.utils import Axial,Facing
import simulation.utils.utils as utils
from simulation.model.board import Board



class Mech:
    def __init__(self,mech_type: str, movement: list[int],weapons: list[Weapon], base_armor: list[int]):
         self.mech_type=mech_type
         self.movement=movement
         self.weapons = weapons
         self.base_armor = base_armor



class BattleMech(Mech):
    def __init__(self,mech_type: str, mech_id: str, movement: list[int],weapons: list[Weapon], base_armor: list[int] ,deployment_position:Axial,facing = 0):
        Mech.__init__(self,mech_type=mech_type, movement=movement,weapons=weapons,base_armor=base_armor)
        self.mech_id= mech_id
        self.remaining_armor = base_armor
        self.movementType=Movement.mv_steady
        self.remaining_movement = 0
        self.position = deployment_position
        self.former_position = deployment_position
        self.facing = Facing(facing)
        self.former_facing = deployment_position
        self.gunner_skill = 4
        self.turn_damage_done=0
        self.turn_damage_received=0
        self.allowed_actions_list = []

    def move_mech(self, movement_type: Movement,new_position:Axial, new_facing:Facing):
        self.former_position=self.position
        self.position=new_position
        self.former_facing=self.facing
        self.facing=new_facing,
        self.movementType=movement_type
    
            
    def is_at_range(self,distance):
        res = [0,0,0]
        ranges = [w.weapon.weapon_range for w in self.mech_type.weapons]
        for r in ranges:
            for i in range(len(r)):
                 res[i]=res[i]+1 if distance<r[i] else res[i]
        return res
    
    def fire_weapons(self,target_position:Axial, target_travessed_cells:int,visibility:int,distance:int):
    
        if utils.is_in_frontal_act(self.position, self.facing, target_position):
              if visibility>=3:
                   return 0
              else:
                damage= 0
                for weapon in self.weapons:
                     damage += weapon.fire_weapon(gunner_skill=self.gunner_skill, 
                                                  distance=distance,
                                                    attacker_movement_type=self.movementType,
                                                    target_modifier=targe_travessed_cells, 
                                                    terrain_modifier=blockers)
                damage = int(damage)
                self.turn_damage_done+=damage
                return damage
        else:
              return 0

    def impact_received(self, damage):
        damage=self.distribute_damage_in_armor(damage)      
        self.turn_damage_received+=damage
        
    def distribute_damage_in_armor(self, damage):
         remaining_damage = damage
         for t in range(len(self.remaining_armor)):
              impact = min(self.remaining_armor[t],remaining_damage)
              self.remaining_armor[t]-=impact
              remaining_damage -=impact
         return damage-remaining_damage
    
    def is_destroyed(self):
         return sum(self.remaining_armor)<=0