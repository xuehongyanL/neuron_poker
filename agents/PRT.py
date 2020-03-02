"""
Pattern Recognition Tree which Maintains of a Set of Action Sequences
"""
from enum import Enum
import random
from gym_env.env import Action, Stage


class PRTNode(object):
    def __init__(self, name, idx=0, stage=0, action=None, agent=2):
        self.name = name
        self.parent = None
        self.child = {}
        self.depth = 0
        self.agent = agent
        self.action = action

        self.stage = stage
        self.idx = idx
        self.node_stats = {'frequency': 0,
                           'avg_strength': 0,
                           'showdown_count': 0,
                           'fold_count': 0}

    def __repr__(self):
        return 'PRT Node(%s)' % self.name

    def __contains__(self, item):
        return item in self.child

    def __len__(self):
        """return number of children node"""
        return len(self.child)

    def __bool__(self):
        """always return True for exist node"""
        return True

    @property
    def path(self):
        """return path string (from root to current node)"""
        if self.parent:
            return '%s %s' % (self.parent.path.strip(), self.name)
        else:
            return self.name

    """child"""

    def get_child(self, name, defval=None):
        """get a child node of current node"""
        return self.child.get(name, defval)

    def add_child(self, name, obj=None, stage=0, action=None, agent=0):
        """add a child node tu current node"""
        if obj and not isinstance(obj, PRTNode):
            raise ValueError('PRT_Node only add another PRT_Node obj as child')
        if obj is None:
            obj = PRTNode(name, stage=stage, action=action, agent=agent)
        obj.parent = self
        obj.depth = self.depth + 1
        obj.idx = self.idx
        self.child[name] = obj
        return obj

    def del_child(self, name):
        if name in self.child:
            del self.child[name]

    def find_child(self, path, creat=False):
        """find child node by path/name, return None if not found"""
        # convert path to a list if input is a string
        path = path if isinstance(path, list) else path.split()
        cur = self
        for sub in path:
            # search
            obj = cur.get_child(sub)
            if obj is None and creat:
                # creat new node if need
                obj = cur.add_child(sub)
            # check if search done
            if obj is None:
                break
            cur = obj
        return obj

    def items(self):
        return self.child.items()

    def dump(self, indent=0, write_file=False, path='PRT.txt'):
        """dump tree to string"""
        tab = '    ' * (indent - 1) + '|-' if indent > 0 else ''
        if write_file:
            data = open("%s" % path, 'a+')
            print('%s%s%s' % (tab, self.name, str(self.node_stats)), file=data)
            for name, obj in self.items():
                obj.dump(indent + 1, write_file=write_file, path=path)
        else:
            print('%s%s%s' % (tab, self.name, str(self.node_stats)))
            for name, obj in self.items():
                obj.dump(indent + 1)

    @property
    def back_to_root(self):
        if self.parent:
            return self.parent.back_to_root
        else:
            return self

    """node stats"""

    def frequency_stat(self):
        self.node_stats['frequency'] += 1

    def showdown_stat(self, strength):
        sd = self.node_stats['showdown_count']
        avg_str = self.node_stats['avg_strength']
        avg_str = (avg_str * sd + strength) / (sd + 1)
        sd += 1
        self.node_stats['showdown_count'] = sd
        self.node_stats['avg_strength'] = avg_str

    def fold_stat(self):
        self.node_stats['fold_count'] += 1

    def get_stats(self):
        return self.node_stats


class CurrentData:
    def __init__(self):
        self.stage = 0
        self.player = 0
        self.action = None


class Result:
    def __init__(self):
        self.strength = 0
        self.showdown = False
        self.fold = False

    def reset(self):
        self.strength = 0
        self.showdown = False
        self.fold = False


class StatEx:
    def __init__(self):
        self.fold_rate = 0
        self.showdown_rate = 0
        self.ex_strength = 0


'''class Action(Enum):
    """Allowed actions"""

    FOLD = 0
    CHECK = 1
    CALL = 2
    RAISE_3BB = 3
    RAISE_HALF_POT = 3
    RAISE_POT = 4
    RAISE_2POT = 5
    ALL_IN = 6
    SMALL_BLIND = 7
    BIG_BLIND = 8
    

class Stage(Enum):
    """Allowed actions"""

    PREFLOP = 0
    FLOP = 1
    TURN = 2
    RIVER = 3
    END_HIDDEN = 4
    SHOWDOWN = 5
'''


def prt_search(current_node, current_data):
    sim_player = current_data.player == current_node.idx  # 简化为两个玩家
    n_next_node = \
        str(int(sim_player)) + '-' + str(current_data.action.name) + '-' + str(Stage(current_data.stage).name)
    # 命名节点为简化玩家名(1为此PRT对应的对手，0为其他玩家)+行动+阶段
    if current_node.parent:
        is_same_player = sim_player == current_node.agent
        is_same_stage = current_node.stage == current_data.stage

        if is_same_player and is_same_stage and current_node.action:  # 将其他玩家同一stage的行为合并
            if current_data.action.value > current_node.action.value:  # 取较高行动值
                current_node = current_node.parent  # 返回父节点重新搜索
            else:
                return current_node

    if n_next_node not in current_node.child:
        current_node.add_child(name=n_next_node, stage=current_data.stage,
                               action=current_data.action, agent=int(sim_player))

    current_node = current_node.get_child(n_next_node)
    return current_node


def update_prt(current_node, result):
    if result.showdown == result.fold:
        raise ValueError('Showdown and Fold cannot be the same! ')
    else:
        current_node.frequency_stat()
        if result.showdown:
            current_node.showdown_stat(result.strength)
        else:
            current_node.fold_stat()

        if current_node.parent:
            current_node = update_prt(current_node.parent, result)

    return current_node


if __name__ == '__main__':
    # local test
    print('test prt')
    PRT = []
    current_data = CurrentData()
    for player in range(6):
        PRT.append(PRTNode(name='Opp' + str(player), idx=player))
    for _ in range(6):
        current_node = PRT
        for Test_stage in range(4):
            for player in range(6):
                R_action = random.choice(list(Action)[:7])
                current_data.stage = Test_stage
                current_data.player = player
                current_data.action = R_action
                for i in range(6):
                    current_node[i] = prt_search(current_node[i], current_data)
            for i in range(6):
                PRT[i] = PRT[i].back_to_root

    for i in range(len(PRT)):
        PRT[i] = PRT[i].back_to_root
        PRT[i].dump()
