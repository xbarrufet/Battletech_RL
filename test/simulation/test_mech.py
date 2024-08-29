

import uuid
from simulation.model.board import Board
import simulation.model.factory as factory
from simulation.model.mech import BattleMech
from simulation.model.mech_utils import Action, Location, Movement, MovementDirection
from simulation.model.weapon import Weapon
from simulation.utils.utils import Axial, Facing


def build_test_mech(position:Axial,face=Facing ):
   return  BattleMech(mech_type="Test Mech", mech_id=uuid.uuid1(), movement=[5,8,5], 
                     weapons=[Weapon(name="Medium Laser HD", damage=5, range=[3,6,9],volley_number=1,location= Location.loc_Head, initial_ammo=-1)],
                     base_armor=[9, 20, 16, 16, 20, 16, 16, 20], deployment_position=position, facing=face)

def build_test_mech_missile(position:Axial,face=Facing ):
   return  BattleMech(mech_type="Test Mech", mech_id=uuid.uuid1(), movement=[5,8,5], 
                     weapons=[Weapon(name="Missile", damage=5, range=[3,6,20],volley_number=7,location= Location.loc_Head, initial_ammo=10)],
                     base_armor=[9, 20, 16, 16, 20, 16, 16, 20], deployment_position=position, facing=face)


sample_cells =          ["00","00","00","00","00","00","00","00","00","00","00","00","00","00","00",
                        "01","00","00","00","00","00","00","00","00","00","00","00","00","00","00",
                        "01","00","00","00","00","00","00","00","00","00","00","00","00","00","00",
                        "00","00","00","00","00","00","00","00","00","00","00","00","00","00","00",
                        "00","00","00","00","00","00","00","00","00","00","00","00","00","00","00",
                        "00","00","00","00","00","00","00","00","00","00","00","00","00","00","00",
                        "02","00","00","00","00","00","00","00","00","00","00","00","00","00","00",
                        "00","00","00","00","00","00","00","00","00","00","00","00","00","00","00",
                        "00","00","00","00","00","00","00","00","00","00","00","00","00","00","00",
                        "00","00","00","00","00","00","00","00","00","00","00","00","00","00","00",
                        "00","00","00","00","00","00","00","00","00","00","00","00","00","00","00",
                        "00","00","00","00","00","00","00","00","00","00","00","00","00","00","00",
                        "00","00","00","00","00","00","00","00","00","00","00","00","00","00","00",
                        "00","00","00","00","00","00","00","00","00","00","00","00","00","00","00",
                        "00","00","00","00","00","00","00","00","00","00","00","00","00","00","00",
                        "00","00","00","00","00","00","00","00","00","00","00","00","00","00","00",
                        "00","00","00","00","00","00","00","00","00","00","00","00","00","00","00"]


def test_travessed_hex():
    board = Board(width=15,height=17,cells=sample_cells)
    position_ini = Axial(3,3)
    mech =factory.build_mech(mech_type=factory.Griffin_GRF_1N,position=position_ini,facing=Facing.face_SE)
    board.deploy_mech(position_ini)
    mech.start_move(Movement.mv_walk)
    mech.move_mech(MovementDirection.md_forward,board=board)
    mech.move_mech(MovementDirection.md_backward,board=board)
    mech.move_mech(MovementDirection.md_backward,board=board)
    mech.move_mech(MovementDirection.md_forward,board=board)
    mech.move_mech(MovementDirection.md_forward,board=board)
    assert mech.get_num_of_travessed_cells()==2

def test_fire_weapon_in_range_faced_with_visibility():
    try:    
        board = Board(width=15,height=17,cells=sample_cells)
        position_mech = Axial(0,0)
        position_target = Axial(0,3)
        board.deploy_mech(position_mech)
        board.deploy_mech(position_target)
        mech =factory.build_mech(mech_type=factory.Griffin_GRF_1N,position=position_mech,facing=Facing.face_S)
        mech_target =factory.build_mech(mech_type=factory.Wolverine_WVR_6N,position=position_target,facing=Facing.face_S)
        damage = mech.fire_weapons(target_position=mech_target.position,targe_travessed_cells=mech_target.get_num_of_travessed_cells(),board=board)
        expected_damage = 9
        assert damage==expected_damage
        assert mech.turn_damage_done==damage
    except Exception as e:
         print(e)
         assert False


def test_fire_weapon_in_range_not_faced_with_visibility():
    try:    
        board = Board(width=15,height=17,cells=sample_cells)
        position_mech = Axial(0,0)
        position_target = Axial(0,6)
        board.deploy_mech(position_mech)
        board.deploy_mech(position_target)
        mech =factory.build_mech(mech_type=factory.Griffin_GRF_1N,position=position_mech,facing=Facing.face_N)
        mech_target =factory.build_mech(mech_type=factory.Wolverine_WVR_6N,position=position_target,facing=Facing.face_S)
        damage = mech.fire_weapons(target_position=mech_target.position,targe_travessed_cells=mech_target.get_num_of_travessed_cells(),board=board)
        expected_damage = 0
        assert damage==expected_damage
    except Exception as e:
         print(e)
         assert False

def test_fire_weapon_in_range_faced_with_no_visibility():
    try:    
        board = Board(width=15,height=17,cells=sample_cells)
        position_mech = Axial(0,0)
        position_target = Axial(0,3)
        board.deploy_mech(position_mech)
        board.deploy_mech(position_target)
        mech =factory.build_mech(mech_type=factory.Griffin_GRF_1N,position=position_mech,facing=Facing.face_N)
        mech_target =factory.build_mech(mech_type=factory.Wolverine_WVR_6N,position=position_target,facing=Facing.face_S)
        damage = mech.fire_weapons(target_position=mech_target.position,targe_travessed_cells=mech_target.get_num_of_travessed_cells(),board=board)
        expected_damage = 0
        assert damage==expected_damage
    except Exception as e:
         print(e)
         assert False

def test_fire_weapon_no_range_faced_with_no_visibility():
    try:    
        board = Board(width=15,height=17,cells=sample_cells)
        position_mech = Axial(1,0)
        position_target = Axial(0,13)
        board.deploy_mech(position_mech)
        board.deploy_mech(position_target)
        mech =build_test_mech(position=position_mech,face=Facing.face_S)
        mech_target =factory.build_mech(mech_type=factory.Wolverine_WVR_6N,position=position_target,facing=Facing.face_S)
        damage = mech.fire_weapons(target_position=mech_target.position,targe_travessed_cells=mech_target.get_num_of_travessed_cells(),board=board)
        expected_damage = 0
        assert damage==expected_damage
    except Exception as e:
         print(e)
         assert False

def test_fire_weapon_ammo_consumption():
    try:    
        board = Board(width=15,height=17,cells=sample_cells)
        position_mech = Axial(1,0)
        position_target = Axial(1,5)
        board.deploy_mech(position_mech)
        board.deploy_mech(position_target)
        mech =build_test_mech_missile(position=position_mech,face=Facing.face_S)
        mech_target =factory.build_mech(mech_type=factory.Wolverine_WVR_6N,position=position_target,facing=Facing.face_S)
        damage = mech.fire_weapons(target_position=mech_target.position,targe_travessed_cells=mech_target.get_num_of_travessed_cells(),board=board)
        remainig_ammo = mech.weapons[0].remaining_ammo
        assert remainig_ammo==3
    except Exception as e:
         print(e)
         assert False

   