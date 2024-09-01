

import uuid

from simulation.games.BTGame import PLAYER_1, PLAYER_2, MoveAction
from simulation.games.BT_Beginner_box_game import BTBeginnerBoxGame,GamePhase
from simulation.model.board import Board
import simulation.model.factory as factory
from simulation.model.mech import Action,  MovementType,MechState
from simulation.utils.utils import Axial, Facing



sample_cells =          ["00","00","00","00","00","00","00","00","00","00","00","00","00","00","00",
                        "00","00","00","00","00","00","00","00","00","00","00","01","02","00","00",
                        "00","00","00","00","00","00","00","00","00","00","01","02","00","00","00",
                        "00","00","00","00","00","00","00","00","00","01","01","00","00","00","00",
                        "00","02","02","01","00","00","00","00","00","01","00","00","00","00","00",
                        "00","00","00","01","00","00","00","00","00","00","00","00","00","00","00",
                        "00","00","00","00","00","00","00","00","00","00","00","00","00","00","00",
                        "00","00","00","00","00","00","00","00","00","00","00","00","00","00","00",
                        "00","00","00","00","00","00","00","00","00","00","00","00","02","00","00",
                        "00","00","00","00","00","00","00","00","00","00","00","00","01","02","00",
                        "00","00","00","00","00","00","00","00","00","00","00","01","01","00","00",
                        "00","00","00","00","00","00","00","00","00","00","00","00","00","00","00",
                        "00","00","00","00","00","00","00","00","00","00","00","00","00","00","00",
                        "00","00","00","00","00","02","00","00","00","00","00","00","00","00","00",
                        "00","00","00","00","01","01","00","00","00","00","00","00","00","00","00",
                        "00","00","00","00","00","01","00","00","00","00","00","00","00","00","00",
                        "00","00","00","00","00","00","00","00","00","00","00","00","00","00","00"]

def load_game():

     game = factory.build_game(sample_cells,width=15, height=17, num_turns=5,
                               mechs_p1=[factory.build_mech(factory.Griffin_GRF_1N,Axial(1,15), Facing.face_N)],
                               mechs_p2=[factory.build_mech(factory.Wolverine_WVR_6N,Axial(13,-6), Facing.face_N)])
     
 
MECH_ID_P1_1="mech_1"
MECH_ID_P2_1="mech_2"   

def load_game_3()->BTBeginnerBoxGame:
     sample_cells = ["01","00","00",    "00","02","00",   "00","00","01"]
     game = factory.build_game(sample_cells,width=3, height=3, num_turns=5,
                               mechs_p1=[factory.build_mech(factory.Griffin_GRF_1N,Axial(0,0), Facing.face_N,mech_id=MECH_ID_P1_1)],
                               mechs_p2=[factory.build_mech(factory.Wolverine_WVR_6N,Axial(2,0), Facing.face_SW,mech_id=MECH_ID_P2_1)])
     return game

''' BTGame ****************************'''
def test_BTGame_constructor():
     try:
          game = load_game_3()
          assert len(game.has_mech_alrady_moved[0])==1
          assert MECH_ID_P1_1 in game.has_mech_alrady_moved[0]
          assert not game.has_mech_alrady_moved[0][MECH_ID_P1_1]
          assert "m1w1" in game.has_weapon_alrady_fired[0]
          assert not game.has_weapon_alrady_fired[0]["m1w1"]
          
     except Exception as e:
        assert False,e


def test_get_player_mechs():
     try:
          game = load_game_3()
          mechs = game.get_player_all_mechs(player=PLAYER_1)
          assert mechs[0].mech_id == MECH_ID_P1_1
          mechs = game.get_player_all_mechs(player=PLAYER_2)
          assert mechs[0].mech_id == MECH_ID_P2_1
          
     except Exception as e:
        assert False,e   
       
def test_get_player_mech():
     try:
          game = load_game_3()
          mech = game.get_player_mech(player=PLAYER_1,mech_id=MECH_ID_P1_1)
          assert mech.mech_id == MECH_ID_P1_1
          try:
               mech = game.get_player_mech(player=PLAYER_2, mech_id="nooo")
               assert False,"expcetion expected"
          except Exception:
               assert True
          
     except Exception as e:
        assert False,e      
    
def test_get_board():
     try:
          game = load_game_3()
          board = game.get_board()
          assert board.width == 3 and board.height==3
          
     except Exception as e:
        assert False,e   

