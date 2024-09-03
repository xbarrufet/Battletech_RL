


from rl.obs_bits.BT_beginner_environment import BTBeginnerBoxEnvironment
from simulation.utils import utils
from test import factory_test


def test_encoding_number():
    res1 = utils._encoding_number(number=4, num_bits=5)
    assert sum(res1)==1
    assert res1[4]==1
    res1 = utils._encoding_number(number=10, num_bits=5, max_value=125)
    assert sum(res1)==1
    assert res1[0]==1
    res1 = utils._encoding_number(number=53, num_bits=5, max_value=125)
    assert sum(res1)==1
    assert res1[2]==1


def test_observations():
    try:
        game = factory_test.load_game_small()
        env = BTBeginnerBoxEnvironment(game)
        observations = env.get_observations() 
        print(observations)
        assert True
    except Exception as e:
        print(e)
        assert False
    
