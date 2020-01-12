$cc=g++

windows: interface.cpp eval.cpp decision.cpp
	g++ -o ./ai.dll -O3 -shared -fPIC ./interface.cpp ./eval.cpp ./decision.cpp

linux: interface.cpp eval.cpp decision.cpp
	g++ -o ./ai.so -O3 -shared -fPIC ./interface.cpp ./eval.cpp ./decision.cpp
