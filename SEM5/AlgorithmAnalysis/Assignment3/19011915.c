#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#define MAX_LEN 32


// Queue ......................

typedef struct Queue {
    int items[MAX_LEN];
    int front;
    int rear;
} Queue;


Queue *createQueue() {
    Queue *q = (Queue *)malloc(sizeof(Queue));
    q->front = -1;
    q->rear = -1;
    return q;
}

int isEmpty(Queue *q) {
    if (q->rear == -1)
        return 1;
    else
        return 0;
}

void enqueue(Queue *q, int value) {
    if (q->rear == MAX_LEN - 1)
        printf("\nQueue is Full!!");
    else
    {
        if (q->front == -1)
            q->front = 0;
        q->rear++;
        q->items[q->rear] = value;
    }
}


int dequeue(Queue *q) {
    int item;
    if (isEmpty(q)) {
        printf("Queue is empty");
        item = -1;
    }
    else {
        item = q->items[q->front];
        q->front++;
        if (q->front > q->rear) {
            printf("Resetting queue ");
            q->front = q->rear = -1;
        }
    }
    return item;
}

void printQueue(Queue *q) {
    int i = q->front;

    if (isEmpty(q)) {
        printf("Queue is empty");
    }
    else {
        printf("\nQueue contains \n");
        for (i = q->front; i < q->rear + 1; i++)
        {
            printf("%d ", q->items[i]);
        }
    }
}

// Graph ......................

struct Edge;
struct Node;
struct Graph;

typedef struct Node {
    char name[MAX_LEN];
    // struct Edge *children; // edge info
} Node;


typedef struct Edge {
    // = Flight
    // to store the "weight" info
    int dest; // index of desination vertex
    int duration, // in terms of minutes only, convert to hh:mm
        price;
    struct Edge *next;
} Edge;

typedef struct Graph {
    int V;
    Node vertices[MAX_LEN]; // Airports as vertex, its indices are used by edges
    Edge** adjList; // the Adjacency list
} Graph;


Graph* newGraph(){
    Graph* graph = (Graph*) malloc(sizeof(Graph));

    graph->adjList = (Edge**) calloc(MAX_LEN, sizeof(Edge*));
    int i;
    for (i = 0; i < MAX_LEN; i++){
        graph->adjList[i] = (Edge*) malloc(sizeof(Edge));
    }
    
    return graph;
}

void addVertex(Graph* graph, char name[]){
    // add a new city as a vertex to the graph
    strcpy(graph->vertices[graph->V++].name, name);
}

void addEdge(Graph* graph, int v1, int v2, int duration, int price){
    graph->adjList[v1]->dest = v2;
    graph->adjList[v1]->duration = duration;
    graph->adjList[v1]->price = price;

    graph->adjList[v2]->dest = v1;
    graph->adjList[v2]->duration = duration;
    graph->adjList[v2]->price = price;
}

// Utilities ................
int indexOf(Graph* graph, char name[]){
    int i=0;
    while (i < graph->V && strcmp(graph->vertices[i].name, name))
        i++;
    
    if (i >= graph->V) // not found
        return -1;
    // found
    return i;
}

void findPathsK(struct Graph *graph, int from, int to, int k_max) {
    struct queue *q = createQueue();
    int visited[MAX_LEN];

    int path[MAX_LEN], count=0; 
    int price = 0;

    visited[from] = 1;
    enqueue(q, from);

    while (!isEmpty(q))
    {
        printQueue(q);
        int current = dequeue(q);
        printf("Visited %d\n", current);

        Edge *temp = graph->adjList[current];

        while (temp){
            int adjV = temp->dest;

            if (visited[adjV] == 0)
            {
                visited[adjV] = 1;
                enqueue(q, adjV);
                path[count++] = adjV;
                price += temp->price;
            }
            temp = temp->next;
        }
        // if last vertex is the desired destination
        // then print the path
        if (strcmp(graph->vertices[temp->dest].name, to)) 
            printPath(path, k_max);
    }
}

int main()
{
    FILE *fp;
    int count = 0;
    char c;
    fp = fopen("sample.txt", "r");

    if (fp == NULL)
    {
        fprintf(stderr, "ERR: Could not open file\n");
        exit(EXIT_FAILURE);
    }

    struct Graph *graph = newGraph();

    int hour, minute, price;
    char fromCity[MAX_LEN], toCity[MAX_LEN];
    int i;

    while (fscanf(fp, "%s %s %d %d %d", fromCity, toCity, &hour, &minute, &price) != EOF) {

        int from_index = indexOf(graph, fromCity);
        int to_index = indexOf(graph, toCity);

        if (from_index == -1) // not found
            addVertex(graph, fromCity);
        if (to_index == -1) // not found
            addVertex(graph, toCity);
        
        int duration = 60 * hour + minute;

        addEdge(graph, from_index, to_index, duration, price);
    }

    for (i = 0; i < graph->V; i++)
        printf("%s ", graph->vertices[i].name);

    // int exit = 1;

    // int v;
    // char kalkis[MAX_LEN];
    // char varis[MAX_LEN];
    // int d;
    // while (exit)
    // {
    //     printf("kalkis yerini giriniz:");
    //     scanf("%s", kalkis);
    //     printf("varis yerini giriniz: ");
    //     scanf("%s", varis);
    //     for (i = 0; i < l; i++)
    //     {
    //         if (!strcmp(city_list[i], kalkis))
    //             c = i;
    //         if (!strcmp(city_list[i], varis))
    //             d = i;
    //     }

    //     findPathsK(graph, c, d, 5);
    //     printf("c:%d d:%d", c, d);
    // }

    fclose(fp);
    return 0;

    return 0;
}