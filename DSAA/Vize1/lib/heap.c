#include <stdio.h>

void maxHeapify(int arr[], int i, int N){
    int left = 2*i,
        right = 2*i+1;
    int largest;
    
    if(left <= N && arr[left]>arr[i])
        largest = left;
    else
        largest = i;
    if (right <= N && arr[right]>arr[largest])
        largest = right;
    
    if(largest != i){
        int temp = arr[i];
        arr[i] = arr[largest];
        arr[largest] = temp;
        maxHeapify(arr, largest, N);
    }
}

void build_maxHeap(int arr[], int N){
    int i;
    for(i=N/2; i>= 1; i--)
        maxHeapify(arr, i, N);
}