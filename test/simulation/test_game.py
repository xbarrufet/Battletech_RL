

import uuid

from simulation.games.BTGame import PLAYER_1, PLAYER_2, MoveAction
from simulation.games.BT_Beginner_box_game import BTBeginnerBoxGame,GamePhase
from simulation.model.board import Board
from simulation.model.mech import Action,  MovementType,MechState
from simulation.utils.utils import Axial, Facing
from test.factory_test import MECH_ID_P1_1, MECH_ID_P2_1, load_game_small



''' BTGame ****************************'''
def test_BTGame_constructor():
     try:
          game = load_game_small()
          assert len(game.has_mech_alrady_moved)==2
          assert MECH_ID_P1_1 in game.has_mech_alrady_moved
          assert not game.has_mech_alrady_moved[MECH_ID_P1_1]
          assert MECH_ID_P1_1 + "_m1w1" in game.has_weapon_alrady_fired
          assert not game.has_weapon_alrady_fired[MECH_ID_P1_1 + "_m1w1"]
          
     except Exception as e:
        assert False,e


def test_get_player_mechs():
     try:
          game = load_game_small()
          mechs = game.get_player_all_mechs(player=PLAYER_1)
          assert mechs[0].mech_id == MECH_ID_P1_1
          mechs = game.get_player_all_mechs(player=PLAYER_2)
          assert mechs[0].mech_id == MECH_ID_P2_1
          
     except Exception as e:
        assert False,e   
       
def test_get_player_mech():
     try:
          game = load_game_small()
          mech = game.get_mech(mech_id=MECH_ID_P1_1)
          assert mech.mech_id == MECH_ID_P1_1
          try:
               mech = game.get_mech( mech_id="nooo")
               assert False,"expcetion expected"
          except Exception:
               assert True
          
     except Exception as e:
        assert False,e      
    
def test_get_board():
     try:
          game = load_game_small()
          board = game.get_board()
          assert board.width == 3 and board.height==3
          
     except Exception as e:
        assert False,e   

def test_complete_phase():
     try:
          game = load_game_small()
          game.next_turn()
          current_phase = game.current_phase
          assert not game.is_phase_completed()
          game.complete_current_phase()
          assert  game.is_phase_completed()
          assert  game.phases_completed[current_phase]
     except Exception as e:
        assert False,e   

def test_move_to_next_phase():
   
          game = load_game_small()
          game.next_turn()
          former_phase = game.current_phase
          try:
               game.next_phase()
               assert False,"exception expected"
          except Exception as e:
               assert True
          game.run_initative_action(forced_player=PLAYER_1)     
          assert  former_phase.value+1==game.current_phase.value
          assert game.phases_completed[former_phase]
          assert not game.phases_completed[game.current_phase]
  
def test_run_initative_action():
     try:
          game = load_game_small()
          game.next_turn()
          player = game.run_initative_action(forced_player=PLAYER_1)
          assert player==PLAYER_1
          assert game.current_phase==GamePhase.MOVEMENT_PHASE
     except Exception as e:
        assert False,e         
        
        
def test_run_move_action():
     try:
          game = load_game_small()
          game.next_turn()
          player = game.run_initative_action(forced_player=PLAYER_1)
          mechs = game.get_player_all_mechs(player=player)     
          game.run_move_action(PLAYER_1,MoveAction(mech=mechs[0],target_position=Axial(1,1),target_facing=Facing.face_S, movement_type=MovementType.mv_walk))
          assert game.has_mech_alrady_moved[MECH_ID_P1_1]
          assert mechs[0].position==Axial(1,1)
          
     except Exception as e:
        assert False,e  




def test_next_turn():
     try:
          game = load_game_small()
          game.next_turn()
          t1 = game.current_turn
          player = game.run_initative_action(forced_player=PLAYER_1)
          mechs = game.get_player_all_mechs(player=PLAYER_1)
          game.run_move_action(PLAYER_1,MoveAction(mech=mechs[0],target_position=Axial(1,1),target_facing=Facing.face_S, movement_type=MovementType.mv_walk))
          game.next_turn()
          t2 = game.current_turn
          assert not game.has_mech_alrady_moved[MECH_ID_P1_1]
          assert t1+1==t2
     except Exception as e:
        assert False,e  

def test_entry_log():
     try:
          game = load_game_small()
          assert len(game.log)==3
     except Exception as e:
        assert False,e  
          
     
def test_run_end_turn_action():
     try:
          game = load_game_small()
          player = game.run_initative_action(forced_player=PLAYER_1)
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
     
     

def test_get_next_player():
     try:
          game = load_game_small()
          player = game.get_next_player(PLAYER_1)
          assert player==PLAYER_2
     except Exception as e:
        assert False,e  
        
def test_next_player_movement():
     try:
          game = load_game_small()
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
          game = load_game_small()
          all_movs = game.get_allowed_movements(PLAYER_1)
          movs = all_movs[MECH_ID_P1_1]
          assert len(movs[MovementType.mv_walk])>0
          assert len(movs[MovementType.mv_run])>0
          assert len(movs[MovementType.mv_jump])>0
     except Exception as e:
        assert False,e  
     