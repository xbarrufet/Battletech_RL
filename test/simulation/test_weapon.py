

from simulation.model.mech_utils import Location, Movement
import simulation.model.mech_utils as mech_utils
from simulation.model.weapon import Weapon


#MediumLaserHD = WeaponStats(name="Medium Laser HD", damage=5, weapon_range=[3,6,9],volley_number=1)
#SRM6 = WeaponStats(name="SRM 6", damage=2, weapon_range=[3,6,9], use_ammo=True, volley_number=6)
#AC5 = WeaponStats(name="A/C 5", damage=5, weapon_range=[6,12,18],volley_number=1)




def test_fire_weapon_no_volley():
    weapon = Weapon(name="Medium Laser HD", damage=5, range=[3,6,9],volley_number=1,location= Location.loc_Head, initial_ammo=-1)
    damage = weapon.fire_weapon(gunner_skill=4 ,distance=1, attacker_movement_type=Movement.mv_walk, target_modifier=0, terrain_modifier=0)
    value = 4 + 1 + 0 + 0 +0
    prob = mech_utils.dice_2D6_prob(value)
    damaga_expected =prob*weapon.damage
    assert damage == damaga_expected


def test_fire_weapon_volley():
    weapon = Weapon(name="SRM 6", damage=2, range=[3,6,9], volley_number=6,location= Location.loc_Head, initial_ammo=10)
    
    damage = weapon.fire_weapon(gunner_skill=4 ,distance=8, attacker_movement_type=Movement.mv_walk, target_modifier=0, terrain_modifier=0)
    value = 4 + 1 + 0 + 0 +4
    prob = mech_utils.dice_2D6_prob(value)
    damaga_expected =prob*weapon.damage * 4
    assert damage == damaga_expected

def test_fire_weapon_no_range():
    weapon = Weapon(name="SRM 6", damage=2, range=[3,6,9], volley_number=6,location= Location.loc_Head, initial_ammo=10)
    damage = weapon.fire_weapon(gunner_skill=4 ,distance=12, attacker_movement_type=Movement.mv_walk, target_modifier=0, terrain_modifier=0)
    assert damage == 0

def test_fire_weapon_too_many_constratints():
    weapon = Weapon(name="SRM 6", damage=2, range=[3,6,9], volley_number=6,location= Location.loc_Head, initial_ammo=10)
    damage = weapon.fire_weapon(gunner_skill=4 ,distance=8, attacker_movement_type=Movement.mv_run, target_modifier=8, terrain_modifier=2)
    assert damage == 0

    