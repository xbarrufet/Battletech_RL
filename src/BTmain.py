



import random

import numpy as np
from gym.environment import BTEnvironment
from rl.dqn_action_filter import DQNAgent

from simulation.model.factory import Game_Sample, Game_Sample_small, Game_Sample_xsmall



def select_action(action_space, actions_allowed):
    allowed = [action for action,allowed in zip(action_space,actions_allowed) if allowed==1]
    return random.choice(allowed)

def random_loop():
    game = Game_Sample
    env = BTEnvironment(game,True)
    for _ in range(10):
        positons, terrain, action_bits = env.reset()
        action_space = env.get_action_space()
        end_game = False
        game_turn = 1
        while not end_game:
            action = select_action(action_space=action_space, actions_allowed=action_bits)
            obs, reward, end_game = env.run_action(action)
            action_bits = obs[2]
            print(f"reward:{reward}")
            if game_turn<env.game.game_turn:
                print(f"TURN CHANGE {env.game.game_turn}-------------------")
                game_turn = env.game.game_turn
            

if __name__ == '__main__':
    game = Game_Sample
    env = BTEnvironment(game,False)
    dims_obs = env.get_observation_space_dims()
    agent=DQNAgent(gamma=0.99,epsilon=1.0,lr=0.03,input_dims=dims_obs[0],n_actions=len(env.get_action_space()),batch_size=64,epsilon_decay=5e-6)
    n_games = 10000
    scores, eps_history = [],[]
    for i in range(n_games):
        score = 0
        observation = env.reset()
        action_space = env.get_action_space()
        end_game = False
        game_turn = 1
        while not end_game:
            action,allowed_actions = agent.choose_action(observation)
            observation_, reward, end_game = env.run_action(action)
            score+=reward
            agent.store_transition( state=observation[0],
                                    action=action,actions_allowed=allowed_actions, 
                                    reward=reward,
                                    state_=observation_[0],actions_allowed_=observation_[1],
                                    done=end_game)
            if reward!=0:
                agent.learn()
            observation=observation_
        scores.append(score)
        eps_history.append(agent.epsilon)

        avg_score = np.mean(scores[-100:])
        print(  "\repisode ", i, "score %.2f" % score,
                "avg score %.2f" % avg_score,
                "epislo %.2f" % agent.epsilon, end='')
    agent.save("bt_mov_10K.tbh")
        


