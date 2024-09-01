


import os
from gym.BT_beginner_environment import BTBeginnerBoxEnvironment
from rl.pg_agent import PolicyGradientAgent
from simulation.games.BTGame import PLAYER_1
from simulation.games.BT_Beginner_box_game import BTBeginnerBoxGame
from simulation.model import factory
from simulation.utils.utils import Axial, Facing
import test.factory_test as factory_test


 
def test_store_reward_agent():
    try:
        game = factory_test.load_game_small()
        env = BTBeginnerBoxEnvironment(game = game)
        agent = PolicyGradientAgent(env.get_observation_space(),env.get_action_space())
        observations = env.reset()
        obs,bits = observations
        action = agent.choose_action(observations)
        assert bits[action]==1
        observations, reward, done,_ = env.run(action=action, player=PLAYER_1)
        agent.store_reward(reward=reward)
        assert len(agent.rewards)==1
        assert agent.rewards[0]==reward
    except Exception as e:
        assert False, e
   

def test_choose_action():
    try:
        game = factory_test.load_game_small()
        env = BTBeginnerBoxEnvironment(game = game)
        agent = PolicyGradientAgent(env.get_observation_space(),env.get_action_space())
        observations = env.reset()
        obs,bits = observations
        action = agent.choose_action(observations)
        assert bits[action]==1
    except Exception as e:
        assert False, e
   
   
def tet_load_and_save():
    try:
        
        game = factory_test.load_game_small()
        env = BTBeginnerBoxEnvironment(game = game)
        agent = PolicyGradientAgent(env.get_observation_space(),env.get_action_space(),model_filename="BeginnerBox_PolicyGradient_1.pgm")
        agent.save("BeginnerBox_PolicyGradient_1_test.pgm")
        assert os.path.isfile("BeginnerBox_PolicyGradient_1_test,pgm")
        agent = PolicyGradientAgent(env.get_observation_space(),env.get_action_space(),model_filename="BeginnerBox_PolicyGradient_1_test.pgm")
        observations = env.reset()
        obs,bits = observations
        action = agent.choose_action(observations)
        assert bits[action]==1
    except Exception as e:
        assert False, e    

