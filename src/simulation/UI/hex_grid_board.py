

import math
from pygame import Surface
import pygame

from simulation.model.board import Board, Cell, CellType
from simulation.model.mech import BattleMech


# Definir constantes
TOTAL_WIDTH,TOTAL_HEIGHT = 1200,800
WIDTH, HEIGHT = 600, 800
BACKGROUND_COLOR = (255, 255, 255)
TEXT_COLOR =  (255, 255, 255)
LINE_COLOR = (0, 0, 0) 
LINE_WIDTH=1
UNIT_HEX_REDUCING_FACTOR = 0.2
TERRAIN_COLOR_CLEAR = (191,140,99)
TERRAIN_COLOR_LIGHT_WOOD = (145,166,94)
TERRAIN_COLOR_HEAVY_WOOD = (46,75,43)

def get_cell_color(cell_type:CellType):
    if cell_type==CellType.cell_Clear:
        return TERRAIN_COLOR_CLEAR
    elif cell_type==CellType.cell_LightWood:
        return TERRAIN_COLOR_LIGHT_WOOD
    else:
        return TERRAIN_COLOR_HEAVY_WOOD

m1 = pygame.image.load('data/imgs/Griffin_4R.png')
m2 = pygame.image.load('data/imgs/Wolverine_6D.png')
mech_imgs_dict = {"Wolverine WVR-6N":m2, "Griffin GRF-1N":m1}

def rot_center(image, angle):
    """rotate an image while keeping its center and size"""
    orig_rect = image.get_rect()
    rot_image = pygame.transform.rotate(image, angle)
    rot_rect = orig_rect.copy()
    rot_rect.center = rot_image.get_rect().center
    rot_image = rot_image.subsurface(rot_rect).copy()
    return rot_image

def scale_image(mech_img ,factor):
    ''' return the image escaled by factor and get the delta_x, delta_y from the original center'''
    scaled_img = pygame.transform.scale_by(mech_img,factor)
    delta_x = int(scaled_img.get_width()/2)
    delta_y= int(scaled_img.get_height()/2)
    return scaled_img, delta_x, delta_y

class HexGrid:
    def __init__(self, origin_x:int, origin_y:int,map_width:int, map_height:int, map_screen_width:int, map_screen_height:int ):
        self.origin_x = origin_x
        self.origin_y = origin_y
        self.map_screen_width = map_screen_width
        self.map_screen_height = map_screen_height
        self.map_width = map_width
        self.map_height = map_height
        # geometry  
        if map_width>map_height:
            self.hex_side =  (map_screen_width)/(map_width*1.5+0.5)
            self.hex_height =( math.sqrt(3)*self.hex_sid)        
        else:
            self.hex_height = map_screen_height/(map_height + 1)
            self.hex_side = (self.hex_height/ math.sqrt(3))
        
    def hex_points(self,x_center,y_center):
            points =[]
            for i in range(6):
                angle_deg = 60 * i
                angle_rad = math.pi / 180 * angle_deg
                points.append((x_center +  self.hex_side * math.cos(angle_rad),y_center +  self.hex_side * math.sin(angle_rad)))  
            return points
    
    def hex_to_pixel(self,position):
        x =  self.origin_x + self.hex_side + self.hex_side * (3./2 * position.q)
        y =  self.origin_y + self.hex_height/2 + position.q * self.hex_height/2 + self.hex_height*position.r
        return x, y

    def draw_unit(self, screen:Surface, mech:BattleMech):
        cx,cy = self.hex_to_pixel(mech.position)
        mech_img,delta_x,delta_y = scale_image(mech_imgs_dict[mech.mech_type],0.8)
        cx,cy = cx-delta_x ,cy-delta_y
        mech_img= rot_center(mech_img,-60*mech.facing.value )
        screen.blit(mech_img,(cx,cy))
    
    def draw_cell(self, screen:Surface,cell:Cell):
        x,y = self.hex_to_pixel(cell.position)
        points = self.hex_points(x,y)
        pygame.draw.polygon(surface=screen, color=get_cell_color(cell.cell_type),points=points)
        pygame.draw.polygon(surface=screen, color=LINE_COLOR,points=points,width=1)


    
    def draw_board(self, screen:Surface, board:Board):
        screen.fill(BACKGROUND_COLOR)
        for cell in board.cells.values():
            self.draw_cell(screen=screen,cell=cell) 
            



