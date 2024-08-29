import math

#import pygame
from typing import NamedTuple
from enum import Enum



def dice_prob(limit):
    return (7-limit)* 1/6


class Facing(Enum):
    face_N=0
    face_NE=1
    face_SE=2
    face_S=3
    face_SW=4
    face_NW=5

def back_facing(facing:Facing):
    value = (facing.value + 3) % len(Facing)
    return Facing(value)
        

class Axial(NamedTuple):
    q:int
    r:int

class Cube(NamedTuple):
    q:int
    r:int
    s:int


''' hexa grid ***********************************************'''

def axial_add(a:Axial, b:Axial)->Axial:
    return Axial(a.q + b.q, a.r + b.r)


def axial_to_oddq(a:Axial):
    col = a.q
    row = a.r + (a.q - (a.q&1)) / 2
    return int(col), int(row)

def axial_to_cube(a:Axial):
    return Cube(a.q,a.r,-a.q-a.r)


def hex_points(self,x_center,y_center):
    points =[]
    for i in range(6):
        angle_deg = 60 * i
        angle_rad = math.pi / 180 * angle_deg
        points.append((x_center +  self.h_size_side * math.cos(angle_rad),y_center +  self.h_size_side * math.sin(angle_rad)))  
    return points
    
def hex_to_pixel(self,hex:Axial):
    x =  self.center_map_x + self.h_size_side * (3./2 * hex.q)
    y =  self.center_map_y + self.h_size_side * (math.sqrt(3)/2 *hex.q +  math.sqrt(3) * hex.r)        
    return x, y


def generate_coords(map_width:int, map_height:int)->list[tuple]:
    coords = []
    for y in range(map_height):
        r=y
        for q in range(map_width):
            coords.append(Axial(q,r))
            if q % 2 ==1:
                r-=1
    return coords

def get_neighbour_position(a:Axial, facing:Facing)->Axial:
    ''' get the coordinates of the nieghbor cell depending on the facing 0-->N and clockwise '''
    if facing.value ==0:
        return Axial(a.q,a.r-1)
    elif facing.value==1:
        return Axial(a.q+1,a.r-1)
    elif facing.value==2:
        return Axial(a.q+1,a.r)
    elif facing.value==3:
        return Axial(a.q,a.r+1)
    elif facing.value==4:
        return Axial(a.q-1,a.r+1)
    else:
        return Axial(a.q-1,a.r)


''' ********************************************************+ '''


def boxed_hexagon_points(top_left_origin, side_length):
    angle = math.radians(60)
    p1 = [top_left_origin[0] + side_length * math.cos(angle),top_left_origin[1]]
    p2 = [p1[0] + side_length, p1[1] ]
    p3 = [p2[0] + side_length * math.cos(angle),p2[1] + side_length*math.sin(angle)]
    p4 = [p2[0],p3[1] + side_length*math.sin(angle)]
    p5 = [p1[0], p4[1]]
    p6=  [top_left_origin[0],p3[1]]
    points =[p1,p2,p3,p4,p5,p6]
    return points


def hexagon_center(points):
    x =  points[0][0] + int((points[1][0] - points[0][0])/2)
    y =  points[1][1] + int((points[3][1] - points[1][1])/2)
    return x,y


# def rot_center(image, angle):
#     """rotate an image while keeping its center and size"""
#     orig_rect = image.get_rect()
#     rot_image = pygame.transform.rotate(image, angle)
#     rot_rect = orig_rect.copy()
#     rot_rect.center = rot_image.get_rect().center
#     rot_image = rot_image.subsurface(rot_rect).copy()
#     return rot_image

def  cube_round(a:Cube):
    q = round(a.q)
    r = round(a.r)
    s = round(a.s)

    q_diff = abs(q - a.q)
    r_diff = abs(r - a.r)
    s_diff = abs(s - a.s)

    
    if q_diff > r_diff and q_diff > s_diff:
        q = -r-s
    elif r_diff > s_diff:
        r = -q-s
    else:
        s = -q-r
    return Cube(q, r, s)


def position_distance(a:Axial,b:Axial):
    return (abs(a.q - b.q) 
          + abs(a.q + a.r - b.q - b.r)
          + abs(a.r - b.r)) / 2

def cube_subtract(a:Cube, b:Cube):
    return Cube(a.q - b.q, a.r - b.r, a.s - b.s)


def cube_distance(a:Cube,b:Cube):
    vec = cube_subtract(a, b)
    return (abs(vec.q) + abs(vec.r) + abs(vec.s)) / 2
    


def lerp(a,b,t):
    return a + (b - a) * t

def cube_lerp(a:Cube,b:Cube,t:int):
   return Cube(lerp(a.q, b.q, t),
                lerp(a.r, b.r, t),
                lerp(a.s, b.s, t))


def get_line(a:Axial, b:Axial)->list[(tuple)]:
    ac,bc = axial_to_cube(a), axial_to_cube(b)
    ''' return the cells between a and b'''
    distance = int(position_distance(ac,bc))
    res = []
    for i in range(1,distance+1):
       res.append(cube_round(cube_lerp(ac, bc, 1.0/distance* i)))
    return [Axial(a.q,a.r) for a in res]


def is_in_frontal_act(a:Axial, facing_a:Facing, b:Axial)->bool:
    ac,bc = axial_to_cube(a), axial_to_cube(b)
    match facing_a:
        case Facing.face_N:
            return bc.r<=ac.r and bc.s>=ac.s
        case Facing.face_NE:
            return bc.q>=ac.q and bc.r<=ac.r
        case Facing.face_SE:
            return bc.q>=ac.q and bc.s<=ac.s
        case Facing.face_S:
            return bc.r>=ac.r and bc.s<=ac.s
        case Facing.face_SW:
            return bc.q<=ac.q and bc.r>=ac.r
        case Facing.face_NW:
            return bc.q<=ac.q and bc.s>=ac.s
    return False

def move_forward(a:Axial, facing:Facing):
        match facing:
            case Facing.face_N:
                return Axial(a.q,a.r-1)
            case Facing.face_NE:
                return Axial(a.q+1,a.r-1)
            case Facing.face_SE:
                return Axial(a.q+1,a.r)
            case Facing.face_S:
                return Axial(a.q,a.r+1)
            case Facing.face_SW:
                return Axial(a.q-1,a.r-1)
            case Facing.face_NW:
                return Axial(a.q-1,a.r)

def move_backward(a:Axial, facing:Facing):
        facing = Facing((facing.value + 3) % 6)
        return move_forward(a, facing=facing)
            