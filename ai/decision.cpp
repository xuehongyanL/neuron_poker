#include <cmath>
#include "observation.h"
#define max(x,y) ((x)>(y))?(x):(y)

int alive(int i,Observation* obs){
    if(obs->stages[obs->currStage].folds[i]==0) return 1;
    else if(obs->stages[obs->currStage].calls[i]) return 1;
    else if(obs->stages[obs->currStage].raises[i]) return 1;
    else if(obs->stack[i]>0) return 1;
    else return 0;
}

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

double tightFactor(Observation* obs){
    double ret=1.0;
    for(int i=0;i<obs->numPlayers;i++){
        if(obs->stages[obs->currStage].contribution[i]>0 && obs->stack[i]==0){
            if(obs->stack[obs->position]>1500){
                ret*=0.5;
            }else if(obs->stack[obs->position]>750){
                ret*=0.75;
            }else if(obs->stack[obs->position]>450){
                ret*=0.85;
            }
            if(obs->stack[obs->position]<150){
                ret*=2;
            }else if(obs->stack[obs->position]<300){
                ret*=1.5;
            }else if(obs->stack[obs->position]<450){
                ret*=1.25;
            }
        }
    }
    /*int stackSum=0;
    int aliveSum=0;
    for(int i=0;i<obs->numPlayers;i++){
        stackSum+=obs->stack[i];
        if(obs->stages[obs->currStage].folds[i]==0 && obs->stack[i]>0) aliveSum++;
    }
    int stackAvg=stackSum/aliveSum;
    ret*=log((double)stackAvg)/log((double)(obs->stack[obs->position]));*/
    return ret;
}

Action decision(double prob1v1,Observation* obs){
    double prob=prob1v1;
    int oppos=0;
    for(int i=0;i<obs->numPlayers;i++){
        if(obs->stages[obs->currStage].folds[i]==0 && alive(i,obs)) oppos++;
    }
    for(int i=0;i<oppos/2;i++) prob*=prob1v1;
    prob*=tightFactor(obs);
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
