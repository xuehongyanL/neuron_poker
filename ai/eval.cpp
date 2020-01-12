#include <bits/stdc++.h>
#include "observation.h"
#include "./SKPokerEval/SevenEval.h"
using namespace std;

#define MAX_AI_SAMPLE 2598961
#define MAX_OPPO_SAMPLE 1000
int aiCnt;
int aiSample[MAX_AI_SAMPLE];
int oppoCnt;
int oppoSample[MAX_OPPO_SAMPLE];

void aiDfs(int n,int m,int mapping[52],int numCards,int cards[7]){
    if(m<=0) return;
    int a[53];
    for(int i=n;i>=1;i--){
        a[m]=i;
        if(m>1) aiDfs(i-1,m-1,mapping,numCards,cards);
        else{
            for(int j=0;j+numCards<7;j++){
                cards[j+numCards]=mapping[a[j+1]-1];
            }
            aiSample[aiCnt]=SevenEval::GetRank(cards[0],cards[1],cards[2],cards[3],cards[4],cards[5],cards[6]);
            aiCnt++;
        }
    }
}

int aiEval(int numCards,int cards[7]){
    int mapping[52];
    memset(mapping,0,sizeof(mapping));
    for(int i=0;i<numCards;i++) mapping[cards[i]]=-1;
    for(int i=0,j=0;i<52-numCards;i++,j++){
        while(mapping[j]==-1) j++;
        mapping[i]=j;
    }
    aiCnt=0;
    aiDfs(52-numCards,7-numCards,mapping,numCards,cards);
    return aiCnt;
}

int oppoEval(int numCards,int cards[7],int sampleSize){
    int mapping[52];
    memset(mapping,0,sizeof(mapping));
    for(int i=0;i<numCards;i++) mapping[cards[i]]=1;
    oppoCnt=0;
    for(int epoch=0;epoch<sampleSize;epoch++){
        int currNum=numCards;
        int choice=rand()%52;
        while(currNum<7){
            while(mapping[choice]) choice=rand()%52;
            mapping[choice]=1;
            cards[currNum++]=choice;
        }
        oppoSample[epoch]=SevenEval::GetRank(cards[0],cards[1],cards[2],cards[3],cards[4],cards[5],cards[6]);
        oppoCnt++;
        while(currNum>numCards){
            currNum--;
            mapping[cards[currNum]]=0;
        }
    }
    sort(oppoSample,oppoSample+oppoCnt);
    return oppoCnt;
}

double eval(Observation* obs){
    srand(time(NULL));

    int numPublicCards=obs->numTableCards;
    int publicCards[7];
    int numPrivateCards=numPublicCards+2;
    int privateCards[7];
    for(int i=0;i<obs->numTableCards;i++){
        publicCards[i]=obs->tableCards[i];
        privateCards[i]=obs->tableCards[i];
    }
    return 0.0;
    privateCards[numPrivateCards-2]=obs->handCards[0];
    privateCards[numPrivateCards-1]=obs->handCards[1];
    aiEval(numPrivateCards,privateCards);
    oppoEval(numPublicCards,publicCards,MAX_OPPO_SAMPLE);

    long long accu=0;
    for(int i=0;i<aiCnt;i++){
        accu+=(long long)(lower_bound(oppoSample,oppoSample+oppoCnt,aiSample[i])-oppoSample);
    }

    return 1.0*accu/aiCnt/oppoCnt;
}
