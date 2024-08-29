import pygame
from simulation.UI.hex_grid_board import HexGrid
from simulation.model.board import Board, CellType, Axial



def Position3(pos:Axial):
     return pos.q,pos.r, -pos.q-pos.r


def max_range_arc( center=Axial, dist:int=0 ,facing:int=0): 
     
    res = []
    match facing:
        case 0:
            res =  [Axial(center.q - i,center.r-dist+i) for i in range(0,dist+1)] + [Axial(center.q + i,center.r-dist) for i in range(0, dist+1)]
        case 1:
            res = [Axial(center.q + i,center.r - dist) for i  in range(0,dist+1)] + [Axial(center.q+dist,center.r -i) for i  in range(0,dist+1)]  
        case 2:
            res = [Axial(center.q + dist,center.r - i ) for i  in range(0,dist+1)] +  [Axial(center.q + dist-i,center.r +i) for i  in range(0,dist+1)]   
        case 3:
            res = [Axial(center.q + i,center.r+dist-i) for i in range(0,dist+1)] + [Axial(center.q - i,center.r+dist) for i in range(0, dist+1)]
        case 4:
            res =  [Axial(center.q - i,center.r + dist) for i  in range(0,dist+1)] + [Axial(center.q-dist,center.r +i) for i  in range(0,dist+1)]
        case 5:
            res =   [Axial(center.q - dist,center.r + i ) for i  in range(0,dist+1)] +  [Axial(center.q - dist+i,center.r -i) for i  in range(0,dist+1)]   
    return [center] + res


def paint_arcs( center=Axial, dist:int=0 ,facing:int=0):
     zero_coords = []
     for t in range(1, dist+1): 
         zero_coords.extend([Axial(0, -t),Axial(t,-t)])
         zero_coords.extend([Axial(i,-t) for i in range(1,t)])
     res = [center]    
     res.extend([Axial(c.q + center.q, c.r + center.r) for c in zero_coords])
     return res


# def paint_arcs(board:Board, dist:int=0 ,facing:int=0):
#      cell = board.get_cell(position=Position(7,5))
#      cell.cell_type=CellType.cell_LightWood
#      cells = [ ]
#      pillar = cell.position
#      for t in range(1, dist+1): 
#          pt = Position(pillar.q, pillar.r-t)
#          pm = Position(pillar.q+t,pillar.r-t)
#          p_arc  = [pt,pm].extend([Position(pillar.q+i,pillar.r-t) for i in range(1,t)])
#          return p_arc
    

         
          
 

sample_cells =          ["00","00","00","00","00","00","00","00","00","00","00","00","00","00","00",
                        "00","00","00","00","00","00","00","00","00","00","00","00","00","00","00",
                        "00","00","00","00","00","00","00","00","00","00","00","00","00","00","00",
                        "00","00","00","00","00","00","00","00","00","00","00","00","00","00","00",
                        "00","00","00","00","00","00","00","00","00","00","00","00","00","00","00",
                        "00","00","00","00","00","00","00","00","00","00","00","00","00","00","00",
                        "00","00","00","00","00","00","00","00","00","00","00","00","00","00","00",
                        "00","00","00","00","00","00","00","00","00","00","00","00","00","00","00",
                        "00","00","00","00","00","00","00","00","00","00","00","00","00","00","00",
                        "00","00","00","00","00","00","00","00","00","00","00","00","00","00","00",
                        "00","00","00","00","00","00","00","00","00","00","00","00","00","00","00",
                        "00","00","00","00","00","00","00","00","00","00","00","00","00","00","00",
                        "00","00","00","00","00","00","00","00","00","00","00","00","00","00","00",
                        "00","00","00","00","00","00","00","00","00","00","00","00","00","00","00",
                        "00","00","00","00","00","00","00","00","00","00","00","00","00","00","00",
                        "00","00","00","00","00","00","00","00","00","00","00","00","00","00","00",
                        "00","00","00","00","00","00","00","00","00","00","00","00","00","00","00"]
Board_Sample = Board(width=15, height=17, cells=sample_cells)
WIDTH, HEIGHT = 600, 800
TOTAL_WIDTH,TOTAL_HEIGHT = 1200,800
cells = max_range_arc(center=Axial(7,5), dist=3, facing = 2)
for x in cells:
     if Board_Sample.is_valid_cell_position(x):
          Board_Sample.get_cell(x).cell_type=CellType.cell_HeavyWood



uiboard = HexGrid(origin_x=0,origin_y=0,map_width=Board_Sample.width, map_height=Board_Sample.height,map_screen_width=WIDTH,map_screen_height=HEIGHT)
pygame.init()
screen = pygame.display.set_mode(( TOTAL_WIDTH, TOTAL_HEIGHT))
clock = pygame.time.Clock()
running = True
while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT or event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                running = False
        uiboard.draw_board(screen=screen,board=Board_Sample)
        pygame.display.flip()
        clock.tick(60)
pygame.quit()

