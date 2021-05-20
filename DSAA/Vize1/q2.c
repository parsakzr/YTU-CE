#include <stdio.h>
#include <stdlib.h>

#define MAX 100

typedef struct Queue {
    int front, rear;
    int id[MAX];
    int page[MAX];
} Queue;

Queue* newQueue(){
    Queue* queue = (Queue*)malloc(sizeof(Queue));

    queue->front = 0;
    queue->rear = 0;

    return queue;
}

int isEmpty(Queue* queue);
int isFull(Queue* queue);

int enqueue(Queue* queue, int id, int page){
    if (isFull(queue))
        return 0; // error

    queue->id[queue->rear] = id;
    queue->page[queue->rear] = page;
    queue->rear++;

    return 1;
}

int dequeue(Queue* queue, int *id, int *page)
{
    if (isEmpty(queue))
        return 0; // error
    
    *id = queue->id[queue->front];
    *page = queue->page[queue->front];
    queue->front++;
    return 1;
}

int main()
{
    Queue* queue = newQueue();
 
    enqueue(queue, 1, 4);
    enqueue(queue, 2, 5);
    enqueue(queue, 3, 30);
    enqueue(queue, 4, 2);
    
    int id, page;
    dequeue(queue, &id, &page);

    printf("%d %d dequeued from queue\n\n", id, page);
 
    return 0;
}
