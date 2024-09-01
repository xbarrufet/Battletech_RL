

from gym.BT_beginner_environment import BTBeginnerBoxEnvironment
from gym.BT_players import BTPlayer_Random
from rl.pg_agent_trainer import PGAgentTrainer
from simulation.games.BT_Beginner_box_game import BTBeginnerBoxGame
from simulation.model import factory


if __name__ == '__main__':
    game = factory.Game_Sample
    environment = BTBeginnerBoxEnvironment(game=game)
    agent_trainer = PGAgentTrainer(environment=environment,
                                   learning_rate=0.0001, 
                                   gamma=0.9, 
                                   result_model_filename="BeginnerBox_PolicyGradient.pgm",
                                   player_2=BTPlayer_Random())

    agent_trainer.train()