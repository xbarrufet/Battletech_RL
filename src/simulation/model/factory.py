import uuid

from simulation.model.board import Board
from simulation.games.BT_Beginner_box_game import BTBeginnerBoxGame
from simulation.model.mech import  BattleMech
from simulation.model.mech_utils import Location
from simulation.model.weapon import Weapon, WeaponStats
from simulation.utils.utils import Axial, Facing

                            
Wolverine_WVR_6N="Wolverine_WVR-6N"  
Griffin_GRF_1N="Griffin GRF-1N"                        
                            

def build_mech(mech_type:str, position:Axial, facing:Facing=Facing.face_N,mech_id="", ):

     if mech_id=="":
         mech_id=uuid.uuid1()
     if mech_type =="Wolverine WVR-6N":
        return BattleMech(mech_type=mech_type, mech_id=mech_id, movement=[5,8,5], 
                     weapons=[Weapon(weapon_id="m2w1", name="Medium Laser HD", damage=5, range=[3,6,9],volley_number=1,location= Location.loc_Head, initial_ammo=-1),
                              Weapon(weapon_id="m2w2",name="SRM 6", damage=2, range=[3,6,9],  volley_number=6,location= Location.loc_LeftTorso, initial_ammo=20),
                              Weapon(weapon_id="m2w3",name="A/C 5", damage=5, range=[6,12,18],volley_number=1, location=Location.loc_RightArm, initial_ammo=15)],
                     base_armor=[9, 20, 16, 16, 20, 16, 16, 20], deployment_position=position, facing=facing)
                     
     else:
        return BattleMech(mech_type=mech_type, mech_id=mech_id,  movement=[5,8,5],
                    weapons=[Weapon(weapon_id="m1w1",name="LRM 10", damage=1, range=[7,14,21], volley_number=10,location= Location.loc_RightTorso, initial_ammo=12),                     
                             Weapon(weapon_id="m1w2",name="PPC", damage=10, range=[6,12,18],volley_number=1,location= Location.loc_RightArm, initial_ammo=-1)],
                    base_armor=[9, 20, 14, 18, 20, 14, 18, 20], deployment_position=position, facing=facing)

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

sample_cells_small = ["00","00","00","00","00",
                "00","00","00","02","00",
                "00","01","00","01","00",
                "00","02","00","02","00",
                "00","00","00","00","00"]

sample_cells_xsmall = ["00","00","00",
                     "00","00","00",
                     "00","00","00",
                     ]



Board_Sample = Board(width=15, height=17, cells=sample_cells)

Board_Sample_small = Board(width=5, height=5, cells=sample_cells_small)
Board_Sample_xsmall = Board(width=3, height=3, cells=sample_cells_xsmall)

Game_Sample = BTBeginnerBoxGame(board=Board_Sample,
                     max_turns=5,
                     p1_mech= build_mech(mech_type="Griffin GRF-1N",position=Axial(1,15)), 
                     p2_mech = build_mech(mech_type="Wolverine WVR-6N",position=Axial(13,-6),facing=4))

Game_Sample_small = BTBeginnerBoxGame(board=Board_Sample_small,
                     max_turns=5,
                     p1_mech= build_mech(mech_type="Griffin GRF-1N",position=Axial(4,0)), 
                     p2_mech = build_mech(mech_type="Wolverine WVR-6N",position=Axial(0,0),facing=4))

Game_Sample_xsmall = BTBeginnerBoxGame(board=Board_Sample_xsmall,
                     max_turns=5,
                     p1_mech= build_mech("Griffin GRF-1N",position=Axial(2,0)), 
                     p2_mech = build_mech("Wolverine WVR-6N",position=Axial(0,0),facing=4))



def build_game(cells:list[str],width:int, height:0,mechs_p1:tuple[list[str],list[Axial],list[Facing]],mechs_p2:tuple[list[str],list[Axial],list[Facing]], num_turns=5):
    mech_type1 = mechs_p1[0]
    mech_type2 = mechs_p2[0]
    
    return BTBeginnerBoxGame(board=Board(width=width, height=height, cells=cells),
                  max_turns=num_turns,p1_mech= mech_type1,p2_mech = mech_type2)



# def build_game(cells:list[str],width:int, height:0,mechs_p1:tuple[list[str],list[Axial],list[Facing]],mechs_p2:tuple[list[str],list[Axial],list[Facing]],num_turns=5):
#     mech_type1, position1, facing1 = mechs_p1[0]
#     mech_type2, position2, facing2 = mechs_p2[0]
    
#     return BTGame(board=Board(width=width, height=height, cells=cells),
#           num_turns=num_turns,
#           p1_mech= build_mech(mech_type=mech_type1,position=position1,facing=facing1),
#           p2_mech = build_mech(mech_type=mech_type2,position=position2,facing=facing2))

    