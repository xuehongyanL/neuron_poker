#include <cstdlib>
#include "observation.h"
using namespace std;

double eval(Observation*);
Action decision(double,Observation*);

extern "C" {
    int interface(Observation* obs){
        double prob1v1=eval(obs);
        Action ret=decision(prob1v1,obs);
        return (int)ret;
    }
}
