#include "observation.h"
#define max(x,y) ((x)>(y))?(x):(y)

int amount(Action act,Observation* obs){
    int minAmount=0;
    for(int i=0;i<obs->numPlayers;i++){
        minAmount=max(minAmount,obs->stages[obs->currStage].contribution[i]);
    }
    if(act==CALL){
        return minAmount;
    }else if(act==RAISE_3BB){
        return minAmount+3*obs->bigBlind;
    }else if(act==RAISE_POT){
        return obs->communityPot+obs->roundPot;
    }else if(act==RAISE_2POT){
        return 2*(obs->communityPot+obs->roundPot);
    }else if(act==ALL_IN){
        return obs->stack[obs->position];
    }else{
        return 0;
    }
}

Action decision(double prob1v1,Observation* obs){
    double prob=1.0;
    int oppos=0;
    for(int i=0;i<obs->numPlayers;i++){
        if(obs->stages[obs->currStage].folds[i]!=0) oppos++;
    }
    for(int i=0;i<oppos;i++) prob*=prob1v1;
    int pool=obs->communityPot+obs->roundPot;

    Action finalAction=(obs->legalMoves[CHECK])?CHECK:FOLD;
    double finalExpect=0.0;
    for(int choice=(int)CALL;choice<=(int)ALL_IN;choice++){
        if(obs->legalMoves[choice]==0) continue;
        double expect=prob*pool+(1.0-prob)*amount((Action)choice,obs);;
        if(expect>finalExpect){
            finalAction=(Action)choice;
            finalExpect=expect;
        }
    }
    return finalAction;
}
