#include <stdio.h>
#include <iostream>
#include <algorithm>
#include "./SKPokerEval/FiveEval.h"
using namespace std;

int main(){
    dfs(52,5);
    cout<<cnt<<endl;
    cout<<maxVal<<' '<<minVal<<endl;
    sort(seq,seq+2598960);
    int div=1000;
    for(int i=0;i<div;i++){
        printf("%d/%d: %d\n",i,div,seq[2598960/div*i]);
    }
    return 0;
}
