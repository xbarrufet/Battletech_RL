
from dataclasses import dataclass
from simulation.model import mech_utils



class WeaponStats:
    def __init__(self,name: str,damage: int ,range: list[int],volley_number: int) -> None:
        self.name=name
        self.damage=damage
        self.range=range
        self.volley_number=volley_number
    

class Weapon(WeaponStats):
    def __init__(self, name: str,damage: int ,range: list[int],location:mech_utils.Location, initial_ammo:int =-1,volley_number: int=1) -> None:
        WeaponStats.__init__(self, name=name, damage=damage, range=range, volley_number=volley_number)
        self.location=location
        self.initial_ammo=initial_ammo
        self.remaining_ammo = initial_ammo

    def reset_weapon(self):
         self.remaining_ammo=self.initial_ammo    

    def fire_weapon(self, gunner_skill,distance,attacker_movement_type, target_modifier,terrain_modifier)->int:
         if distance>self.range[mech_utils.Range.range_Long.value]:
             return 0
         result = gunner_skill
         result += mech_utils.table_attacker_movement(attacker_movement_type)
         result += mech_utils.table_target_movement(target_modifier)
         result += mech_utils.table_other_modifiers(terrain_modifier)
         result += mech_utils.table_range_modfier(distance=distance, range=self.range)
         prob = mech_utils.dice_2D6_prob(result)  
         damage_done=0
         volley_number=1
         if self.initial_ammo>0:
            volley_number = min(self.remaining_ammo,self.volley_number)
            self.remaining_ammo-=volley_number       
         damage_done = self.calculate_damage(prob=prob,volley_number=volley_number)     
         return damage_done 

    def calculate_damage(self,prob, volley_number=1)->int:
         if self.volley_number==1:
              return self.damage*prob
         else:
              return mech_utils.table_volley_hits(self.volley_number)* self.damage * prob
