// functions.h
#ifndef FUNCTIONS_H
#define FUNCTIONS_H

#include <vector>
extern int comparisons;  
extern int swaps;         
extern bool bigArray;     


void countComparisons();
void countSwaps();

void printArray(std::vector<int>& arr);
bool isSorted(const std::vector<int>& arr);

#endif