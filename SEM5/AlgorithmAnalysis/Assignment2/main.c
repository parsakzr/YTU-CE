#include <stdio.h>

#define MAXNUM 32

typedef struct Reklam {
    int id; // Keep the original index before sorting
    int start,  // start time
        end,    // End time = Start + Duration
        value;  // 
} Reklam;

void setReklam(Reklam* reklam, int id, int start, int duration, int value){
    // Updates the contents of a given ad;
    reklam->id = id;
    reklam->start = start;
    reklam->end = start + duration;
    reklam->value = value;
}

void printReklam(Reklam reklam){ // prints the contents of an ad

    printf("ID: %d | START: %d | END: %d | VALUE: %d\n",
            reklam.id, reklam.start, reklam.end, reklam.value);
}
// ....................................
int compareEnd(const void* ad1, const void* ad2){
// Utility: compareEnd() used by qsort()
    const Reklam *_ad1 = ad1, *_ad2 = ad2;
    int end1 = _ad1->end,
        end2 = _ad2->end;
    return (end1 > end2) - (end1 < end2); // debugged->Extreme numbers on int
}

void maxProfit(Reklam ads[], int n){
    int profit[MAXNUM]; // data from previous results, used for DP
    profit[0] = 0;

    int path[MAXNUM]; // To save the selected ads
    int k=0; // the counter

    int temp, i=1; // i as the main index.
    while (i < n) {
        int j=i-1; // j = index of the last ad without collision
        while (j > 0 && ads[j].end > ads[i].start) {
            j--;
        }
        
        temp = profit[j] + ads[i].value;
        if ( temp > profit[i-1]){ // -> Ad[i] selected
            // #TODO: it adds but doesn't replace
            profit[i] = temp;
            path[k++] = ads[i].id; // Add to the path
        }
        else // -> Ad[i] Not Selected
            profit[i] = profit[i-1];

        i++;
    }
    
    printf("Profits: \n");
    for (int i = 0; i < n; i++) {
        printf("%d ", profit[i]);
    }

    printf("\n----------------\n");
    printf("Max Profit = %d", profit[n-1]);

    printf("\nUsing the ads with id:\n");
    for (int i = 0; i < k; i++) {
        printf("%d ", path[i]);
    }
    
    return;
}

int main(){
    Reklam ads[MAXNUM];
    int n, start, duration, value;
    printf("Enter the number of advertisements: ");
    scanf("%d", &n);
    
    printf("Enter the Start time, Duration and Value of each ad:\n");
    for (int i = 0; i < n; i++) {
        scanf ("%d%d%d", &start, &duration, &value);
        setReklam(&ads[i], i+1, start, duration, value);
    }
    
    // Print The Original Information
    printf("| ID | Start | End | Value |\n");
    for (int i = 0; i < n; i++) {
        printReklam(ads[i]);
    }

    // Sort by the End time, using standard qsort()
    qsort(ads, n, sizeof(Reklam), compareEnd);

    printf("\nAfter sorting:\n");
    printf("| ID | Start | End | Value |\n");
    for (int i = 0; i < n; i++) {
        printReklam(ads[i]);
    }
    
    // Call the Algorithm
    maxProfit(ads, n);

    return 0;
}
