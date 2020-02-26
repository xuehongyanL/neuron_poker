"""
Modified by Xue Hongyan
"""
from gym_env.env import Action
import numpy as np

autoplay = True  # play automatically if played against keras-rl


class Player:
    """Mandatory class with the player methods"""

    def __init__(self, name='EnsembleEX'):
        """Initiaization of an agent"""
        self.equity_alive = 0
        self.name = name
        self.actions = []  # sequence of actions in one game
        self.choice = []  # sequence of agents don't follow
        self.weight = [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]
        # weight of 20 agents
        self.temp_stack = 2.50  # tempstack num
        self.previous_stage = 0
        self.fold = 1
        self.autoplay = True

    def oneaction(self, action_space, equity_alive, min_call_equity, min_bet_equity, increment1, increment2):
        if equity_alive > min_bet_equity + increment2 and Action.ALL_IN in action_space:
            action = Action.ALL_IN

        elif equity_alive > min_bet_equity + increment1 and Action.RAISE_2POT in action_space:
            action = Action.RAISE_2POT

        elif equity_alive > min_bet_equity and Action.RAISE_POT in action_space:
            action = Action.RAISE_POT

        elif equity_alive > min_bet_equity - increment1 and Action.RAISE_HALF_POT in action_space:
            action = Action.RAISE_HALF_POT

        elif equity_alive > min_call_equity and Action.CALL in action_space:
            action = Action.CALL

        elif Action.CHECK in action_space:
            action = Action.CHECK

        else:
            action = Action.FOLD

        return action

    def Isnewstage(self, stage, stack):
        if (self.fold == 1):
            return True
        elif (stage == 0):
            if (self.previous_stage != 0):
                return True
            elif (self.temp_stack < stack):
                return True
            else:
                return False
        else:
            return False
        return False

    def newweight(self, stack):
        if stack > self.temp_stack:
            for choice in self.choice:
                for j in range(20):
                    if j in choice:
                        self.weight[j] += 0.2
                    else:
                        self.weight[j] -= 0

        else:
            for choice in self.choice:
                for j in range(20):
                    if j in choice:
                        self.weight[j] -= 0
                    else:
                        self.weight[j] += 0.2

        self.fold = 0
        self.actions[:] = []
        self.choice[:] = []

    def action_to_int(self, action):
        if action == Action.FOLD:
            return 0
        elif action == Action.CHECK:
            return 1
        elif action == Action.CALL:
            return 2
        elif action == Action.RAISE_3BB:
            return 3
        elif action == Action.RAISE_HALF_POT:
            return 3
        elif action == Action.RAISE_POT:
            return 4
        elif action == Action.RAISE_2POT:
            return 5
        else:
            return 6

    def int_to_action(self, value):
        if value == 0:
            action = Action.FOLD
        elif value == 1:
            action = Action.CHECK
        elif value == 2:
            action = Action.CALL
        elif value == 3:
            action = Action.RAISE_HALF_POT
        elif value == 4:
            action = Action.RAISE_POT
        elif value == 5:
            action = Action.RAISE_2POT
        else:
            action = Action.ALL_IN
        return action

    def action(self, action_space, observation, info):  # pylint: disable=no-self-use
        """Mandatory method that calculates the move based on the observation array and the action space."""
        _ = observation
        equity_alive = info['player_data']['equity_to_river_alive']
        position = info['player_data']['position']

        stage_a = info['community_data']['stage'].index(1)
        print(stage_a)
        assert 0 <= stage_a < 4
        stack_a = info['player_data']['stack'][position]

        if self.Isnewstage(stage=stage_a, stack=stack_a):
            self.newweight(stack=stack_a)
            self.temp_stack = stack_a

        action_a = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
        for i in range(20):
            increment1 = (0.1 if (i // 10 == 0) else 0.15)
            increment2 = (0.2 if (i // 10 == 0) else 0.25)
            min_call_equity = (i % 10) / 5 * 0.2
            min_bet_equity = min_call_equity + 0.1 + (i % 2) * 0.1
            action_a[i] = self.action_to_int(
                self.oneaction(action_space, equity_alive, min_call_equity, min_bet_equity, increment1, increment2))
        action_b = 0
        sum = 0
        for i in range(20):
            action_b = action_b + action_a[i] * self.weight[i]
            sum = sum + self.weight[i]
        action_float = action_b / sum
        action_int = round(action_b / sum)
        action = self.int_to_action(action_int)
        while action not in action_space:
            #print(f'Wrong action: {action}')
            action_int -= 1
            action = self.int_to_action(action_int)
            # action = self.int_to_action(action_a[8])
            # i = i + 1
        self.actions.append(action)
        action_int = self.action_to_int(action)
        List = []
        for i in range(20):
            if action_a[i] == action_int:
                List.append(i)
        self.choice.append(List)
        if action == Action.FOLD:
            self.fold = 1
        #print(self.weight)
        self.previous_stage = stage_a
        # print(self.weight)
        return action
