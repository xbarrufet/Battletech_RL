
from simulation.games.BT_Beginner_box_game import BTBeginnerBoxGame
from simulation.model import factory
from simulation.utils.utils import Axial, Facing


MECH_ID_P1_1="mech_1"
MECH_ID_P2_1="mech_2"

def load_game_small()->BTBeginnerBoxGame:
     sample_cells = ["01","00","00",    "00","02","00",   "00","00","01"]
     game = factory.build_game(sample_cells,width=3, height=3, num_turns=5,
                               mechs_p1=[factory.build_mech(mech_type=factory.Griffin_GRF_1N,position=Axial(0,0), facing=Facing.face_N,mech_id=MECH_ID_P1_1,player=0)],
                               mechs_p2=[factory.build_mech(mech_type=factory.Wolverine_WVR_6N,position=Axial(2,0), facing=Facing.face_SW,mech_id=MECH_ID_P2_1,player=1)])
     return game



def load_game_sample():
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
     game = factory.build_game(sample_cells,width=15, height=17, num_turns=5,
                               mechs_p1=[factory.build_mech(mech_type=factory.Griffin_GRF_1N,position=Axial(1,15), facing=Facing.face_N,mech_id=MECH_ID_P1_1,player=0)],
                               mechs_p2=[factory.build_mech(mech_type=factory.Wolverine_WVR_6N,position=Axial(13,-6), facing=Facing.face_SW,mech_id=MECH_ID_P2_1,player=1)])
     return game
 