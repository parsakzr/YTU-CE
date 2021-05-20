#include <stdio.h>
#include <stdlib.h>
#include <math.h>
#include <time.h>
#include <float.h>
#include <SDL2/SDL.h>

// Point + Properties ....BEGIN................................................
typedef struct Point{ // Struct Point : Contains (int)coordinates 
    int x, y;
} Point; // typedef (struct Point) ---> Point

Point newPoint(int x_val, int y_val){ // SET : Constructor of Point()
    Point* this;
    this = malloc(sizeof(Point));
    this->x = x_val;
    this->y = y_val;
    return *this;
}

void printPoint(Point this){ // GET : Prints a point in proper format
    printf("( %d, %d )\n", this.x, this.y); 
}

// Utilities ..................................................................
float distance(Point p1, Point p2){ // Eucledean Distance
    // Calculates the distance between 2 points
    int dx = p2.x - p1.x;
    int dy = p2.y - p1.y;
    return sqrt(dx*dx + dy*dy);
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

float bruteforce(Point points[], int n){
    float dist, min_dist = FLT_MAX; //  FLT_MAX ~ infinity
    for (int i = 0; i < n; i++)
        for (int j = i+1; j < n; j++){
            dist = distance(points[i], points[j]);
            if (dist < min_dist)
                min_dist = dist;   
        }

    return min_dist;
}

float min(float f1, float f2){
    if (f1 > f2)
        return f2;
    return f1;
}


// ClosestPair() ..............................................................
float ClosestPair_stripe(Point strip[], int n, float d) {
    // minimum distance of the points in a d sized stripe
    qsort(strip, n, sizeof(Point), compareY);
    float min = d;
    for (int i = 0; i < n; ++i)
        for (int j = i+1; j < n && (strip[j].y - strip[i].y) < min; ++j)
            if (distance(strip[i],strip[j]) < min)
                min = distance(strip[i], strip[j]);
    return min;
}

float closestPair_DC(Point points[], int n) { 
    // Base of recursion; maximum 6 steps ( O(1) )
    // for n=2 n=3 it's just better to bruteforce
    if (n <= 3) 
        return bruteforce(points, n); 
  
    // middle point 
    int mid = n/2; 
    Point pmid = points[mid]; 
    
    // Find dl and dr
    float dl = closestPair_DC(points, mid); // min distance of left side
    float dr = closestPair_DC(points + mid, n-mid);  // ~ of right side
  
    float d = min(dl, dr); // best of dl and dr
  
    // Build strip[] for points near the dividor (closer than d)  
    Point strip[n]; 
    int n_stripe = 0; 
    for (int i = 0; i < n; i++) 
        if (abs(points[i].x - pmid.x) < d) 
            strip[n_stripe++] = points[i]; 
  
    // Find the closest points in strip.  Return the minimum of d and closest
    // distance is strip[]

    return min(d, ClosestPair_stripe(strip, n_stripe, d) ); 
} 

float closestPair(Point points[], int n) {
    // the main function that is be called
    //find distance of closest pair in a set of points
    qsort(points, n, sizeof(Point), compareX);

    return closestPair_DC(points, n);
}
// ............................................................................
// SDL and Graphics ...........................................................
void draw_SDL(Point points[], int n){

    // Init SDL2 + handle errors
    if(SDL_Init(SDL_INIT_VIDEO) != 0) {
        fprintf(stderr, "Could not init SDL: %s\n", SDL_GetError());
        return;
    }
    // Init screen and renderer + handle errors
    SDL_Window* window = NULL;
    SDL_Renderer* renderer = NULL;
    const int WINDOW_WIDTH  = 800;
    const int WINDOW_HEIGHT = 600;
    SDL_CreateWindowAndRenderer(WINDOW_WIDTH, WINDOW_HEIGHT, 0, &window, &renderer);
    if(!window || !renderer) {
        fprintf(stderr, "Could not create window/renderer: %s\n", SDL_GetError());
        return;
    }

    // Start the drawing;
    // clear the renderer
    SDL_SetRenderDrawColor(renderer, 0, 0, 0, SDL_ALPHA_OPAQUE);
    SDL_RenderClear(renderer);
    
    // Draw points[] 
    SDL_SetRenderDrawColor(renderer, 255, 255, 255, SDL_ALPHA_OPAQUE);
    for (int i = 0; i < n; i++)
        SDL_RenderDrawPoint(renderer, points[i].x, points[i].y);

    // Draw the line 
    //SDL_SetRenderDrawColor(renderer, 255, 0, 0, SDL_ALPHA_OPAQUE);
    //SDL_RenderDrawLine(renderer, WINDOW_WIDTH/2, 0, WINDOW_WIDTH/2, WINDOW_HEIGHT);

    // Apply everything on window
    SDL_RenderPresent(renderer);

    // Quit process //
    printf("(Enter any key to close SDL)\n");
    getchar();

    fprintf(stderr, "Exiting SDL\n");
    SDL_DestroyRenderer(renderer);
    SDL_DestroyWindow(window);
    SDL_Quit();
}

// main() .....................................................................
int main(){
    srand(time(NULL));
    int num = 6;
    Point points[100] = { {20, 30}, {120, 300}, {400, 500}, {50, 10}, {120, 100}, {30, 40}};

    // Data
    // for (int i = 0; i < num; i++){
        // points[i] = newPoint(rand()%num*40, rand()%num*30);
    // }

    for (int i = 0; i < num; i++)
        printPoint(points[i]);

    printf("Minimum distance : %f\n", closestPair(points, num));
    
    // Draw points + a line between Closest pair of points
    draw_SDL(points, num);
    return 0;
}
