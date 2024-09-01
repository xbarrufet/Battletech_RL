import numpy as np
from gym.BT_environment import BTEnvironment
from gym.BT_players import BTPlayer, BTPlayer_Random
from rl.pg_agent import PolicyGradientAgent
from simulation.games.BTGame import PLAYER_1, PLAYER_2



class PGAgentTrainer:
    def __init__(self,environment:BTEnvironment,learning_rate = 0.01, gamma=0.9, initial_modeL_filename:str="",result_model_filename:str="",player_2:BTPlayer=BTPlayer_Random ) -> None:
        self.env = environment
        observation_space = self.env.get_observation_space()
        action_space = self.env.get_action_space()
        self.player_2 = player_2
        self.agent = PolicyGradientAgent(input_size=observation_space,num_actions=action_space,learning_rate=learning_rate,gamma=gamma,model_filename= initial_modeL_filename)
        self.result_model_filename=result_model_filename

    def train(self,n_steps=1000):
        scores, eps_history = [],[]
        for i in range(n_steps):
            score = 0
            observation = self.env.reset()
            end_game=False
            steps =0
            while not end_game:
                action = self.agent.choose_action(observation)
                observation_, reward, end_game,info =self.env.run(action=action, player=PLAYER_1)
                obs,allowed_actions = observation
                # action_2 = self.player_2.choose_action(observations=obs, allowed_actions=allowed_actions)
                # observation_, reward, end_game,info = self.env.run(action=action, player=PLAYER_2)
                score+=reward
                self.agent.store_reward(reward=reward)
                observation=observation_
                steps +=1
                #print(  "\rscore %.2f" % score,"Steps ", steps ,end='')
            self.agent.learn()
            scores.append(score)
            avg_score = np.mean(scores[-100:])
            print(  "\repisodes ", i, "score %.2f" % score,
                    "Steps ", steps ,
                    "avg score %.2f" % avg_score,end='')
        
        if self.result_model_filename!="":
            self.agent.save(self.result_model_filename)
        
        
