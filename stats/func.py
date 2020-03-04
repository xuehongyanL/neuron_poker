def select(names):
    def ret(val):
        return val['name'] in names

    return ret


def getVal(record):
    return record['stats']['fold_rate']


def getMaxVal(pair):
    assert len(pair) == 2
    return max(getVal(pair[0]), getVal(pair[1]))


def getMinVal(pair):
    assert len(pair) == 2
    return min(getVal(pair[0]), getVal(pair[1]))


def getAvgVal(pair):
    assert len(pair) == 2
    return (getVal(pair[0]) + getVal(pair[1])) * 0.5


def getDiffVal(pair):
    assert len(pair) == 2
    return -abs(getVal(pair[0]) - getVal(pair[1]))
