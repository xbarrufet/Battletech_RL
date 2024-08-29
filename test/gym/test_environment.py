

import math
import uuid
from gym.environment import BTEnvironment
from simulation.games.BT_Beginner_box_game import BTGame
from simulation.model.mech import Action, BattleMech
import simulation.model.factory as factory
from simulation.model.mech_utils import Location
from simulation.model.weapon import Weapon
from simulation.utils.utils import Axial, Facing





def load_game()->BTGame:
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
     
     try:
          game = load_game()
          env = BTEnvironment(game)
          actions_allowed = [Action.ACT_SELECT_WALK_MOVEMENT_TYPE,Action.ACT_SELECT_NO_MOVEMENT,Action.ACT_MOVE_FORWARD]
          bits = env.get_allowed_actions_bits(allowed_actions=actions_allowed)
          assert bits[0]==1 and bits[1]==1 and bits[3]==1 and sum(bits)==3
     except Exception as e:
         print(e)
         assert False
  

def test_terrain_map():
     try:
          game = load_game()
          env = BTEnvironment(game)
          terrain = env.build_terrain_map()
          assert terrain[0][0]==1 and terrain[1][1]==2 and terrain[2][2]==1 and terrain[1][0]==0
     except Exception as e:
         print(e)
         assert False
     

def test_run_action_get_observations():
     game = factory.build_game(sample_cells,width=3, height=3, num_turns=5,
                               mechs_p1=[mech1],
                               mechs_p2=[mech2])
     env = BTEnvironment(game)
     obs,bit = env.reset()
     assert len(obs)==17 and len(bit)==len(env.get_action_space())
     assert obs[0]==env.game.gameStatus.current_phase.value
     assert obs[10]==env.game.p2_mech.position.r


def test_automatic_movement_and_game_is_over():
     try:
          game = factory.build_game(sample_cells,width=3, height=3, num_turns=5,
                                   mechs_p1=[mech1],
                                   mechs_p2=[dummy_mech])
          env = BTEnvironment(game)
          obs,bit = env.reset()
          obs,rewards,done,map = env.run_action(Action.ACT_SELECT_WALK_MOVEMENT_TYPE)
          obs,rewards,done,map = env.run_action(Action.ACT_NO_MOVEMENT)
          obs,rewards,done,map = env.run_action(Action.ACT_FIRE_WEAPONS,dummy_mech)
          assert done
     except Exception as e:
         print(e)
         assert False


def test_run_automatic_actions():
     pass

