

import uuid

from simulation.games.BT_Beginner_box_game import BTGame, GamePhase
from simulation.model.board import Board
import simulation.model.factory as factory
from simulation.model.mech import Action,  Movement,MechState
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
     
     return game

def load_game_2():
     
     game = factory.build_game(sample_cells,width=15, height=17, num_turns=5,
                               mechs_p1=[factory.build_mech(factory.Griffin_GRF_1N,Axial(0,0), Facing.face_SE)],
                               mechs_p2=[factory.build_mech(factory.Wolverine_WVR_6N,Axial(1,0), Facing.face_NW)])
     return game

def load_game_3()->BTGame:
     sample_cells = ["01","00","00",    "00","02","00",   "00","00","01"]
     game = factory.build_game(sample_cells,width=3, height=3, num_turns=5,
                               mechs_p1=[factory.build_mech(factory.Griffin_GRF_1N,Axial(0,0), Facing.face_N)],
                               mechs_p2=[factory.build_mech(factory.Wolverine_WVR_6N,Axial(2,0), Facing.face_SW)])
     return game


def test_select_movement():
     game = load_game()        
     mech =game.p1_mech
     try:
         game.run_action(mech_id=mech.mech_id,action=Action.ACT_SELECT_WALK_MOVEMENT_TYPE)
         assert game.p1_mech.movementType==Movement.mv_walk
         assert game.p1_mech.current_state==MechState.ST_WALKING
     except Exception as e:
         print(e)
         assert False


def test_move_walk():
     
     try:
          game = load_game()        
          mech =game.p1_mech
          pos_ini = mech.position
          game.run_action(mech_id=mech.mech_id,action=Action.ACT_SELECT_WALK_MOVEMENT_TYPE)
          game.run_action(mech_id=mech.mech_id,action=Action.ACT_MOVE_FORWARD)
          pos_f = mech.position
          assert pos_f[0] == pos_ini[0]
          assert pos_f[1] == pos_ini[1]-1
          game.run_action(mech_id=mech.mech_id,action=Action.ACT_MOVE_BACKWARD)
          pos_f2 = mech.position
          assert pos_f2[0] == pos_ini[0]
          assert pos_f2[1] == pos_ini[1]
     
          assert mech.movementType==Movement.mv_walk
     except Exception as e:
         print(e)
         assert False


def test_move_facing():
     game = load_game()        
     mech = game.p1_mech
     pos_ini = mech.position
     game.run_action(mech_id=mech.mech_id,action=Action.ACT_SELECT_WALK_MOVEMENT_TYPE)
     game.run_action(mech_id=mech.mech_id,action=Action.ACT_ROTATE_RIGHT)
     assert mech.facing == Facing.face_NE
     game.run_action(mech_id=mech.mech_id,action=Action.ACT_MOVE_FORWARD)
     pos_f = mech.position
     assert pos_f[0] == pos_ini[0]+1
     assert pos_f[1] == pos_ini[1]-1


def test_get_allowed_actions():
     game = load_game_2()        
     mech = game.p1_mech
     aa = mech.build_allowed_actions(board=game.board)
     assert len(aa)==2
     game.run_action(mech_id=mech.mech_id,action=Action.ACT_SELECT_WALK_MOVEMENT_TYPE)
     aa = mech.build_allowed_actions(board=game.board)
     assert len(aa)==3
     assert Action.ACT_MOVE_FORWARD not in aa
     assert Action.ACT_MOVE_BACKWARD not in aa

def test_end_movement():
     game = load_game()        
     mech = game.p1_mech
     try:
          game.run_action(mech_id=mech.mech_id,action=Action.ACT_SELECT_WALK_MOVEMENT_TYPE)
          for _ in range(mech.movement[0]):
               game.run_action(mech_id=mech.mech_id,action=Action.ACT_NO_MOVEMENT)
          assert mech.current_state==MechState.ST_WAITING
     except Exception as e:
         print(e)
         assert False

def test_turn_change():
     try:
          game = load_game()        
          mech = game.p1_mech
          mech2 = game.p2_mech

          game.run_action(mech_id=mech.mech_id,action=Action.ACT_SELECT_WALK_MOVEMENT_TYPE)
          for _ in range(5):
               game.run_action(mech_id=mech.mech_id,action=Action.ACT_ROTATE_RIGHT)

          game.run_action(mech_id=mech2.mech_id,action=Action.ACT_SELECT_WALK_MOVEMENT_TYPE)
          for _ in range(5):
               game.run_action(mech_id=mech2.mech_id,action=Action.ACT_ROTATE_RIGHT)
          assert game.gameStatus.current_phase==GamePhase.SHOOTING_PHASE and mech.current_state==MechState.ST_READY_TO_FIRE and mech2.current_state==MechState.ST_WAITING

          game.run_action(mech_id=mech.mech_id,action=Action.ACT_FIRE_WEAPONS,parameters=mech2)
          assert game.gameStatus.current_phase==GamePhase.SHOOTING_PHASE and mech.current_state==MechState.ST_WAITING and mech2.current_state==MechState.ST_READY_TO_FIRE

          game.run_action(mech_id=mech2.mech_id,action=Action.ACT_FIRE_WEAPONS,parameters=mech)

          assert game.gameStatus.current_phase==GamePhase.MOVEMENT_PHASE and mech.current_state==MechState.ST_READY_TO_MOVE and mech2.current_state==MechState.ST_WAITING
     except Exception as e:
         print(e)
         assert False

def test_game_factory():
     Board_Sample = Board(width=15, height=17, cells=sample_cells)
     id1 = uuid.uuid1()
     id2 = uuid.uuid1()
     game = factory.build_game(sample_cells,width=15, height=17, num_turns=5,
                               mechs_p1=[factory.build_mech(factory.Griffin_GRF_1N,Axial(1,15), Facing.face_N)],
                               mechs_p2=[factory.build_mech(factory.Wolverine_WVR_6N,Axial(13,-6), Facing.face_N)])
     
     assert game.board.get_cell(Axial(1,15)).occupied
     assert game.board.get_cell(Axial(13,-6)).occupied
     assert not game.board.get_cell(Axial(0,0)).occupied
