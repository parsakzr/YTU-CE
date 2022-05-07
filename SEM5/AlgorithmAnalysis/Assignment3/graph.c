#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#define SIZE 40

struct node
{
    int vertex;
    struct node *next;
};

struct node *createNode(int v);

struct Graph
{
    int numVertices;
    int *visited;

    struct node **adjLists;
};
struct queue
{
    int items[SIZE];
    int front;
    int rear;
};

struct queue *createQueue();
void enqueue(struct queue *q, int);
int dequeue(struct queue *q);
void display(struct queue *q);
int isEmpty(struct queue *q);
void printQueue(struct queue *q);

struct node *createNode(int);

void printPath(int path[], int k)
{
    printf("Path= ");
    int i = 0;
    for (i = 0; i < k; i++)
    {
        printf("%d, ", path[i]);
    }
    printf("\n");
}

void findPathsK(struct Graph *graph, int from, int to, int k_max)
{
    struct queue *q = createQueue();

    int path[graph->numVertices];

    graph->visited[from] = 1;
    enqueue(q, from);

    while (!isEmpty(q))
    {
        printQueue(q);
        int currentVertex = dequeue(q);
        printf("Visited %d\n", currentVertex);

        struct node *temp = graph->adjLists[currentVertex];

        while (temp)
        {
            int adjVertex = temp->vertex;

            if (graph->visited[adjVertex] == 0)
            {
                graph->visited[adjVertex] = 1;
                enqueue(q, adjVertex);
            }
            temp = temp->next;
        }
        // if last vertex is the desired destination
        // then print the path
        if (temp->vertex == to)
            printPath(path, k_max);
    }
}

void find_paths(struct Graph *graph, int startVertex, int dst)
{
    struct queue *q = createQueue();

    graph->visited[startVertex] = 1;
    enqueue(q, startVertex);

    while (!isEmpty(q))
    {
        printQueue(q);
        int currentVertex = dequeue(q);
        printf("Visited %d\n", currentVertex);

        struct node *temp = graph->adjLists[currentVertex];

        while (temp)
        {
            int adjVertex = temp->vertex;

            if (graph->visited[adjVertex] == 0)
            {
                graph->visited[adjVertex] = 1;
                enqueue(q, adjVertex);
            }
            temp = temp->next;
        }
    }
}

struct queue *createQueue()
{
    struct queue *q = malloc(sizeof(struct queue));
    q->front = -1;
    q->rear = -1;
    return q;
}

// Check if the queue is empty
int isEmpty(struct queue *q)
{
    if (q->rear == -1)
        return 1;
    else
        return 0;
}

// Adding elements into queue
void enqueue(struct queue *q, int value)
{
    if (q->rear == SIZE - 1)
        printf("\nQueue is Full!!");
    else
    {
        if (q->front == -1)
            q->front = 0;
        q->rear++;
        q->items[q->rear] = value;
    }
}

// Removing elements from queue
int dequeue(struct queue *q)
{
    int item;
    if (isEmpty(q))
    {
        printf("Queue is empty");
        item = -1;
    }
    else
    {
        item = q->items[q->front];
        q->front++;
        if (q->front > q->rear)
        {
            printf("Resetting queue ");
            q->front = q->rear = -1;
        }
    }
    return item;
}

void printQueue(struct queue *q)
{
    int i = q->front;

    if (isEmpty(q))
    {
        printf("Queue is empty");
    }
    else
    {
        printf("\nQueue contains \n");
        for (i = q->front; i < q->rear + 1; i++)
        {
            printf("%d ", q->items[i]);
        }
    }
}

// DFS algo
void DFS(struct Graph *graph, int vertex)
{
    struct node *adjList = graph->adjLists[vertex];
    struct node *temp = adjList;

    graph->visited[vertex] = 1;
    printf("Visited %d \n", vertex);

    while (temp != NULL)
    {
        int connectedVertex = temp->vertex;

        if (graph->visited[connectedVertex] == 0)
        {
            DFS(graph, connectedVertex);
        }
        temp = temp->next;
    }
}

struct node *createNode(int v)
{
    struct node *newNode = malloc(sizeof(struct node));
    newNode->vertex = v;
    newNode->next = NULL;
    return newNode;
}

struct Graph *createGraph(int vertices)
{
    struct Graph *graph = malloc(sizeof(struct Graph));
    graph->numVertices = vertices;

    graph->adjLists = malloc(vertices * sizeof(struct node *));

    graph->visited = malloc(vertices * sizeof(int));

    int i;
    for (i = 0; i < vertices; i++)
    {
        graph->adjLists[i] = NULL;
        graph->visited[i] = 0;
    }
    return graph;
}

// Add edge
void addEdge(struct Graph *graph, int src, int dest)
{
    // Add edge from src to dest
    struct node *newNode = createNode(dest);
    newNode->next = graph->adjLists[src];
    graph->adjLists[src] = newNode;

    // Add edge from dest to src
    newNode = createNode(src);
    newNode->next = graph->adjLists[dest];
    graph->adjLists[dest] = newNode;
}

// Print the graph
void printGraph(struct Graph *graph)
{
    int v;
    for (v = 0; v < graph->numVertices; v++)
    {
        struct node *temp = graph->adjLists[v];
        printf("\n Adjacency list of vertex %d\n ", v);
        while (temp)
        {
            printf("%d -> ", temp->vertex);
            temp = temp->next;
        }
        printf("\n");
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
        printf("Could not open file");
        return 0;
    }

    for (c = getc(fp); c != EOF; c = getc(fp))
        if (c == '\n')
            count = count + 1;

    printf("line count:%d\n", count);

    int V = count;
    int *hour = (int *)malloc(V * sizeof(int));
    int *minute = (int *)malloc(V * sizeof(int));
    int *price = (int *)malloc(V * sizeof(int));
    char city_list[V][20];
    char city[20], destination[20];
    int l = 0;
    int k = 0;
    struct Graph *graph = createGraph(V);
    rewind(fp);
    int i;

    while (fscanf(fp, "%s %s %d %d %d", city, destination, &hour[k], &price[k], &minute[k]) != EOF)
    {
        int flag1 = 0;
        int flag2 = 0;
        int c;
        int d;
        for (i = 0; i < l; i++)
        {
            if (!strcmp(city_list[i], city))
                flag1 = 1;
            if (!strcmp(city_list[i], destination))
                flag2 = 1;
        }
        if (flag1 == 0)
        {
            strcpy(city_list[l], city);
            l++;
        }
        if (flag2 == 0)
        {

            strcpy(city_list[l], destination);
            l++;
        }
        for (i = 0; i < l; i++)
        {
            if (!strcmp(city_list[i], city))
                c = i;
            if (!strcmp(city_list[i], destination))
                d = i;
        }
        addEdge(graph, c, d);
        k++;
    }
    for (i = 0; i < l; i++)
        printf("%s \n", city_list[i]);

    int exit = 1;

    int v;
    char kalkis[20];
    char varis[20];
    int d;
    while (exit)
    {
        printf("kalkis yerini giriniz:");
        scanf("%s", kalkis);
        printf("varis yerini giriniz: ");
        scanf("%s", varis);
        for (i = 0; i < l; i++)
        {
            if (!strcmp(city_list[i], kalkis))
                c = i;
            if (!strcmp(city_list[i], varis))
                d = i;
        }

        findPathsK(graph, c, d, 5);
        printf("c:%d d:%d", c, d);
    }

    fclose(fp);
    return 0;
}
