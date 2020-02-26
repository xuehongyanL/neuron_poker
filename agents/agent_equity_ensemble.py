"""Random player"""

from gym_env.env import Action
import numpy as np

autoplay = True  # play automatically if played against keras-rl


class Player:
    """Mandatory class with the player methods"""

    def __init__(self, name='Ensemble'):
        """Initiaization of an agent"""
        self.equity_alive = 0
        self.name = name
        self.pos = 0 #position of player
        self.actions = [] #sequence of actions in one game
        self.choice = [] #sequence of agents don't follow
        self.weight = [1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1] #weight of 20 agents
        self.tempstack=0 #tempstack num
        self.previous_stage=0
        self.fold=0
        self.autoplay = True

    def oneaction(self, action_space, info, min_call_equity, min_bet_equity, increment1, increment2):
        equity_alive = info['player_data']['equity_to_river_alive']

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
        #print("a")
        if (self.fold == 1):
            #print("b")
            return True
        elif (stage == 0):
            if (self.previous_stage != 0):
                #print("c")
                return True
            elif (self.tempstack < stack):
                #print("d")
                return True
            else:
                #print("e")
                return False
        else:
            #print("f")
            return False
        return False

    def newweight(self,stack):
        if stack>self.tempstack:
            n=0
            for i in self.actions:
                for j in self.choice[n]:
                    self.weight[j]=self.weight[j]+0.2
                n=n+1
        else:
            n=0
            for i in self.actions:
                for j in range(20):
                    if j not in self.choice[n]:
                        self.weight[j]=self.weight[j]+0.2
                n=n+1
        self.fold=0
        self.actions[:]=[]
        self.choice[:]=[]
    def action_to_int(self,action):
        if action==Action.FOLD:
            return 0
        elif action==Action.CHECK:
            return 1
        elif action==Action.CALL:
            return 2
        elif action==Action.RAISE_3BB:
            return 3
        elif action==Action.RAISE_HALF_POT:
            return 3
        elif action==Action.RAISE_POT:
            return 4
        elif action==Action.RAISE_2POT:
            return 5
        else:
            return 6

    def int_to_action(self,value):
        if value==0:
            action=Action.FOLD
        elif value==1:
            action=Action.CHECK
        elif value==2:
            action=Action.CALL
        elif value==3:
            action=Action.RAISE_HALF_POT
        elif value==4:
            action=Action.RAISE_POT
        elif value==5:
            action=Action.RAISE_2POT
        else:
            action=Action.ALL_IN
        return action

    def action(self, action_space, observation, info):  # pylint: disable=no-self-use
        """Mandatory method that calculates the move based on the observation array and the action space."""
        _ = observation
        equity_alive = info['player_data']['equity_to_river_alive']
        position = info['player_data']['position']
        self.pos=position

        stage_data=info['community_data']['stage']
        stage_a = 0
        for i in stage_data:
            if i == 1:
                stage_a = i
        stack_a = 0
        stack_data=info['player_data']['stack']
        for i in stack_data:
            if i == 1:
                stack_a = i

        if self.Isnewstage(stage=stage_a, stack=stack_a):
            #print("new?")
            self.newweight(stack=stack_a)

        action_a=[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
        for i in range(20):
            increment1=(0.1 if (i // 10 == 0) else 0.15)
            increment2=(0.2 if (i // 10 == 0) else 0.25)
            min_call_equity = (i % 10) / 5 * 0.2
            min_bet_equity = min_call_equity+0.1+(i % 2)*0.1
            action_a[i] = self.action_to_int(self.oneaction(action_space, info, min_call_equity, min_bet_equity, increment1, increment2))
        action_b = 0
        sum = 0
        #print(action_a)
        for i in range(20):
            action_b=action_b+action_a[i]*self.weight[i]
            sum = sum+self.weight[i]
        action_float = action_b/sum
        action_int=round(action_b / sum)
        action = self.int_to_action(action_int)
        #print(action)
        while action not in action_space:
            action=self.int_to_action(action_a[8])
            #print(action)
            i = i+1
        #print(action)
        self.actions.append(action)
        action_int=self.action_to_int(action)
        list=[]
        for i in range(20):
            if action_a[i]==action_int:
                list.append(i)
        #print(list)
        self.choice.append(list)
        #print(self.choice)
        if action == Action.FOLD:
            self.fold=1
        # print(self.weight)
        self.previous_stage=stage_a
        #print(self.previous_stage)
        return action



