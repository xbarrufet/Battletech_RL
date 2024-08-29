
import math
import time
import uuid
from simulation.model.board import Board, CellType
from simulation.utils.utils import Axial, Facing
import simulation.utils.utils as utils



sample_cells =          ["00","00","00","00","00","00","00","00","00","00","00","00","00","00","00",
                        "00","00","00","00","00","00","00","00","00","00","00","01","02","00","00",
                        "00","00","00","00","00","00","00","00","00","00","01","02","00","00","00",
                        "00","00","00","00","00","00","00","00","00","01","01","00","00","00","00",
                        "00","02","02","01","00","00","00","00","00","01","00","00","00","00","00",
                        "00","00","00","01","00","00","00","00","00","00","00","00","00","00","00",
                        "00","00","00","00","00","00","00","00","00","00","00","00","00","00","00",
                        "00","00","00","00","00","00","00","00","00","00","00","00","00","00","00",
                        "00","00","00","00","00","00","00","00","00","00","00","00","02","00","00",
                        "00","00","00","00","00","00","00","00","00","00","00","00","01","02","00",
                        "00","00","00","00","00","00","00","00","00","00","00","01","01","00","00",
                        "00","00","00","00","00","00","00","00","00","00","00","00","00","00","00",
                        "00","00","00","00","00","00","00","00","00","00","00","00","00","00","00",
                        "00","00","00","00","00","02","00","00","00","00","00","00","00","00","00",
                        "00","00","00","00","01","01","00","00","00","00","00","00","00","00","00",
                        "00","00","00","00","00","01","00","00","00","00","00","00","00","00","00",
                        "00","00","00","00","00","00","00","00","00","00","00","00","00","00","00"]


def test_build_board():
    values = ["00","01","00","01","02","01","00","00","00"]
    width=3
    height = 3
    board = Board(width=width,height=height,cells=values)
    c1 = board.get_cell(Axial(q=1,r=0))
    c2 = board.get_cell(Axial(q=0,r=0))
    c3= board.get_cell(Axial(q=1,r=1))
    assert c1.cell_type ==CellType.cell_LightWood
    assert c2.cell_type ==CellType.cell_Clear
    assert c3.cell_type ==CellType.cell_HeavyWood
    max_q = max([pos.q for pos in board.cells.keys()])
    max_r = max([pos.r for pos in board.cells.keys()])
    min_r = min([pos.r for pos in board.cells.keys()])
    assert max_q == width-1
    assert max_r == height-1
    assert min_r == -math.floor(width/2)
    
def test_factory_board():
   
    Board_Sample = Board(width=15, height=17, cells=sample_cells)
    c1 = Board_Sample.get_cell(Axial(q=0,r=0))
    assert c1.cell_type ==CellType.cell_Clear


def test_cell_distance():
    p1= Axial(0,0)
    p2= Axial(2,0)
    assert utils.position_distance(p1,p2)==2


def test_line():
    a = Axial(0,0)
    b = Axial(0,3)
    line = utils.get_line(a,b)
    assert len(line)==3
    assert Axial(0,1) in line
    assert Axial(0,2) in line
    assert Axial(0,3) in line
    


def test_cell_visibility():
    values_5 = ["00","00","00","00","00",
                "00","00","00","02","00",
                "00","01","00","01","00",
                "00","02","00","02","00",
                "00","00","00","00","00"]
    board = Board(width=5,height=5,cells=values_5)
    p1_1 = Axial(0,0)
    p1_2 = Axial(0,4)
    distance,forest = board.check_visibility(a=p1_1,facing=Facing.face_SE, b=p1_2)
    assert distance==4
    assert forest==0
    p1_1 = Axial(1,1)
    p1_2 = Axial(1,4)
    distance,forest = board.check_visibility(a=p1_1,facing=Facing.face_SE, b=p1_2)
    assert distance==3
    assert forest==3
    p1_1 = Axial(0,3)
    p1_2 = Axial(2,3)
    distance,forest = board.check_visibility(a=p1_1,facing=Facing.face_SE, b=p1_2)
    assert distance==2
    assert forest==2


def test_is_in_arc():
    a=Axial(3,3)
    assert utils.is_in_frontal_act(a,utils.Facing.face_N,Axial(3,1))
    assert not utils.is_in_frontal_act(a,utils.Facing.face_N,Axial(11,19))

    assert utils.is_in_frontal_act(a,utils.Facing.face_NE,Axial(5,0))
    assert not utils.is_in_frontal_act(a,utils.Facing.face_NE,Axial(0,0))

    assert utils.is_in_frontal_act(a,utils.Facing.face_SE,Axial(3,5))
    assert not utils.is_in_frontal_act(a,utils.Facing.face_SE,Axial(0,0))

    assert utils.is_in_frontal_act(a,utils.Facing.face_S,Axial(3,5))
    assert not utils.is_in_frontal_act(a,utils.Facing.face_S,Axial(0,0))

    assert utils.is_in_frontal_act(a,utils.Facing.face_SW,Axial(3,5))
    assert not utils.is_in_frontal_act(a,utils.Facing.face_SW,Axial(0,0))

    assert utils.is_in_frontal_act(a,utils.Facing.face_NW,Axial(0,0))
    assert not utils.is_in_frontal_act(a,utils.Facing.face_NW,Axial(5,3))

def test_get_forest_map():
    values_5 = ["00","00","00","00","00",
                "00","00","00","02","00",
                "00","01","00","01","00",
                "00","02","00","02","00",
                "00","00","00","00","00"]
    try:
        board = Board(width=5,height=5,cells=values_5)
        f1= Axial(1,2)
        f2 = Axial(1,3)
        od_Light = utils.axial_to_oddq(f1)
        od_Heavy = utils.axial_to_oddq(f2)
        forest =board.get_forest_map()
        assert len(forest[0]) == board.width
        assert len(forest) == board.height
        assert forest[od_Light[1]][od_Light[0]] == 1
        assert forest[od_Heavy[1]][od_Heavy[0]] == 2
    except Exception as e:
        print(e)
        assert False
    
  
    

    
    