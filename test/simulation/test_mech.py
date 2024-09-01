

import uuid
from simulation.model.board import Board
import simulation.model.factory as factory
from simulation.model.mech import BattleMech
from simulation.model.mech_utils import Action, Location, MovementType, MovementDirection
from simulation.model.weapon import Weapon
from simulation.utils.utils import Axial, Facing


def build_test_mech(position:Axial,face=Facing ):
   return  BattleMech(mech_type="Test Mech", mech_id=uuid.uuid1(), movement=[5,8,5], 
                     weapons=[Weapon(weapon_id=uuid.uuid1(),name="Medium Laser HD", damage=5, range=[3,6,9],volley_number=1,location= Location.loc_Head, initial_ammo=-1)],
                     base_armor=[9, 20, 16, 16, 20, 16, 16, 20], deployment_position=position, facing=face)

def build_test_mech_missile(position:Axial,face=Facing ):
   return  BattleMech(mech_type="Test Mech", mech_id=uuid.uuid1(), movement=[5,8,5], 
                     weapons=[Weapon(weapon_id=uuid.uuid1(),name="Missile", damage=5, range=[3,6,20],volley_number=7,location= Location.loc_Head, initial_ammo=10)],
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
