from collections import deque
import numpy as np
import torch as T
import torch.nn as nn
import torch.nn.functional as F
from torch.autograd import Variable
import torch.optim as optim

from simulation.games.BT_Beginner_box_game import PLAYER_1, PLAYER_2, BTBeginnerBoxGame
from simulation.model.factory import Game_Sample


T.autograd.set_detect_anomaly(True)

class PolicyGradientModel(nn.Module):
    def __init__(self, n_obs, n_actions, fc1_dims=1024, fc2_dims=1024,learning_rate=0.01):
        super(PolicyGradientModel, self).__init__()
        self.fc1_dims = fc1_dims
        self.fc2_dims = fc2_dims
        self.n_actions = n_actions

        self.fc1 = nn.Linear(in_features=n_obs, out_features=512)
        self.fc2 = nn.Linear(in_features=512, out_features=1024)
        self.fc3 = nn.Linear(in_features=1024, out_features=n_actions)
        
        self.optimizer = optim.Adam(self.parameters(), lr=learning_rate)
        
    def forward(self, state, valid_actions):
        value = F.relu(self.fc1(state))
        value = F.relu(self.fc2(value))
        value =  F.relu(self.fc3(value))
        action_values = T.where(valid_actions == 1, value, -T.inf)
        action_probs = F.softmax(action_values)
        return action_probs
    
    def save(self, filename):
        T.save(self.state_dict(), filename)

    def load(self, filename):
        self.load_state_dict(T.load(filename))

class PolicyGradientAgent():
    def __init__(self,  input_size, num_actions,learning_rate=0.01, gamma=0.9, model_filename=""):
        self.gamma = gamma
        self.learning_rate = learning_rate
        self.saved_log_probs = []
        self.rewards = []
        self.num_actions = num_actions
        self.model = PolicyGradientModel(n_obs=input_size,n_actions=num_actions,learning_rate=learning_rate)
        if model_filename!="":
            self.model.load(model_filename)
        self.eps  = np.finfo(np.float32).eps.item()
        
    def store_reward(self, reward):
        self.rewards.append(reward)

        
    def choose_action(self, obs_and_bits):
        observation, action_bits = obs_and_bits
        
        state =T.tensor(observation, dtype=T.float32)
        action_bits =T.tensor(action_bits, dtype=T.int64)
        action_values = self.model.forward(state,action_bits)
        action_probs = T.distributions.Categorical(probs=action_values)
        action = action_probs.sample()  
        self.saved_log_probs.append(action_probs.log_prob(action))
        return action.numpy()
        
    def learn(self):
        R = 0
        policy_loss = []
        returns = deque()
        for r in self.rewards[::-1]:
            R = r + self.gamma * R
            returns.appendleft(R)
        returns = T.tensor(returns)
        returns = (returns - returns.mean()) / (returns.std() + self.eps)
        for log_prob, R in zip(self.saved_log_probs, returns):
            policy_loss.append(-log_prob * R)
        self.model.optimizer.zero_grad()
        policy_loss = T.stack(policy_loss).sum()
        policy_loss.backward()
        self.model.optimizer.step()
        del self.rewards[:]
        del self.saved_log_probs[:]
        
    
        
    def save(self, f_name):
        
        self.model.save(filename=f_name)
    
    def load(self, f_name):
         self.model.laod(filename=f_name)


# def train(load:bool=False, learning_rate=0.0001,gamma=0.9,n_steps = 1000,random_player2=True,load_filename="",save_filename=""):
#     game = Game_Sample
#     env = BTBeginnerBoxGameEnvironment(game=game,random_player2=random_player2)
#     dims_obs = env.obs_dim
#     agent=PolicyGradientAgent(learning_rate= learning_rate, gamma=gamma,input_size=dims_obs,num_actions=env.get_action_space(),model_filename=load_filename)
#     agent_player2=PolicyGradientAgent(learning_rate= learning_rate, gamma=gamma,input_size=dims_obs,num_actions=env.get_action_space(),model_filename=load_filename)
    
#     n_games = n_steps
#     scores, eps_history = [],[]
#     for i in range(n_games):
#         score = 0
#         observation = env.reset()
#         end_game=False
#         steps =0
#         while not end_game:
#             action = agent.choose_action(observation)
#             observation_, reward, end_game,info = env.run(action=action, player=PLAYER_1)
#             if not random_player2:
#                 action = agent_player2.choose_action(observation_)
#                 observation_, reward, end_game,info = env.run(action=action, player=PLAYER_2)
#             score+=reward
#             agent.store_reward(reward=reward)
#             observation=observation_
#             steps +=1
#             #print("\rSteps ", steps, "Action:", Action(action).name, " acum reward:", info[0],"-",info[1], end_game,end='')    
#         agent.learn()
#         scores.append(score)
#         avg_score = np.mean(scores[-100:])
#         print(  "\repisodes ", i, "score %.2f" % score,
#                    "Steps ", steps ,
#                    "avg score %.2f" % avg_score,end='')
    
#     if save_filename!="":
#         agent.save(save_filename)
#     return avg_score
      
# filename ="BeginnerBox_PolicyGradient.pgm"
# if __name__ == '__main__':
#     train(learning_rate=0.0001,gamma=0.9,n_steps=1000, save_filename=filename,load_filename="")
#     #train(learning_rate=0.0001,gamma=0.9,n_steps=1000, save_filename=filename,load_filename="BeginnerBox_PolicyGradient_1.pgm",random_player2=False)
