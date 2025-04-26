#ifndef SELECTION_SORT_H
#define SELECTION_SORT_H

#include <vector>

// Prototypy funkcji
void insertionSort(std::vector<int>& A, int p, int r);
int modifiedPartition(std::vector<int>& A, int p, int q, int pivot);
int select(std::vector<int>& A, int p, int q, int i);

#endif // SELECTION_SORT_H
