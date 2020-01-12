#ifndef OBSERVATION_H
#define OBSERVATION_H

typedef enum {
    FOLD=0,
    CHECK=1,
    CALL=2,
    RAISE_3BB=3,
    RAISE_POT=4,
    RAISE_2POT=5,
    ALL_IN=6,
    SMALL_BLIND=7,
    BIG_BLIND=8
} Action;

struct Card {
    int suit;
    int rank;
};

struct Stage {
    int calls[10];
    int raises[10];
    int folds[10];
    int contribution[10];
};

struct Observation {
    int numPlayers;
    int position;
    int stack[10];
    int currStage;
    int communityPot;
    int roundPot;
    int bigBlind;
    int smallBlind;
    int legalMoves[9];
    Stage stages[4];
    int numTableCards;
    int tableCards[5];
    int handCards[2];
};

#endif
