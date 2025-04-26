#include "selectFunctions.h"

void insertionSort(std::vector<int>& A, int p, int r) {
    for (int j = p + 1; j <= r; j++) {
        int key = A[j];
        int i = j - 1;
        while (i >= p && (A[i] > key)) {
            countComparisons();
            A[i + 1] = A[i];
            countSwaps();
            i--;
        }
        A[i + 1] = key;
    }
}

int modifiedPartition(std::vector<int>& A, int p, int q, int pivot) {

    int x = A[pivot];       // partition with given pivot

    std::swap(A[pivot], A[q]); // move to the end
    countSwaps();

    int i = p - 1;

    for(int j = p; j < q; j++) {
        countComparisons();
        if((A[j] <= x)) {
            i++;
            std::swap(A[i], A[j]);
            countSwaps();
            if(i != j) {
                if(!bigArray) {printArray(A);}
            }
        }
    }
    std::swap(A[i + 1], A[q]);
    countSwaps();

    if(i+1 != q) {
        if(!bigArray) {printArray(A);}
    }
    return (i+1);
}


int select(std::vector<int>& A, int p, int q, int i) {
    if (p == q) {
        return A[p];
    }

    int n = q - p + 1;
    int howManyFives = n / 5;
    int rest = n % 5;

    std::vector<int> medians;
    std::vector<int> medianIndices;

    for (int j = 0; j < howManyFives; j++) {
        int left = p + j * 5;
        int right = left + 4;
        insertionSort(A, left, right);
        int median = A[left + 2];
        medians.push_back(median);
    }

    if (rest != 0) {
        int left = p + howManyFives * 5;
        int right = q;
        insertionSort(A, left, right);
        int mid = left + (right - left) / 2;
        medians.push_back(A[mid]);
    }

    int medianOfMedians;
    if (medians.size() == 1) {
        medianOfMedians = medians[0];
    } else {
        medianOfMedians = select(medians, 0, medians.size() - 1, medians.size() / 2);
    }

    // Find the index of the medianOfMedians in the original array
    int pivotIndex = p;
    for (int j = p; j <= q; j++) {
        if (A[j] == medianOfMedians) {
            pivotIndex = j;
            break;
        }
    }

    int partitionIndex = modifiedPartition(A, p, q, pivotIndex);
    int k = partitionIndex - p + 1;

    if (i == k) {
        return A[partitionIndex];
    } else if (i < k) {
        return select(A, p, partitionIndex - 1, i);
    } else {
        return select(A, partitionIndex + 1, q, i - k);
    }
}