import math
from gym.BT_environment import BTEnvironment
from simulation.games.BTGame import PLAYER_1, GamePhase, MoveAction
from simulation.games.BT_Beginner_box_game import BTBeginnerBoxGame
from simulation.model import mech_utils
from simulation.model.mech import BattleMech
from simulation.model.mech_utils import MovementType
from simulation.utils import utils
from simulation.utils.utils import Facing


class BTBeginnerBoxEnvironment(BTEnvironment):
    
    def __init__(self, game:BTBeginnerBoxGame) -> None:
        super().__init__(game=game)
        self.acum_rewards = [0,0]
        self.game = game
        self.obs_dim = 9
        self.action_dim =game.board.height*game.board.width*len(Facing)*len(MovementType)
        self.enc_tuple_int = {}
        self.enc_int_tuple = [0] * self.action_dim
        self._encoding_tuple()
                        
    def _encoding_tuple(self):
        counter= 0
        for pos in self.game.board.cells.keys():
            for f in range(6):
                facing = Facing(f)
                for mv in range(3):
                    self.enc_tuple_int[(pos,facing,MovementType(mv))]=counter
                    self.enc_int_tuple[counter]=(pos,facing,MovementType(mv))
                    counter+=1
        
        
    def reset(self):
        super().reset()
        self.acum_rewards = [0,0]
        self.game.next_turn()
        first_player = self.game.run_initative_action(forced_player=PLAYER_1)
        gameStatus =self.game.get_game_status()
        mech1 = list(gameStatus.mechs[first_player].values())[0]
        mech2 =  list(gameStatus.mechs[self.game.get_next_player(first_player)].values())[0]
        d1, v1 = self.game.board.check_visibility(mech1.position,mech1.facing,mech2.position)
        d2, v2 = self.game.board.check_visibility(mech2.position,mech2.facing,mech1.position)
        return (self.build_observations(mech_player=mech1,mech_target=mech2,d1=d1,d2=d2,v1=v1,v2=v2), self.get_allowed_actions_bits(player=first_player))
  
    
    def run_action_return(self, player=PLAYER_1):
        gameStatus =self.game.get_game_status()
        mech_player = list(gameStatus.mechs[player].values())[0]
        mech_target =  list(gameStatus.mechs[self.game.get_next_player(player)].values())[0]
        d1, v1 = self.game.board.check_visibility(mech_player.position,mech_player.facing,mech_target.position)
        d2, v2 = self.game.board.check_visibility(mech_target.position,mech_target.facing,mech_player.position)
        return  (self.build_observations(mech_player=mech_player,mech_target=mech_target,d1=d1,d2=d2,v1=v1,v2=v2), self.get_allowed_actions_bits(player=player)),\
                self.build_reward(mech_player=mech_player,mech_target=mech_target,d1=d1,d2=d2,v1=v1,v2=v2, current_turn=gameStatus.current_turn,player=player), \
                self.build_is_done(), \
                self.build_info()
    
    
    def build_observations(self,mech_player:BattleMech, mech_target:BattleMech, d1:int,v1:int,d2:int,v2:int):
        
        obs = []
        obs.append(mech_player.facing.value)
        obs.append(mech_target.facing.value)
        obs.append(mech_player.position.q)
        obs.append(mech_player.position.r)
        
        obs.append(mech_player.movementType.value if mech_player.movementType is not None else -1)
        obs.append(mech_target.movementType.value  if mech_target.movementType is not None else -1)
        obs.append(d1)
        obs.append(1 if utils.is_in_frontal_act(mech_player.position,mech_player.facing,mech_target.position) else 0)
        obs.append(1 if utils.is_in_frontal_act(mech_target.position,mech_target.facing,mech_player.position) else 0)
        
        return obs
        
    def build_reward(self,mech_player:BattleMech, mech_target:BattleMech, d1:int,v1:int,d2:int,v2:int,player:int,current_turn:int):
        
        g1 = mech_player.gunner_skill
        g2 = mech_target.gunner_skill
        # r1 = table_range_modfier(d1)
        # r2 = table_range_modfier(d2)
        a1 = mech_utils.table_attacker_movement(mech_player.movementType)
        a2 = mech_utils.table_attacker_movement(mech_target.movementType)
        o1 = mech_utils.table_other_modifiers(v1)
        o2 = mech_utils.table_other_modifiers(v2)
        rew1 = 0.1*((mech_utils.dice_2D6_prob(g1 + a1 + o1 )-math.log(current_turn))- (mech_utils.dice_2D6_prob(g2 + a2 + o2)- math.log(current_turn)))
        rew2 = (mech_utils.dice_2D6_prob(g2 + a2 + o2) -  mech_utils.dice_2D6_prob(g1 + a1 + o1))
        self.acum_rewards[player]+=rew1
        self.acum_rewards[(player+1)%2]+=rew2
        return rew1
        
    
    def build_is_done(self):
        base = 2
        return self.acum_rewards[0]>base or self.acum_rewards[0]<-base 
    
    def build_info(self):
        info = [0]*2
        info[0] = self.acum_rewards[0]
        info[1] = self.acum_rewards[1]
        return info
    
    def run(self,action:int, player:int) -> tuple:
        if player==self.game.current_player:
            if self.game.current_phase==GamePhase.MOVEMENT_PHASE:
                return self.run_movement_action(action, player)
        else:
            raise f"Not valid player turn, received {player}, expected {self.game.current_player}"    
    
    def run_movement_action(self, action:int, player:int) -> tuple:
        pos, facing,mov_type = self.enc_int_tuple[action]
        mech_player = list(self.game.get_game_status().mechs[player].values())[0]
        self.game.run_move_action(player=player,action=MoveAction(mech=mech_player,target_position=pos,target_facing=facing,movement_type=mov_type))
        ''' TODO mech2 estatic'''
        self.game.complete_current_phase_and_start_next()
        
        if self.game.current_phase==GamePhase.SHOOTING_PHASE:
            self.game.next_turn()
            self.game.run_initative_action(forced_player=PLAYER_1)
        return self.run_action_return()
      
    
    def get_allowed_actions_bits(self, player:int):
        allowed_actions = self.game.get_allowed_movements(player=player)
        ''' allwed_actions is a dictionay  [Movemnt][(cell, Facing)]=1'''
        bits = [0]*self.get_action_space()
        mech1_allowed_actions =list( allowed_actions.values())[0]
        for mt,cells in mech1_allowed_actions.items():
            for position,facing in cells:
                position = self.enc_tuple_int[(position, facing, mt)]
                bits[position]=1
        return bits

    
    
    def get_action_space(self):
       return self.action_dim
    
    def get_observation_space(self):
        return self.obs_dim
            