"""
Modified by Xue Hongyan
"""
from gym_env.env import Action
import numpy as np

autoplay = True  # play automatically if played against keras-rl

# 弱学习器类


class Learner:
    def __init__(self, params):  # 用一组固定参数初始化
        self.params = params

    def decision(self, equity_alive, action_space):  # 决策函数
        min_call_equity = self.params['min_call_equity']
        min_bet_equity = self.params['min_bet_equity']
        increment1 = self.params['increment1']
        increment2 = self.params['increment2']

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

    @staticmethod
    def reduce(action_a, weight):  # 规约函数 将多个决策值根据权重规约成一个最终结果
        action_b = 0
        sum = 0
        for i in range(20):
            action_b += action_a[i] * weight[i]
            sum += weight[i]
        action_float = action_b / sum
        action_int = round(action_float)
        action = Action(action_int)

        return action


class Player:
    def __init__(self, name='EnsembleEX'):
        self.name = name
        self.autoplay = True
        self.initState()
        self.initWeight()
        self.initLearner()

    def initState(self):  # 状态的初始化 状态记录的是还未被学习的信息
        self.state = {
            'choice': [],
            'temp_stack': 2.50,
            'previous_stage': 0,
            'fold': 1,
        }

    def initWeight(self):  # 权重的初始化 权重记录的是已经被学习的信息
        self.weight = [1.0 for _ in range(20)]

    def initLearner(self):  # 弱学习器的初始化 生成一组参数并用参数来实例化学习器
        paramList = [{
            'increment1': (0.1 if (i // 10 == 0) else 0.15),
            'increment2': (0.2 if (i // 10 == 0) else 0.25),
            'min_call_equity': (i % 10) / 5 * 0.2,
            'min_bet_equity': (i % 10) / 5 * 0.2 + 0.1 + (i % 2) * 0.1,
        } for i in range(20)]
        self.learners = [Learner(params) for params in paramList]

    def isNewHand(self, newState):  # 用来判断是否是新的一手牌
        stage = newState['current_stage']
        stack = newState['current_stack']

        if (self.state['fold'] == 1):
            return True
        elif (stage == 0):
            if (self.state['previous_stage'] != 0):
                return True
            elif (self.state['temp_stack'] < stack):
                return True
            else:
                return False
        else:
            return False
        return False

    def updateWeight(self, newState):  # 更新权重 从[状态]中学习并更新到[权重]
        stack = newState['current_stack']

        if stack > self.state['temp_stack']:
            for choice in self.state['choice']:
                for j in range(20):
                    if j in choice:
                        self.weight[j] += 0.2
                    else:
                        self.weight[j] -= 0

        else:
            for choice in self.state['choice']:
                for j in range(20):
                    if j in choice:
                        self.weight[j] -= 0
                    else:
                        self.weight[j] += 0.2

        self.state['fold'] = 0
        self.state['choice'][:] = []
        self.state['temp_stack'] = stack

    def updateState(self, newState):  # 更新状态 每次决策后更新状态
        self.state['choice'].append(newState['newChoices'])
        if newState['fold']:
            self.state['fold'] = 1
        self.state['previous_stage'] = newState['current_stage']

    def action(self, action_space, observation, info):  # pylint: disable=no-self-use
        _ = observation

        # 构建新状态
        current_stage = info['community_data']['stage'].index(1)
        assert 0 <= current_stage < 4
        position = info['player_data']['position']
        current_stack = info['player_data']['stack'][position]
        newState = {
            'current_stage': current_stage,
            'current_stack': current_stack,
        }

        # 如果是新的一手牌那么更新权重
        if self.isNewHand(newState):
            self.updateWeight(newState)

        # 决策
        equity_alive = info['player_data']['equity_to_river_alive']
        actions = [learner.decision(
            equity_alive, action_space).value for learner in self.learners]
        action = Learner.reduce(actions, self.weight)
        action_int = action.value
        while action not in action_space:
            action = sorted(list(action_space),
                            key=lambda x: abs(x.value-action_int))[0]

        # 更新状态
        newState['newChoices'] = [
            i for i in range(20) if actions[i] == action_int]
        newState['fold'] = (action == Action.FOLD)
        self.updateState(newState)

        return action
