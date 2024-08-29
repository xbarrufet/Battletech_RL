





import uuid
from simulation.games.BT_Beginner_box_game import BTBeginnerBoxGame,BTBeginnerBoxGameEnvironment
from simulation.model import factory
from simulation.model.mech import BattleMech
from simulation.model.mech_utils import Location
from simulation.model.weapon import Weapon
from simulation.utils.utils import Axial, Facing


def load_game()->BTBeginnerBoxGame:
     sample_cells = ["01","00","00",    "00","02","00",   "00","00","01"]
     game = factory.build_game(sample_cells,width=3, height=3, num_turns=5,
                               mechs_p1=[factory.build_mech(factory.Griffin_GRF_1N,Axial(0,0), Facing.face_N)],
                               mechs_p2=[factory.build_mech(factory.Wolverine_WVR_6N,Axial(2,0), Facing.face_SW)])
     return game


sample_cells = ["00","00","00",    "00","00","00",   "00","00","00"]
mech1 = BattleMech(mech_type="Test Mech", mech_id=uuid.uuid1(), movement=[1,8,5], 
               weapons=[Weapon(name="Laser", damage=5, range=[3,6,20],volley_number=1,location= Location.loc_Head, initial_ammo=-1)],
               base_armor=[9, 20, 16, 16, 20, 16, 16, 20], deployment_position=Axial(0,0), facing=Facing.face_SE)
mech2 = BattleMech(mech_type="Test Mech", mech_id=uuid.uuid1(), movement=[5,8,5], 
               weapons=[Weapon(name="Laser", damage=5, range=[3,6,20],volley_number=1,location= Location.loc_Head, initial_ammo=-1)],
               base_armor=[9, 20, 16, 16, 20, 16, 16, 20], deployment_position=Axial(0,0), facing=Facing.face_SE)
dummy_mech = BattleMech(mech_type="Test Mech 2", mech_id=uuid.uuid1(), movement=[1,1,1], 
               weapons=[Weapon(name="Missile", damage=5, range=[3,6,20],volley_number=7,location= Location.loc_Head, initial_ammo=10)],
               base_armor=[1, 0, 0, 0, 0, 0, 0, 0], deployment_position=Axial(2,0), facing=Facing.face_SE)
      



# #     ACT_SELECT_WALK_MOVEMENT_TYPE = 0
# #     ACT_SELECT_RUN_MOVEMENT_TYPE = 1
# #     ACT_MOVE_FORWARD = 2
# #     ACT_MOVE_BACKWARD = 3
# #     ACT_ROTATE_LEFT = 4
# #     ACT_ROTATE_RIGHT = 5
# #     ACT_END_MOVEMENT = 6





def test_allowed_action_bits():
 pass    
 

def test_terrain_map():
     pass

def test_run_action_get_observations():
   pass

def test_automatic_movement_and_game_is_over():
    pass


def test_run_automatic_actions():
     pass

