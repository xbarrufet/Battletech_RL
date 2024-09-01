





import random
import uuid
from gym.BT_beginner_environment import BTBeginnerBoxEnvironment
from simulation.games.BTGame import PLAYER_1, GamePhase
from simulation.games.BT_Beginner_box_game import BTBeginnerBoxGame
from simulation.model import factory
from simulation.model.mech import BattleMech
from simulation.model.mech_utils import Location, MovementType
from simulation.model.weapon import Weapon
from simulation.utils.utils import Axial, Facing

MECH_ID_P1_1="mech_1"
MECH_ID_P2_1="mech_2"

def load_game_1()->BTBeginnerBoxGame:
     sample_cells = ["01","00","00",    "00","02","00",   "00","00","01"]
     game = factory.build_game(sample_cells,width=3, height=3, num_turns=5,
                               mechs_p1=[factory.build_mech(mech_id=MECH_ID_P1_1,mech_type=factory.Griffin_GRF_1N,position=Axial(0,0), facing=Facing.face_N)],
                               mechs_p2=[factory.build_mech(factory.Wolverine_WVR_6N,Axial(2,0), Facing.face_SW,mech_id=MECH_ID_P2_1)])
     return game


sample_cells = ["00","00","00",    "00","00","00",   "00","00","00"]
mech1 = BattleMech(mech_type="Test Mech 1", mech_id=MECH_ID_P1_1, movement=[1,8,5], 
               weapons=[Weapon(weapon_id=uuid.uuid1(),name="Laser", damage=5, range=[3,6,20],volley_number=1,location= Location.loc_Head, initial_ammo=-1)],
               base_armor=[9, 20, 16, 16, 20, 16, 16, 20], deployment_position=Axial(0,0), facing=Facing.face_SE)
mech2 = BattleMech(mech_type="Test Mech 2", mech_id=MECH_ID_P2_1, movement=[5,8,5], 
               weapons=[Weapon(weapon_id="TM3",name="Laser", damage=5, range=[3,6,20],volley_number=1,location= Location.loc_Head, initial_ammo=-1)],
               base_armor=[9, 20, 16, 16, 20, 16, 16, 20], deployment_position=Axial(0,0), facing=Facing.face_SE)
dummy_mech = BattleMech(mech_type="Test Mech 4", mech_id=uuid.uuid1(), movement=[1,1,1], 
               weapons=[Weapon(weapon_id=uuid.uuid1(),name="Missile", damage=5, range=[3,6,20],volley_number=7,location= Location.loc_Head, initial_ammo=10)],
               base_armor=[1, 0, 0, 0, 0, 0, 0, 0], deployment_position=Axial(2,0), facing=Facing.face_SE)
             
 
def bits_to_action_list(bits:list)->list:
     return [idx for idx,v in enumerate(bits) if v==1 ] 
            

def test_encoing_tuple():
     game = load_game_1()
     env = BTBeginnerBoxEnvironment(game)
     assert len(env.enc_int_tuple)==(game.board.width*game.board.height*len(Facing)*len(MovementType))
     assert len(env.enc_tuple_int)==(game.board.width*game.board.height*len(Facing)*len(MovementType))
     for t in range(2):
          assert (Axial(t,t),Facing(t), MovementType(t)) in env.enc_tuple_int

     
def test_initial_reset():
     env = BTBeginnerBoxEnvironment(load_game_1())
     observations = env.reset()
     obs, bits = observations
     assert env.game.current_phase==GamePhase.MOVEMENT_PHASE
     assert env.game.current_player==PLAYER_1
     assert env.game.current_turn==1
     assert len(obs)==env.get_observation_space()
     assert len(bits)==env.get_action_space()
     
def test_run():
     game = load_game_1()
     env = BTBeginnerBoxEnvironment(game)
     observations = env.reset()
     obs, bits = observations
     mech = env.game.get_player_mech(player=PLAYER_1,mech_id=MECH_ID_P1_1)
     action = random.choice(bits_to_action_list(bits))
     action_item = env.enc_int_tuple[action]
     observations, reward, done,_ = env.run(action=action, player=PLAYER_1)
     obs, bits = observations
     assert len(obs)==env.get_observation_space()
     assert len(bits)==env.get_action_space()
     assert reward is not None
     assert not done
     assert mech.position==action_item[0]
     assert mech.facing==action_item[1]
     assert mech.movementType==action_item[2]
     
     
