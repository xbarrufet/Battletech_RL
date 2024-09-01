from dataclasses import dataclass
from enum import Enum
import math
from typing import Dict
import uuid
import simulation.utils.utils as utils
from simulation.utils.utils import Axial, Facing
    


class CellType(Enum):
    cell_Clear = 0
    cell_LightWood = 1
    cell_HeavyWood = 2


class Cell:
    def __init__(self,position:Axial,elevation:int, cell_type:CellType) -> None:
        self.position=position
        self.elevation=elevation
        self.cell_type=cell_type
        self.occupied = False


    def set_occupied(self, value:bool):
        self.occupied=value

    def movement_needed(self):
        if self.cell_type==CellType.cell_Clear:
            return 1
        elif self.cell_type==CellType.cell_LightWood:
            return 2
        else:
            return 3


class Board:
    def __init__(self, width: int, height: int, cells: list[str]) -> None:
         self.width = width
         self.height = height
         self.cells = {}
         self.evaluated_cells={}
         cells_counter = 0
         for y in range(self.height):
            r=y
            for q in range( self.width):
                if q>0 and  q%2==0:
                    r-=1
                cell_str = cells[cells_counter]
                position = Axial(q,r)
                self.cells[position] = Cell(position, int(cell_str[0]), CellType(int(cell_str[1])))
                cells_counter+=1
         self.evaluated_cells = self.evaluate_board_positions()
    
    def deploy_mech(self,a:Axial)->None:
        if self.is_valid_cell_position(a):
            cell = self.get_cell(a)
            cell.occupied=True


    def is_valid_cell_position(self, position:Axial):
        return position in self.cells.keys()


    def get_cell(self, position:Axial) -> Cell:
        if not self.is_valid_cell_position(position):
            raise ValueError(f"({position}) is not a valid cell coord")
        else:
            return self.cells[position]
 
    def get_neighbour_cell(self, position:Axial, facing:Facing):
        neibourgh = utils.get_neighbour_position(position, facing)
        if self.is_valid_cell_position(neibourgh):
            return self.get_cell(neibourgh)
        else:
            return None
        
    def check_visibility(self, a:Axial, facing:Facing,b:Axial)->tuple[int,int]:
            line = utils.get_line(a,b)
            visibility = 0
            if utils.is_in_frontal_act(a,facing_a=facing,b=b):
                for cell_position in line:
                    if self.is_valid_cell_position(cell_position):
                        cell = self.get_cell(cell_position)
                        visibility+=cell.cell_type.value
                    else:
                        return (-1,25)
            else:
                visibility=25
            return (len(line),visibility)    
    
    def check_visibility_line(self, a:Axial, b:Axial)->Dict[Axial, tuple[int,int]]:
        line = utils.get_line(a,b)
        res = {}
        visibility = 0
        for cell_position in line:
            if self.is_valid_cell_position(cell_position):
                cell = self.get_cell(cell_position)
                visibility+=cell.cell_type.value
                res[b]=visibility
            else:
                res[b]=(-1,-1)
        return res    

    def cell_distance(a:Axial,b:Axial)->float:
        return utils.position_distance(a,b)


    def get_forest_map(self):
        forest = [[0] * self.width for _ in range(self.height)]
        for axial in self.cells.keys():
            odd= utils.axial_to_oddq(axial)
            forest[odd[1]][odd[0]]=self.get_cell(axial).cell_type.value
        return forest
    
    
    def get_board_border_cells(self)->list[Axial]:        
        border_cells =set()
        border_cells.update([Axial(0,r) for r in range(self.height)])
        border_cells.update([Axial(self.width,r) for r in range(self.height)])
        border_cells.update([Axial(self.width,-q) for q in range(self.width)])
        border_cells.update([Axial(self.width, self.height-q) for q in range(self.width)])
        return list(border_cells)
    
    def evaluate_board_positions(self):
        border_cell  = self.get_board_border_cells()
        #result = Dict[Axial,Dict[Axial, tuple[int,int]]:]
        result = {}
        for a in self.cells.keys():
            cell_result = Dict[Axial, tuple[int,int]]
            for b in border_cell:
                cell_result.update(self.check_visibility_line(a,b))
            result[a]=cell_result
        return result        
        
    def allowed_movements(self, remaining_movement:int, distance_from_origin:int,current_cell:Axial, current_facing:Facing,cells:Dict, back_allowed:bool)->Dict:
        if remaining_movement==0:
            if not (current_cell, current_facing) in cells:
                cells[(current_cell, current_facing)]=distance_from_origin
        elif remaining_movement>0:
            if not  (current_cell, current_facing) in cells:
                cells[(current_cell, current_facing)]=distance_from_origin
            face_left = Facing((current_facing.value-1)% 6)
            face_right =Facing((current_facing.value+1)% 6)
            if not  (current_cell, face_left) in cells:
                cells =  self.allowed_movements( remaining_movement=remaining_movement-1,distance_from_origin=distance_from_origin+1, current_cell=current_cell, current_facing=face_left, back_allowed=back_allowed, cells=cells)    
            if not  (current_cell, face_right) in cells:
                cells =  self.allowed_movements( remaining_movement=remaining_movement-1, distance_from_origin=distance_from_origin+1,current_cell=current_cell, current_facing=face_right, back_allowed=back_allowed, cells=cells)    
            cell_forward_pos=utils.move_forward(current_cell, current_facing)
            cell_backward_pos=utils.move_backward(current_cell, current_facing)
            if self.is_valid_cell_position(cell_forward_pos) and not (cell_forward_pos,current_facing) in cells:
                cell = self.get_cell(cell_forward_pos)
                cells =  self.allowed_movements( remaining_movement=remaining_movement-cell.movement_needed(),distance_from_origin=distance_from_origin+cell.movement_needed() ,current_cell=cell_forward_pos,current_facing=current_facing,back_allowed=back_allowed,cells=cells)       
            if self.is_valid_cell_position(cell_backward_pos) and not (cell_backward_pos,current_facing) in cells and back_allowed:    
                cell = self.get_cell(cell_backward_pos)
                cells =   self.allowed_movements( remaining_movement=remaining_movement-cell.movement_needed(),distance_from_origin=distance_from_origin+cell.movement_needed(),current_cell=cell_backward_pos,current_facing=current_facing,back_allowed=back_allowed, cells=cells)       
            
        return cells  
    
    def allowed_jump_movements(self, jump_max_movement:int, current_cell:Axial)->Dict:
        results = {}
        for q  in range(-jump_max_movement,jump_max_movement+1):
            for r in range(max(-jump_max_movement,-q-jump_max_movement),min(jump_max_movement,-q+jump_max_movement)+1):
                cell = utils.axial_add(current_cell, Axial(q, r))
                if self.is_valid_cell_position(cell) and not self.get_cell(cell).occupied:
                    for face in Facing:
                        results[(cell, face)]=1
        return results