def test_complete_phase():
     try:
          game = load_game_3()
          game.next_turn()
          current_phase = game.current_phase
          assert not game.is_phase_completed()
          game.complete_current_phase()
          assert  game.is_phase_completed()
          assert  game.phases_completed[current_phase]
     except Exception as e:
        assert False,e   

def test_move_to_next_phase():
   
          game = load_game_3()
          game.next_turn()
          former_phase = game.current_phase
          try:
               game.next_phase()
               assert False,"exception expected"
          except Exception as e:
               assert True
          game.complete_current_phase()
          game.next_phase()
          assert  former_phase.value+1==game.current_phase.value
          assert game.phases_completed[former_phase]
          assert not game.phases_completed[game.current_phase]
  
def test_run_initative_action():
     try:
          game = load_game_3()
          game.next_turn()
          player = game.run_initative_action(forced_player=PLAYER_1)
          assert player==PLAYER_1
          assert game.current_phase==GamePhase.MOVEMENT_PHASE
     except Exception as e:
        assert False,e         
        
        
def test_run_move_action():
     try:
          game = load_game_3()
          game.next_turn()
          player = game.run_initative_action(forced_player=PLAYER_1)
          mechs = game.get_player_all_mechs(player=player)     
          game.run_move_action(PLAYER_1,MoveAction(mech=mechs[0],target_position=Axial(1,1),target_facing=Facing.face_S, movement_type=MovementType.mv_walk))
          assert game.has_mech_alrady_moved[0][MECH_ID_P1_1]
          assert mechs[0].position==Axial(1,1)
          
     except Exception as e:
        assert False,e  




def test_next_turn():
     try:
          game = load_game_3()
          game.next_turn()
          t1 = game.current_turn
          player = game.run_initative_action(forced_player=PLAYER_1)
          mechs = game.get_player_all_mechs(player=PLAYER_1)
          game.run_move_action(PLAYER_1,MoveAction(mech=mechs[0],target_position=Axial(1,1),target_facing=Facing.face_S, movement_type=MovementType.mv_walk))
          game.next_turn()
          t2 = game.current_turn
          assert not game.has_mech_alrady_moved[0][MECH_ID_P1_1]
          assert t1+1==t2
     except Exception as e:
        assert False,e  

def test_entry_log():
     try:
          game = load_game_3()
          game.next_turn()
          assert len(game.log)==3
     except Exception as e:
        assert False,e  
          
     
def test_run_end_turn_action():
     try:
          game = load_game_3()
          game.next_turn()
          game.complete_current_phase()
          game.next_phase()
          assert game.current_phase==GamePhase.MOVEMENT_PHASE
          game.complete_current_phase()
          game.next_phase()
          assert game.current_phase==GamePhase.SHOOTING_PHASE
          game.complete_current_phase()
          game.next_phase()
          assert game.current_phase==GamePhase.END_PHASE
          game.run_end_turn_action()
          assert game.current_phase==GamePhase.INITIAL_PHASE
          assert game.current_turn==2
     except Exception as e:
        assert False,e  
     
     
     
     

def test_get_game_status():
     try:
          game = load_game_3()
          game.next_turn()
          gameStatus = game.get_game_status()
          assert gameStatus.mechs[0][MECH_ID_P1_1].mech_id ==MECH_ID_P1_1
          assert gameStatus.mechs[1][MECH_ID_P2_1].mech_id ==MECH_ID_P2_1
          assert len(gameStatus.log)==3
     except Exception as e:
        assert False,e  

def test_get_next_player():
     try:
          game = load_game_3()
          player = game.get_next_player(PLAYER_1)
          assert player==PLAYER_2
     except Exception as e:
        assert False,e  
        
def test_next_player_movement():
     try:
          game = load_game_3()
          game.next_turn()
          player = game.run_initative_action(forced_player=PLAYER_1)
          mechs = game.get_player_all_mechs(player=PLAYER_1)
          game.run_move_action(PLAYER_1,MoveAction(mech=mechs[0],target_position=Axial(1,1),target_facing=Facing.face_S, movement_type=MovementType.mv_walk))
          assert game.current_player==PLAYER_2
     
     except Exception as e:
           assert False,e  

'''BTBeginnerBoxGame ****************************'''
def test_get_allowed_movements():
     try:
          game = load_game_3()
          all_movs = game.get_allowed_movements(PLAYER_1)
          movs = all_movs[MECH_ID_P1_1]
          assert len(movs[MovementType.mv_walk])>0
          assert len(movs[MovementType.mv_run])>0
          assert len(movs[MovementType.mv_jump])>0
     except Exception as e:
        assert False,e  
     