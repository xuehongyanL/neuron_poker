"""Random player"""
import random
import numpy as np
from gym_env.env import Action
from gym_env.env import CommunityData
from gym_env.env import PlayerData
from gym_env.env import StageData
from tools.hand_evaluator import eval_best_hand

autplay = True  # play automatically if played against keras-rl


class FGF_Player:
    """Mandatory class with the player methods"""

    def __init__(self, name='FGF_Player'):
        """Initiaization of an agent"""
        self.equity_alive = 0
        self.actions = []
        self.last_action_in_stage = ''
        self.temp_stack = []
        self.name = name
        self.autoplay = True

    def action(self, action_space, observation, info):  # pylint: disable=no-self-use
        """Mandatory method that calculates the move based on the observation array and the action space."""
        _ = observation  # not using the observation for random decision
        _ = info

        this_player_action_space = {Action.FOLD, Action.CHECK, Action.CALL, Action.RAISE_POT, Action.RAISE_HALF_POT,
                                    Action.RAISE_2POT}
        possible_moves = this_player_action_space.intersection(set(action_space))
        action = random.choice(list(possible_moves))
        return action


class XN_Player:
    """Mandatory class with the player methods"""

    def __init__(self, name='XN_Player'):
        """Initiaization of an agent"""
        self.equity_alive = 0
        self.actions = []
        self.last_action_in_stage = ''
        self.temp_stack = []
        self.name = name
        self.autoplay = True

    def action(self, action_space, observation, info):  # pylint: disable=no-self-use
        """Mandatory method that calculates the move based on the observation array and the action space."""
        _ = observation  # not using the observation for random decision
        _ = info

        this_player_action_space = {Action.FOLD, Action.CHECK, Action.CALL, Action.RAISE_POT, Action.RAISE_HALF_POT,
                                    Action.RAISE_2POT}
        possible_moves = this_player_action_space.intersection(set(action_space))
        action = random.choice(list(possible_moves))
        return action


class XR_Player:
    """Mandatory class with the player methods"""

    def __init__(self, name='XR_Player'):
        """Initiaization of an agent"""
        self.equity_alive = 0
        self.actions = []
        self.last_action_in_stage = ''
        self.temp_stack = []
        self.name = name
        self.autoplay = True

    def action(self, action_space, observation, info):  # pylint: disable=no-self-use
        """Mandatory method that calculates the move based on the observation array and the action space."""
        _ = observation  # not using the observation for random decision
        _ = info

        this_player_action_space = {Action.FOLD, Action.CHECK, Action.CALL, Action.RAISE_POT, Action.RAISE_HALF_POT,
                                    Action.RAISE_2POT}
        possible_moves = this_player_action_space.intersection(set(action_space))
        action = random.choice(list(possible_moves))
        return action


def expectation(equity_alive, community_pot, my_pot):
    expect = equity_alive*community_pot - (1-equity_alive)*my_pot
    if(expect>=0):
        return True
    else:
        return False


class AI_Player:
    """Mandatory class with the player methods"""

    def __init__(self, name='AI_Player', min_call_equity=None, min_bet_equity=None):
        """Initiaization of an agent"""
        self.equity_alive = 0
        self.actions = []
        self.last_action_in_stage = ''
        self.temp_stack = []
        self.name = name
        self.autoplay = True
        self.min_call_equity = .56
        self.min_bet_equity = .66

    def action(self, action_space, observation, info):  # pylint: disable=no-self-use
        """Mandatory method that calculates the move based on the observation array and the action space."""
        global Current_stage
        Current_stage = 0
        _ = observation  # not using the observation for random decision
        Community = CommunityData(6)
        my_position=info['player_data']['position']
        equity_alive = info['player_data']['equity_to_river_alive']
        Stages = info['community_data']['stage']
        for i in range(len(Stages)):
            if Stages[i]:
                Current_stage = i  # 0-PREFLOP 1-FLOP 2-TURN 3-RIVER
                break
        Community_pot = Community.community_pot
        Current_round_pot = Community.current_round_pot
        Active_Players = Community.active_players
        # max_win = sum(Community_pot)
        if Current_stage == 0:  # PREFLOP
            if equity_alive > .25 and (
                    Action.RAISE_POT or Action.RAISE_HALF_POT) in action_space:
                seeds = random.randrange(0, 100)
                if seeds >= 50:
                    action = Action.RAISE_POT
                else:
                    action = Action.RAISE_HALF_POT

            elif equity_alive > .22 and (Action.RAISE_3BB ) in action_space:
                    action = Action.RAISE_3BB


            elif equity_alive > .15 and Action.CALL in action_space:
                    action = Action.CALL

            elif equity_alive > .14 and Action.CHECK in action_space:
                action = Action.CHECK
            else:  # terrible hand
                action = Action.FOLD

        elif Current_stage == 1:  # FLOP
            if equity_alive > .4 and Action.RAISE_HALF_POT in action_space:
                action = Action.RAISE_HALF_POT
            elif equity_alive > .33 and Action.RAISE_3BB in action_space:
                action = Action.RAISE_3BB
            elif equity_alive > .25 and Action.CALL in action_space:
                action = Action.CALL
            elif Action.CHECK in action_space:
                action = Action.CHECK
            else:
                action = Action.FOLD

        elif Current_stage == 2:  # TURN
            if equity_alive > .71 and Action.ALL_IN in action_space:
                action = Action.ALL_IN
            elif equity_alive > .6 and Action.RAISE_2POT in action_space:
                action = Action.RAISE_2POT
            elif equity_alive > .5 and Action.RAISE_POT in action_space:
                action = Action.RAISE_POT
            elif equity_alive > .4 and Action.RAISE_3BB in action_space:
                action = Action.RAISE_3BB
            elif equity_alive > .3 and Action.CALL in action_space:
                action = Action.CALL
            elif Action.CHECK in action_space:
                action = Action.CHECK
            else:
                action = Action.FOLD

        else:  # RIVER
            if equity_alive > .88 and Action.ALL_IN in action_space:
                action = Action.ALL_IN
            elif equity_alive > .70 and Action.RAISE_2POT in action_space:
                action = Action.RAISE_2POT
            elif equity_alive > .64 and Action.RAISE_POT in action_space:
                action = Action.RAISE_POT
            elif equity_alive > .60 and Action.RAISE_HALF_POT in action_space:
                action = Action.RAISE_HALF_POT
            elif equity_alive > .52 and Action.RAISE_3BB in action_space:
                action = Action.RAISE_3BB
            elif equity_alive > .5 and Action.CALL in action_space:
                action = Action.CALL
            elif Action.CHECK in action_space:
                action = Action.CHECK
            else:
                action = Action.FOLD
        # action = random.choice(list(possible_moves))
        return action
