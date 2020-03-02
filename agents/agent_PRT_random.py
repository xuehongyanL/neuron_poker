"""Random player"""
import random
import agents.PRT as PRT
from gym_env.env import Action
from tools.montecarlo_python import get_equity

autplay = True  # play automatically if played against keras-rl


class Player:
    """Mandatory class with the player methods"""

    def __init__(self, name='Random_PRT', prt=[], env=None):
        """Initiaization of an agent"""
        self.env = env

        self.equity_alive = 0
        self.actions = []
        self.last_action_in_stage = ''
        self.temp_stack = []
        self.name = name
        self.autoplay = True
        self.realtime = True
        self.end_require = True

        self.plr_num = 1
        self.pos = 0

        self.prt = prt
        self.order = [0]
        self.alive_players = [False]
        self.stage = 0
        self.big_blind = 0
        self.small_blind = 0
        self.ix = 0

    def init_prt(self):  # 初始化PRT
        for i in range(self.plr_num):
            self.prt.append(PRT.PRTNode(name='PRT' + str(i), idx=i))

    def showdown_update(self, opp_info):
        """
        对摊牌阶段进行更新
        Result : { strength = 0,
                   showdown = False,
                   fold = False }
        """
        lhand_cards = opp_info['lhand_cards']
        ltable_cards = opp_info['ltable_cards']
        last_action = opp_info['last_action']
        alive_players = [False if action == Action.FOLD or action == 0
                         else True for action in last_action]
        for i, player in enumerate(alive_players):  # 进行摊牌更新
            if player:
                # print(i, lhand_cards, ltable_cards, alive_players)
                result = PRT.Result()
                result.showdown = True
                result.strength = get_equity(set(lhand_cards[i]), set(ltable_cards),
                                             sum(alive_players), 10)
                PRT.update_prt(self.prt[i], result)

    def rt(self, realtime_info, info):
        """
        使用每位玩家行动结束时的数据进行PRT操作
        """
        opp_info = info['opp_information']

        self.plr_num = opp_info['num_players']

        # print(sum(opp_info['is_newhand']))

        if not bool(self.prt):  # 初始化prt
            self.init_prt()
        elif sum(opp_info['is_newhand']) == self.plr_num:  # 判断是否是新一局
            if opp_info['ltable_cards']:
                self.showdown_update(opp_info)
            for i in range(len(self.prt)):
                self.prt[i] = self.prt[i].back_to_root

        # 查找节点
        current_data = PRT.CurrentData()
        """
        CurrentData = { stage = 0,
                        player = 0,
                        action = None }
        """
        current_data.stage = realtime_info.stage
        current_data.player = realtime_info.position
        current_data.action = realtime_info.action
        alive = opp_info['alive_players']
        for i in range(len(self.prt)):
            if alive[i] and bool(self.prt[i]):
                self.prt[i] = PRT.prt_search(self.prt[i], current_data)

        # 对FOLD玩家进行PRT更新
        if realtime_info.action == Action.FOLD:
            result = PRT.Result()
            result.fold = True
            PRT.update_prt(self.prt[realtime_info.position], result)
            self.prt[realtime_info.position] = self.prt[realtime_info.position].back_to_root

        # print(realtime_info.__dict__)

    def stats_ex(self, node_stats):
        ex_stats = PRT.StatEx()
        ex_stats.fold_rate = (node_stats['fold_count'] + 1) / (node_stats['frequency'] + 3)
        ex_stats.showdown_rate = (node_stats['showdown_count'] + 1) / (node_stats['frequency'] + 3)
        ex_stats.ex_strength = (0.85 * (5 - node_stats['showdown_count'])
                                + node_stats['showdown_count'] * node_stats['avg_strength']) \
            if node_stats['showdown_count'] < 5 \
            else node_stats['avg_strength']
        return ex_stats

    def endgame(self):
        """如果self.end_require为True，将在游戏结束时打印PRT"""
        # path = 'log/PRT.txt'
        # f = open('%s' % path, 'w')
        # f.truncate()
        # f.close()
        # for i in range(self.plr_num):
        #     self.prt[i] = self.prt[i].back_to_root
        #     self.prt[i].dump(write_file=True, path=path)
        for i in range(self.plr_num):
            # data = open("%s" % path, 'a+')
            # print('第%d位玩家数据：' % i, self.stats_ex(self.prt[i].node_stats).__dict__, file=data)
            print(f'第{i}位玩家[{self.env.players[i].name}]数据：{self.stats_ex(self.prt[i].node_stats).__dict__}')

    def action(self, action_space, observation, info):  # pylint: disable=no-self-use
        _ = observation
        _ = info

        opp_info = info['opp_information']
        player_data = info['player_data']
        community_data = info['community_data']

        self.plr_num = opp_info['num_players']
        self.pos = player_data['position']

        # 决策时注意，PRT的生成在游戏第一局第一位玩家行动结束后。
        # 决策时应判断PRT是否存在

        # 决策算法

        this_player_action_space = {Action.FOLD, Action.CHECK, Action.CALL, Action.RAISE_POT, Action.RAISE_HALF_POT,
                                    Action.RAISE_2POT}
        possible_moves = this_player_action_space.intersection(set(action_space))
        action = random.choice(list(possible_moves))
        return action
