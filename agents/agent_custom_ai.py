"""
Created by Xue Hongyan
Our Customom Agent
"""
import platform
import random
from ctypes import *
from typing import Any, List, Optional, Tuple

Attribute = Tuple[str, Any]
IntArr = Any
StageArr = Any
CardArr = Any
autplay = True


def intArr(arr: List[int]) -> IntArr:
    for i, elem in enumerate(arr):
        arr[i] = int(arr[i])
    return (c_int * len(arr))(*arr)


def extendArr(arr: list, length: int, default: Any) -> None:
    while len(arr) < length:
        arr.append(default)


def makeCard(notation: Optional[str]):
    notationStr: str = 'AS' if notation is None else notation
    suit: int = {'S': 0, 'H': 1, 'D': 2, 'C': 3}[notationStr[1]]
    rank: int = {'A': 12, '2': 11, '3': 10, '4': 9, '5': 8,
                 '6': 7, '7': 6, '8': 5, '9': 4, 'T': 3,
                 'J': 2, 'Q': 1, 'K': 0}[notationStr[0]]
    return suit + 4 * rank


class Stage(Structure):
    _fields_: List[Attribute] = [
        ('calls', c_int * 10),
        ('raises', c_int * 10),
        ('folds', c_int * 10),
        ('contribution', c_int * 10),
    ]

    def __init__(self, stage: dict, bigBlind100: int):
        super().__init__()
        extendArr(stage['calls'], 10, 0)
        self.calls = intArr(stage['calls'])
        extendArr(stage['raises'], 10, 0)
        self.raises = intArr(stage['raises'])
        extendArr(stage['folds'], 10, 0)
        self.folds = intArr(stage['folds'])
        for i, elem in enumerate(stage['contribution']):
            stage['contribution'][i] *= bigBlind100
        extendArr(stage['contribution'], 10, 0)
        self.contribution = intArr(stage['contribution'])

    @staticmethod
    def stageArr(arr: list) -> StageArr:
        return (Stage * len(arr))(*arr)


class Observation(Structure):
    _fields_: List[Attribute] = [
        ('numPlayers', c_int),
        ('position', c_int),
        ('stack', c_int * 10),
        ('currStage', c_int),
        ('communityPot', c_int),
        ('roundPot', c_int),
        ('bigBlind', c_int),
        ('smallBlind', c_int),
        ('legalMoves', c_int * 9),
        ('stages', Stage * 4),
        ('nameTableCards', c_int),
        ('tableCards', c_int * 5),
        ('handCards', c_int * 2),
    ]

    def __init__(self, obs: dict):
        super().__init__()
        bigBlind100: int = 100 * obs['community_data']['big_blind']

        for i, elem in enumerate(obs['player_data']['stack']):
            obs['player_data']['stack'][i] *= bigBlind100
        extendArr(obs['player_data']['stack'], 10, 0)

        self.numPlayers: int = obs['numPlayers']
        self.position: int = obs['player_data']['position']
        self.stack: IntArr = intArr(obs['player_data']['stack'])
        self.currStage: int = obs['community_data']['stage']
        self.communityPot: int = int(bigBlind100 * obs['community_data']['community_pot'])
        self.roundPot: int = int(bigBlind100 * obs['community_data']['current_round_pot'])
        self.bigBlind: int = obs['community_data']['big_blind']
        self.smallBlind: int = obs['community_data']['small_blind']
        self.legalMoves: IntArr = intArr(obs['community_data']['legal_moves'])
        self.stages: StageArr = Stage.stageArr([Stage(stg, bigBlind100) for stg in obs['stage_data'][:4]])
        self.numTableCards: int = obs['numTableCards']
        self.tableCards: CardArr = intArr([makeCard(card) for card in obs['tableCards']])
        self.handCards: CardArr = intArr([makeCard(card) for card in obs['handCards']])


class Player:
    def __init__(self, env, name=None):
        self.env = env
        self.name = f'Custom[{random.randint(10000, 99999)}]' if name is None else name
        self.autoplay = True
        if platform.system() == 'Windows':
            self.lib = cdll.LoadLibrary('./ai/ai.dll')
        elif platform.system() == 'Linux':
            self.lib = cdll.LoadLibrary('./ai/ai.so')

    def action(self, action_space, observation, info):
        _ = observation
        _ = action_space

        info['numPlayers'] = self.env.num_of_players
        info['community_data']['stage'] = info['community_data']['stage'].index(1)
        info['numTableCards'] = len(self.env.table_cards[:])
        info['tableCards'] = self.env.table_cards[:]
        extendArr(info['tableCards'], 5, None)
        info['handCards'] = self.env.players[info['player_data']['position']].cards[:]
        for i in range(4):
            if i == info['community_data']['stage']:
                info['stage_data'][i]['folds'] = self.env.player_cycle.folder[:]
            else:
                info['stage_data'][i]['folds'] = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]

        self.lib.interface.argtypes = [POINTER(Observation)]
        self.lib.interface.restype = c_int
        action: int = self.lib.interface(Observation(info))

        return action
