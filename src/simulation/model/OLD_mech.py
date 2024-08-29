# from typing import NamedTuple
# from dataclasses import dataclass
# from enum import Enum

# from simulation.model.mech_utils import Action, MechState, Movement, MovementDirection, RotatetDirection,allowed_state_actions
# from simulation.model.weapon import Weapon
# from simulation.utils.utils import Axial,Facing
# import simulation.utils.utils as utils
# from simulation.model.board import Board



# class OLD_Mech:
#     def __init__(self,mech_type: str, movement: list[int],weapons: list[Weapon], base_armor: list[int]):
#          self.mech_type=mech_type
#          self.movement=movement
#          self.weapons = weapons
#          self.base_armor = base_armor



# class OLD_BattleMech(OLD_Mech):
#     def __init__(self,mech_type: str, mech_id: str, movement: list[int],weapons: list[Weapon], base_armor: list[int] ,deployment_position:Axial,facing = 0):
#         Mech.__init__(self,mech_type=mech_type, movement=movement,weapons=weapons,base_armor=base_armor)
#         self.mech_id= mech_id
#         self.remaining_armor = base_armor
#         self.movementType=Movement.mv_steady
#         self.remaining_movement = 0
#         self.position = deployment_position
#         self.facing = Facing(facing)
#         self.current_state = MechState.ST_READY_TO_MOVE
#         self.traverssed_hexes=[deployment_position]
#         self.gunner_skill = 4
#         self.turn_damage_done=0
#         self.turn_damage_received=0
#         self.allowed_actions_list = []

#     def move_to_firing_phase(self):
#         self.current_state=MechState.ST_READY_TO_FIRE
#         self.turn_damage_done=0
#         self.turn_damage_received=0

#     def move_to_movement_phase(self):
#          self.current_state=MechState.ST_READY_TO_MOVE

#     def move_to_waiting(self):
#          self.current_state=MechState.ST_WAITING

#     def mech_turn_reset(self):
#         self.movementType=Movement.mv_steady
#         self.remaining_movement = 0
#         self.current_state=MechState.ST_READY_TO_MOVE
#         self.traverssed_hexes=[self.position]
       
    
#     def get_num_of_travessed_cells(self):
#          #remove the initial cell
#          return len(self.traverssed_hexes)-1
            
    
#     def start_move(self,mov_type:Movement):
#         self.movementType=mov_type
#         if mov_type!=Movement.mv_steady:
#             self.remaining_movement = self.movement[mov_type.value]
#         else:
#              self.remaining_movement = 0
    
#     def move_mech(self, direction:MovementDirection, board:Board):
#         ''' move mech 1 square back or forw in its current facing direction
#             direction: Movement direction, Forward or Backward
#             board: Board on the movement will be done
#         '''
#         facing = self.facing if direction == MovementDirection.md_forward else utils.back_facing(self.facing)
#         new_cell = board.get_neighbour_cell(self.position,facing)
#         movement_cost = new_cell.movement_needed()
#         current_cell = board.get_cell(self.position)
#         current_cell.occupied=False
#         self.position=new_cell.position
#         new_cell.occupied=True
#         self.remaining_movement -=movement_cost
#         if not new_cell.position in self.traverssed_hexes:
#              self.traverssed_hexes.append(new_cell.position)

            
#     def rotate_mech(self, rotateDirection:RotatetDirection):
        
#         self.facing = Facing((self.facing.value+rotateDirection.value) % 6)
#         self.remaining_movement -=1


