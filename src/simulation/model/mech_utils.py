

from enum import Enum


class MechState(Enum):
    ST_READY_TO_MOVE=0
    ST_WALKING=1
    ST_RUNNING=2
    ST_MOVEMENT_COMPLETE = 10
    ST_READY_TO_FIRE = 21
    ST_FIRING_COMPLETE = 22
    ST_WAITING = 99



class Action(Enum):
    ACT_SELECT_NO_MOVEMENT = 0
    ACT_SELECT_WALK_MOVEMENT_TYPE = 1
    ACT_SELECT_RUN_MOVEMENT_TYPE = 2
    ACT_MOVE_FORWARD = 3
    ACT_MOVE_BACKWARD = 4
    ACT_ROTATE_LEFT = 5
    ACT_ROTATE_RIGHT = 6
    ACT_NO_MOVEMENT = 7
    ACT_FIRE_WEAPONS=8
    

            
allowed_state_actions =  {
    MechState.ST_READY_TO_MOVE:[Action.ACT_SELECT_RUN_MOVEMENT_TYPE,Action.ACT_SELECT_WALK_MOVEMENT_TYPE,Action.ACT_SELECT_NO_MOVEMENT ],
    MechState.ST_WALKING:[Action.ACT_MOVE_FORWARD,Action.ACT_MOVE_BACKWARD,Action.ACT_ROTATE_LEFT,Action.ACT_ROTATE_RIGHT,Action.ACT_NO_MOVEMENT],
    MechState.ST_RUNNING:[Action.ACT_MOVE_FORWARD,Action.ACT_ROTATE_LEFT,Action.ACT_ROTATE_RIGHT,Action.ACT_NO_MOVEMENT],
    MechState.ST_MOVEMENT_COMPLETE:[],
    MechState.ST_READY_TO_FIRE:[Action.ACT_FIRE_WEAPONS],
    MechState.ST_FIRING_COMPLETE:[]
}




class Location(Enum):
    loc_Head = 0
    loc_CenterTorso = 1
    loc_RightArm = 2
    loc_RightLeg = 3
    loc_RightTorso = 4
    loc_LeftArm = 5
    loc_LeftLeg = 6
    loc_LeftTorso = 7

class MovementType(Enum):
    mv_walk = 0
    mv_run = 1
    mv_jump = 2
    
class MovementDirection(Enum):
    md_forward = 0
    md_backward = -1

class RotatetDirection(Enum):
    rd_left = -1
    rd_right = 1



class Range(Enum):
     range_Short = 0
     range_Medium = 1
     range_Long = 2

def dice_2D6_prob(limit=12)->float:
    return max(0,(13-limit)* 1/12)

def dice_1D6_prob(limit=6)->float:
    return max(0,(6-limit)* 1/6)


def table_attacker_movement(movementType:MovementType)->int:
     match movementType:
          case MovementType.mv_walk:
               return 1
          case MovementType.mv_run:
               return 2
          case MovementType.mv_jump:
               return 3
          case _:
               return 0

def table_volley_hits(volley)-> int:
        if volley==2:
            return 1
        elif volley==5:
            return 3
        elif volley==6:
            return 4
        if volley==10:
            return 6
        if volley==10:
            return 9
        else:
             return 0

def table_target_movement(moved_hexes:int)->int:
        if moved_hexes>=10:
            return 4
        elif moved_hexes>=7:
            return 3
        elif moved_hexes>=5:
            return 2
        if moved_hexes>=3:
            return 1
        else:
             return 0

def table_other_modifiers(visibility:int)->int:
    return visibility

def table_range_modfier(distance:int,range:list[int])->int:
     if distance<range[Range.range_Short.value]:
          return 0
     elif distance<range[Range.range_Medium.value]:
          return 2
     elif distance<range[Range.range_Long.value]:
          return 4
     else:
          return 12
     