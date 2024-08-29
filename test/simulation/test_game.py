

import uuid

from simulation.games.BT_Beginner_box_game import BTBeginnerBoxGame,GamePhase
from simulation.model.board import Board
import simulation.model.factory as factory
from simulation.model.mech import Action,  Movement,MechState
from simulation.utils.utils import Axial, Facing


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

def load_game():

     game = factory.build_game(sample_cells,width=15, height=17, num_turns=5,
                               mechs_p1=[factory.build_mech(factory.Griffin_GRF_1N,Axial(1,15), Facing.face_N)],
                               mechs_p2=[factory.build_mech(factory.Wolverine_WVR_6N,Axial(13,-6), Facing.face_N)])
     
     return game

def load_game_2():
     
     game = factory.build_game(sample_cells,width=15, height=17, num_turns=5,
                               mechs_p1=[factory.build_mech(factory.Griffin_GRF_1N,Axial(0,0), Facing.face_SE)],
                               mechs_p2=[factory.build_mech(factory.Wolverine_WVR_6N,Axial(1,0), Facing.face_NW)])
     return game

def load_game_3()->BTBeginnerBoxGame:
     sample_cells = ["01","00","00",    "00","02","00",   "00","00","01"]
     game = factory.build_game(sample_cells,width=3, height=3, num_turns=5,
                               mechs_p1=[factory.build_mech(factory.Griffin_GRF_1N,Axial(0,0), Facing.face_N)],
                               mechs_p2=[factory.build_mech(factory.Wolverine_WVR_6N,Axial(2,0), Facing.face_SW)])
     return game


