import copy
from enum import Enum
import math

import pygame
from simulation.UI.hex_grid_board import HexGrid
from simulation.utils.utils import axial_to_oddq,position_distance
from simulation.games.BT_Beginner_box_game import  BTGame, GamePhase, MechState
from simulation.model.board import Board
from simulation.model.mech import Action, BattleMech, Movement, MovementDirection




WIDTH, HEIGHT = 600, 800
TOTAL_WIDTH,TOTAL_HEIGHT = 1200,800


class BTEnvironment:

    def __init__(self, game:BTGame,render=False) -> None:
        self.copy_game = game
        self.game =game

        self.render = render
        self.uiboard = HexGrid(origin_x=0,origin_y=0,
                               map_width= self.game.board.width, map_height= self.game.board.height,
                               map_screen_width=WIDTH,map_screen_height=HEIGHT)
        self.screen = None
        self.running=False
        self.clock = None
        if self.render:
               pygame.init()
               self.screen = pygame.display.set_mode(( TOTAL_WIDTH, TOTAL_HEIGHT))
               self.clock = pygame.time.Clock()    
               self.running=True
        self.steps=0

    def reset(self):
        self.game =copy.deepcopy(self.copy_game)
        self.render_state()
        self.steps=0
        return self.get_observations()

    def render_state(self):
        if self.render:
            self.uiboard.draw_board(screen=self.screen,board=self.game.board)
            self.uiboard.draw_unit(screen=self.screen, mech=self.game.p1_mech)
            self.uiboard.draw_unit(screen=self.screen, mech=self.game.p2_mech)
            pygame.display.flip()
            self.clock.tick(60)

    def build_action_results(self,invalid_action=False):
        return self.get_observations(), self.get_reward(invalid_action), self.game.is_game_over() or self.steps>100

    def run_action(self, action:Action,parameters=None):
        
        if self.game.p1_mech.is_action_allowed(Action(action)):
            self.steps+=1
            mech2_id = self.game.p2_mech
            mech_id = self.game.p1_mech.mech_id
            self.game.run_action(mech_id=mech_id,action=Action(action))
            self.render_state()
            # check if some automatic actions needs to be done
            if self.game.gameStatus.has_player_ended and self.game.gameStatus.current_player==2:
                mech2_id = self.game.p2_mech
                # automatic player 2 movement
                if self.game.gameStatus.current_phase==GamePhase.MOVEMENT_PHASE:
                    self.game.run_action(mech2_id,Action.ACT_SELECT_NO_MOVEMENT)
                else:
                    # automatic player 2 fire phase
                    self.game.run_action(mech2_id,Action.ACT_FIRE_WEAPONS,self.game.p1_mech.mech_id)
            return self.build_action_results()
        else:
            return self.build_action_results(invalid_action=True)

    
    def get_allowed_actions_list(self)->list[int]:
       return self.game.get_allowed_actions()



    def get_allowed_actions_bits(self, allowed_actions:list[Action]=[]):
        if len(allowed_actions)==0:
            allowed_actions = self.get_allowed_actions_list()
        bits = [0]*len(Action)
        for a in allowed_actions:
            bits[a.value]=1
        return bits

    
    def get_observations(self):
        mech1=self.game.p1_mech
        mech2=self.game.p2_mech
        visibility = self.game.get_visibilties()
        gameStatus = self.game.gameStatus
        obs = []
        # obs.append(gameStatus.current_phase.value) #phase 
        # obs.append(mech1.current_state.value) #mech1 remaining movement
        # obs.append(mech2.current_state.value) #mech2 remaining movement
        # obs.append(mech1.remaining_movement) #mech1 remaining movement
        # obs.append(mech2.remaining_movement) #mech2 remaining movement
        # obs.append(mech1.facing.value) #mech1 facing
        # obs.append(mech2.facing.value) #mech2 facing
        d, v = self.game.board.check_visibility(mech1.position, mech2.position)
        obs.append(v ) #mech1 q
        obs.append(self.steps ) #mech1 q
        
        obs.append(mech1.position.q) #mech1 q
        obs.append(mech2.position.q) #mech2 q
        obs.append(mech1.position.r) #mech1 r
        obs.append(mech2.position.r) #mech2 r
        
        obs.append(mech1.turn_damage_received) #mech1 r
        obs.append(mech1.turn_damage_done) #mech2 r
        
        obs.append(visibility[0][0]) #distance m1->m2
        obs.append(visibility[0][1]) #visibility m1->m2
        #obs.append(visibility[1][0]) #distance m2->m1
        obs.append(visibility[1][1]) #visibility m1->m2
        

        bit_actions = self.get_allowed_actions_bits()
        #return (obs,bit_actions,self.game.get_forest_map())
        return (obs,bit_actions)


    def get_visibility_reward(self,v):
        distance, vis = v
        reward = 0 
        if distance<0:
            return -1
        else:
            if distance<5:
                reward = 0
            elif distance<10:
                reward = 1
            elif distance<15:
                reward = 2
            else:
                reward =3
            match vis:
                case 0:
                    reward +=1
                case 1:
                    reward +=2
                case 2:
                    reward +=2
                case _:
                    return -1
            reward = reward + vis
            return 1/reward



    def get_reward(self,invalid_action=False):
        m1,m2 = self.game.get_visibilties()
        m1_r =self. get_visibility_reward(m1)
        m2_r = self. get_visibility_reward(m2)*3
        if self.game.gameStatus.has_turn_ended:
            return m1_r-m2_r
        else:
            return  (m1_r-m2_r)/5
        
    def build_terrain_map(self)->list[list]:
        width, height = self.game.board.width,self.game.board.height
        terrain = [[0] * width for _ in range(height) ]
        cell_positions = self.game.board.cells.items()
        for pos,cell in cell_positions:
            x,y = axial_to_oddq(pos)
            terrain[y][x]= cell.cell_type.value
        return terrain
    
    def quit(self):
        pygame.quit()

    def get_action_space(self):
        return [Action(x).value for x in range(len(Action)) ]
    
    def get_observation_space_dims(self):
        return [11,len(Action)]