#     def build_allowed_actions(self, board:Board):
#         allowed_actions=[]
#         match self.current_state:
#             case MechState.ST_READY_TO_MOVE:
#                   #allowed_actions.extend([Action.ACT_END_MOVEMENT,Action.ACT_SELECT_RUN_MOVEMENT_TYPE,Action.ACT_SELECT_WALK_MOVEMENT_TYPE])
#                   allowed_actions.extend([Action.ACT_SELECT_RUN_MOVEMENT_TYPE,Action.ACT_SELECT_WALK_MOVEMENT_TYPE,Action.ACT_SELECT_NO_MOVEMENT])
#             case MechState.ST_MOVEMENT_COMPLETE | MechState.ST_WAITING:
#                   allowed_actions=[]
#             case MechState.ST_RUNNING:
#                   #allowed_actions=[Action.ACT_END_MOVEMENT]
#                   allowed_actions=[Action.ACT_NO_MOVEMENT]
#                   if self.is_movement_allowed(MovementDirection.md_forward,board):
#                        allowed_actions.append(Action.ACT_MOVE_FORWARD)
#                   if self.remaining_movement>0:
#                       allowed_actions.extend([Action.ACT_ROTATE_LEFT, Action.ACT_ROTATE_RIGHT])
#             case MechState.ST_WALKING:
#                    #allowed_actions=[Action.ACT_END_MOVEMENT]
#                   allowed_actions=[Action.ACT_NO_MOVEMENT]
#                   if self.is_movement_allowed(MovementDirection.md_forward,board):
#                        allowed_actions.append(Action.ACT_MOVE_FORWARD)
#                   if self.is_movement_allowed(MovementDirection.md_backward,board):
#                        allowed_actions.append(Action.ACT_MOVE_BACKWARD)
#                   if self.remaining_movement>0:
#                      allowed_actions.extend([Action.ACT_ROTATE_LEFT, Action.ACT_ROTATE_RIGHT])  
#             case MechState.ST_READY_TO_FIRE:
#                   allowed_actions=[Action.ACT_FIRE_WEAPONS]    
#         self.allowed_actions_list=allowed_actions                
#         return allowed_actions
    
#     def is_action_allowed(self, action:Action):
#         return action in self.allowed_actions_list     

#     def is_movement_allowed(self, direction:MovementDirection, board:Board)->bool:
#         ''' check if movement is allowed
#             direction: Movement direction, Forward or Backward
#             board: Board on the movement will be done
#         '''
#         facing = self.facing if direction == MovementDirection.md_forward else utils.back_facing(self.facing)
#         is_valid = True
#         try:
#             new_cell = board.get_neighbour_cell(self.position,facing)
#             if new_cell!=None:
#                 if new_cell.occupied:
#                     is_valid= False
#                 movement_cost = new_cell.movement_needed()
#                 if movement_cost> self.remaining_movement:
#                     is_valid= False
#                 return is_valid
#             else:
#                  return False
#         except Exception as e:
#             print(e)
#             return False
        
        
#     def state_transition(self, action_done:Action):
#         match action_done:
#             case Action.ACT_SELECT_WALK_MOVEMENT_TYPE:
#                         self.current_state=MechState.ST_WALKING
#             case Action.ACT_SELECT_NO_MOVEMENT:
#                         self.current_state= MechState.ST_MOVEMENT_COMPLETE        
#             case Action.ACT_SELECT_RUN_MOVEMENT_TYPE:
#                         self.current_state=MechState.ST_RUNNING
#             case Action.ACT_MOVE_FORWARD | Action.ACT_MOVE_BACKWARD | Action.ACT_ROTATE_LEFT | Action.ACT_ROTATE_RIGHT | Action.ACT_NO_MOVEMENT:
#                         if self.remaining_movement==0:
#                             self.current_state= MechState.ST_MOVEMENT_COMPLETE
#             case Action.ACT_FIRE_WEAPONS:
#                         self.current_state=MechState.ST_FIRING_COMPLETE
            
#     def is_at_range(self,distance):
#         res = [0,0,0]
#         ranges = [w.weapon.weapon_range for w in self.mech_type.weapons]
#         for r in ranges:
#             for i in range(len(r)):
#                  res[i]=res[i]+1 if distance<r[i] else res[i]
#         return res
    
#     def fire_weapons(self,target_position:Axial,targe_travessed_cells:int, board:Board):
    
#         if utils.is_in_frontal_act(self.position, self.facing, target_position):
#               distance, blockers = board.check_visibility(a=self.position, b=target_position)
#               if blockers>=3:
#                    return 0
#               else:
#                 damage= 0
#                 for weapon in self.weapons:
#                      damage += weapon.fire_weapon(gunner_skill=self.gunner_skill, 
#                                                   distance=distance,
#                                                     attacker_movement_type=self.movementType,
#                                                     target_modifier=targe_travessed_cells, 
#                                                     terrain_modifier=blockers)
#                 damage = int(damage)
#                 self.turn_damage_done+=damage
#                 return damage
#         else:
#               return 0

#     def impact_received(self, damage):
#         damage=self.distribute_damage_in_armor(damage)      
#         self.turn_damage_received+=damage
        
#     def distribute_damage_in_armor(self, damage):
#          remaining_damage = damage
#          for t in range(len(self.remaining_armor)):
#               impact = min(self.remaining_armor[t],remaining_damage)
#               self.remaining_armor[t]-=impact
#               remaining_damage -=impact
#          return damage-remaining_damage
    
#     def is_destroyed(self):
#          return sum(self.remaining_armor)<=0