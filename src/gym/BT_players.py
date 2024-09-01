import random

import torch as T
from rl.pg_agent import PolicyGradientModel


class BTPlayer:
    def __init__(self):
        pass
    
    def choose_action(self,observations:any, allowed_actions:list)->int:
        pass

class BTPlayer_Random(BTPlayer):
    def __init__(self):
        super().__init__()
        
    def choose_action(self, observations: any, allowed_actions: list) -> int:
        bits = [t for t,val in enumerate(allowed_actions) if val==1 ]
        action = random.choice(bits)
        return action
    
 
class BTPlayer_Agent(BTPlayer):
    def __init__(self, model_filename:str,n_obs:int,n_actions:int):
        super().__init__()
        self.model = PolicyGradientModel(n_obs=n_obs,n_actions=n_actions,learning_rate=0)
        
        
    def choose_action(self, observations: any, allowed_actions: list) -> int:
         
        state =T.tensor(observations, dtype=T.float32)
        action_bits =T.tensor(allowed_actions, dtype=T.int64)
        action_values = self.model.forward(state,action_bits)
        action_probs = T.distributions.Categorical(probs=action_values)
        action = action_probs.sample()  
        return action.numpy()
                  