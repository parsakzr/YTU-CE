#include <stdio.h>
#include <stdlib.h>


// MACROS
#define MAXNUM 128 // Maximum number of points

// Point + Properties .........................................................
typedef struct Point{
    int x, y; // A Point's Coordinates
} Point;

Point newPoint(int x_val, int y_val){ // Constructor of Point()
    Point* this;
    this = malloc(sizeof(Point));
    this->x = x_val;
    this->y = y_val;
    return *this;
}

void printPoint(Point this){ // Prints a point in a proper format
    printf("P(%d, %d)\n", this.x, this.y); 
}

// Utilities ..................................................................
float distance_sq(Point p1, Point p2){ // Eucledean Distance
    // Calculates the squered distance between 2 points
    // Since d1^2 > d2^2 ==> d1 > d2 we don't need to compare the
    int dx = p2.x - p1.x;
    int dy = p2.y - p1.y;
    return dx*dx + dy*dy;
}

int compareX (const void * a, const void * b){ // qsort() by x
    // Compare x coordinates ( Needed for qsort() )
    Point *p1 = (Point *)a;
    Point *p2 = (Point *)b;
    return ( p1->x - p2->x );
}

int compareY (const void * a, const void * b){ // qsort() by y
    // Compare y coordinates ( Needed for qsort() )
    Point *p1 = (Point *)a;
    Point *p2 = (Point *)b;
    return ( p1->y - p2->y );
}

float min(float f1, float f2){
    if (f1 > f2)
        return f2;
    return f1;
}

// BruteForce Approach  .......................................................
// Used when n<=3
float bruteforce(Point *points, int n, Point *p1, Point *p2){
    float dist,
          min_dist = distance_sq(points[0], points[1]);
    for (int i = 0; i < n; i++)
        for (int j = i+1; j < n; j++){
            dist = distance_sq(points[i], points[j]);
            if (dist < min_dist)
                min_dist = dist;   
        }

    return min_dist;
}


// ClosestPair() ..............................................................
float ClosestPair_stripe(Point *stripe, int n, float d, Point *p1, Point *p2) {
    // minimum distance of the points in a d sized stripe
    qsort(stripe, n, sizeof(Point), compareY); // sort by Y
    float min = d;
    for (int i = 0; i < n; ++i)
        for (int j = i+1; j < n && (stripe[j].y - stripe[i].y) < min; ++j)
            if (distance_sq(stripe[i],stripe[j]) < min){
                min = distance_sq(stripe[i], stripe[j]);
                p1 = &stripe[i];
                p2 = &stripe[j];
            }
    
    return min;
}


float closestPair(Point points[], int n, Point *p1, Point *p2) {
    //find the closest pair in a set of points

     // Sort the points relative to x
    qsort(points, n, sizeof(Point), compareX);

    // Main Algorithm, Divide and Conquer

    // Base of recursion; maximum 6 steps ( O(1) )
    // for n=2 n=3 it's just better to bruteforce
    if (n <= 3) 
        return bruteforce(points, n, p1, p2); 
  
    // middle point 
    int mid = n/2; // the index
    Point pmid = points[mid]; // the middle point
    
    // Find dl and dr
    float dl = closestPair(points, mid, p1, p2); // min distance of left side
    float dr = closestPair(points + mid, n-mid, p1, p2);  // ~ of right side
  
    float d = min(dl, dr); // best of dl and dr
  
    // Build strip[] for points near the dividor (closer than d)  
    Point *strip;
    strip = (Point*) malloc (sizeof(Point) * n); // DList of n points
    if (points == NULL){
        fprintf(stderr, "[!] ERROR : Couldn't Allocate Memory!\n");
        exit(EXIT_FAILURE);
    }

    // Add the close points to the strip list
    int n_stripe = 0; 
    for (int i = 0; i < n; i++) 
        if (abs(points[i].x - pmid.x) < d) 
            strip[n_stripe++] = points[i]; 
  
    // Find the closest points in strip.  Return the minimum of d and closest
    float dmin = min(d, ClosestPair_stripe(strip, n_stripe, d, p1, p2));

    free(strip); // memory management in a recursive call

    return dmin;
}

// main() .....................................................................
int main(){
    Point *points;
    points = (Point*) malloc (sizeof(Point) * MAXNUM); // Dynamic points[MAXSIZE]

    if (points == NULL){
        fprintf(stderr, "[!] ERROR : Couldn't Allocate Memory!\n");
        exit(EXIT_FAILURE);
    }
    
    char* filename = "sample.txt";

    FILE *fin = fopen(filename, "r");
    if (fin == NULL){
        fprintf(stderr, "[!] ERROR : Couldn't read the file '%s'!\n", filename);
        exit(EXIT_FAILURE);
    }

    int i=0;
    while (fscanf(fin, "%d%d", &points[i].x , &points[i].y) == 2)
        i++;

    int numOfPoints = i;

    printf("Num of Points = %d\nPoints:\n", numOfPoints);
    for (i = 0; i < numOfPoints; i++){
        printPoint(points[i]);
    }
    

    Point *p1, *p2; // The Close pair
    printf("Distance^2 = %f\n", closestPair(points, numOfPoints, p1, p2));
    printPoint(*p1);
    printPoint(*p2);


    free(points);
    
    return 0;
}
