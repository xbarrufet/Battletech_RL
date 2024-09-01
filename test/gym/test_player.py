from gym.BT_beginner_environment import BTBeginnerBoxEnvironment
from gym.BT_players import BTPlayer, BTPlayer_Random,BTPlayer_Agent
from simulation.games.BT_Beginner_box_game import BTBeginnerBoxGame
from simulation.model import factory
from simulation.utils.utils import Axial, Facing

MECH_ID_P1_1="mech_1"
MECH_ID_P2_1="mech_2"

def load_game_1()->BTBeginnerBoxGame:
     sample_cells = ["01","00","00",    "00","02","00",   "00","00","01"]
     game = factory.build_game(sample_cells,width=3, height=3, num_turns=5,
                               mechs_p1=[factory.build_mech(mech_id=MECH_ID_P1_1,mech_type=factory.Griffin_GRF_1N,position=Axial(0,0), facing=Facing.face_N)],
                               mechs_p2=[factory.build_mech(factory.Wolverine_WVR_6N,Axial(2,0), Facing.face_SW,mech_id=MECH_ID_P2_1)])
     return game

def test_random_player_choose_action():

    try:
        player = BTPlayer_Random()
        game = load_game_1()
        env = BTBeginnerBoxEnvironment(game)
        obsevations = env.reset()
        obs,bits = obsevations
        action = player.choose_action(obs,bits)
        assert bits[action]==1
    except Exception as e:
        assert False, e
    
def test_agent_player_choose_action():
    try:
        
        game = load_game_1()
        env = BTBeginnerBoxEnvironment(game)
        player = BTPlayer_Agent(model_filename="BeginnerBox_PolicyGradient_1.pgm",n_obs=env.get_observation_space(),n_actions=env.get_action_space())
        obsevations = env.reset()
        obs,bits = obsevations
        action = player.choose_action(obs,bits)
        assert bits[action]==1
    except Exception as e:
        assert False, e
    