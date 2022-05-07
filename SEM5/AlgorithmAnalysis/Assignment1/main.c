#include <stdio.h>
#include <stdlib.h>
#include <math.h>

// MACROS
#define MAXNUM 128 // Maximum number of points

// Point + Properties .........................................................
typedef struct Point{
    int x, y; // A Point's Coordinates
} Point;

Point *newPoint(int x_val, int y_val){ // Constructor of Point()
    Point* this;
    this = malloc(sizeof(Point));
    this->x = x_val;
    this->y = y_val;
    return this;
}

void printPoint(Point *this){ // Prints a point in a proper format
    printf("P(%d, %d)\n", this->x, this->y); 
}

// Utilities ..................................................................
float distance_sq(Point *p1, Point *p2){ // Eucledean Distance
    // Calculates the squered distance between 2 points
    // Since d1^2 > d2^2 ==> d1 > d2 we don't need to compare the
    int dx = p2->x - p1->x;
    int dy = p2->y - p1->y;
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
float bruteforce(Point **points, int n, Point *p1, Point *p2){
    float dist;
    float min_dist = distance_sq(points[0], points[1]);

    for (int i = 0; i < n; i++)
        for (int j = i+1; j < n; j++){
            dist = distance_sq(points[i], points[j]);
            if (dist < min_dist){
                min_dist = dist;
                p1 = points[i];
                p2 = points[j];
            }  
        }

    return min_dist;
}


// ClosestPair() ..............................................................
float ClosestPair_stripe(Point **stripe, int n, float d, Point *p1, Point *p2) {
    // minimum distance of the points in a d sized stripe
    qsort(stripe, n, sizeof(Point), compareY); // sort by Y
    float min = d;
    for (int i = 0; i < n; ++i)
        for (int j = i+1; j < n && (stripe[j]->y - stripe[i]->y) < min; ++j)
            if (distance_sq(stripe[i], stripe[j]) < min){
                min = distance_sq(stripe[i], stripe[j]);
                p1 = stripe[i];
                p2 = stripe[j];
            }
    
    return min;
}


float closestPair(Point **points, int n, Point *p1, Point *p2) {
    //find the closest pair in a set of points

     // Sort the points relative to x
    qsort(points, n, sizeof(Point), compareX);

    printf("------------\n");
    printf("Runs on these points:\n");
    for (int i = 0; i < n; i++){
        printPoint(points[i]);
    }
    // Main Algorithm, Divide and Conquer

    // Base of recursion; maximum 6 steps ( O(1) )
    // for n=2 n=3 it's just better to bruteforce
    if (n <= 3) 
        return bruteforce(points, n, p1, p2); 
  
    // middle point 
    int mid = n/2; // the index
    Point *pmid = points[mid]; // the middle point
    
    // Find dl and dr
    Point *pr1, *pr2; // to not overwrite the p1 p2 value on dr (second call)
    float dl = closestPair(points, mid, p1, p2); // min distance of left side
    float dr = closestPair(points+mid, n-mid, pr1, pr2);  // ~ of right side
  
    // d = min(dl, dr)
    float d = dl; // didn't use the min() function because of p1 and p2 
    if(dr<dl){
        d = dr;
        p1 = pr1;
        p2 = pr2;
    }
  
    // Build strip[] for points near the dividor (closer than d)  
    Point **stripe;
    stripe = (Point**) malloc (sizeof(Point*) * n); // DList of n points
    if (stripe == NULL){
        fprintf(stderr, "[!] ERROR : Couldn't Allocate Memory!\n");
        exit(EXIT_FAILURE);
    }

    // Add the close points to the stripe list
    int n_stripe = 0; 
    for (int i = 0; i < n; i++) 
        if (abs(points[i]->x - pmid->x) < d) 
            stripe[n_stripe++] = points[i]; 
  
    // Find the closest points in strip.
    Point *ps1, *ps2;
    float ds = ClosestPair_stripe(stripe, n_stripe, d, ps1, ps2);

    // result = minimum of d and ds, also handle p1, p2
    float dmin = d;
    if (ds<d){
        dmin = ds;
        p1 = ps1;
        p2 = ps2;
    }

    free(stripe); // memory management in a recursive call

    return dmin;
}

// main() .....................................................................
int main(){
    Point *points[MAXNUM];
    // points = (Point*) malloc (sizeof(Point) * MAXNUM); // Dynamic points[MAXSIZE]

    if (*points == NULL){
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
    int ix, iy;
    while (fscanf(fin, "%d%d", &ix , &iy) == 2){
        points[i] = newPoint(ix, iy);
        i++;
    }

    int numOfPoints = i; // save i value

    printf("Num of Points = %d\nPoints:\n", numOfPoints);
    for (i = 0; i < numOfPoints; i++){
        printPoint(points[i]);
    }
    
    
    // The Closest points
    Point *p1=points[0],
          *p2=points[1];

    
    float minDist = sqrt(closestPair(points, numOfPoints, p1, p2));
    
    printf("------------\n");
    printf("Results:\n");
    printf("Distance = %f\n", minDist);

    // #TODO Debug for not changing the values
    printf("The Closest Pair is between:\n");
    printPoint(p1);
    printPoint(p2);

    // free(points);
    
    return 0;
}
