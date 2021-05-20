#include <stdio.h>

/*
# Algorithm Analysis

    Best Case  :    Time Complexity  : O(n*m)
                    Space Complexity : O(k)

    Worst Case :    Time Complexity  : O(n*m)
                    Space Complexity : O(k)

    Because We need to check every data, so the Worst case and Best case are the same.
    But if we implemented a vector or other data structure that we append data to it,
    Space Complexity would be different. 
*/

int main(){
    int n, m, k; // N*M, for colors between 1 - k-1
    int map[20][20]; // input
    int hist_raw[256] = {0}; // to store the i'th color frequency in hist_full[i]
    int hist[86][2]; // max 256/3 = 85 different colors
    int indx = 0;

    printf("N, M :  ");
    scanf("%d%d", &n, &m);
    
    printf("K :  ");
    scanf("%d", &k);

    printf("Matrix:\n");
    for (int i = 0; i < n; i++)
        for (int j = 0; j < m; j++)
            scanf("%d", &map[i][j]);
    
    for (int i = 0; i < n; i++)
        for (int j = 0; j < m; j++)
            hist_raw[map[i][j]]++;


    // process the raw array to a smaller array only containing used colors
    for (int i = 0; i < k; i++)
        if (hist_raw[i] > 0){
            hist[indx][0] = i;
            hist[indx][1] = hist_raw[i];
            indx++;
        }

    printf("Histogram:  [ Color, Frequency ]\n"); // Output
    for (int i = 0; i < indx; i++)
        printf("[ %d, %d ]\n", hist[i][0], hist[i][1]);


    return 0;
}