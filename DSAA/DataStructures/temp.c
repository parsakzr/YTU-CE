#include <stdio.h>
#include <stdlib.h>
 
#define MAX 100 // Needed for Stack

// ... <STACK> ................................................................
typedef struct Stack {
    int top;
    int* array;
} Stack;
 

Stack* initStack()
{
    Stack* stack = (Stack*)malloc(sizeof(Stack));
    stack->top = 0;
    stack->array = (int*)malloc(MAX * sizeof(int));
    return stack;
}
 

int isFull(Stack* stack)
{
    return stack->top == MAX;
}

int isEmpty(Stack* stack)
{
    return stack->top == 0;
}

int push(Stack* s, int value)
{
    if (isFull(s))
        return 0;
    s->array[s->top++] = value;
    return 1;
}

int pop(Stack* s, int *variable){
    if (isEmpty(s))
        return 0;
    *variable = s->array[--s->top];
    return 1;
}

int peek(Stack* s, int *variable){
    if (isEmpty(s))
        return 0;
    *variable = s->array[s->top - 1];
    return 1;
}
// ... </STACK> ...............................................................



int main()
{
    Stack* s = initStack();
 
    push(s, 10);
    push(s, 20);
    push(s, 30);
    int res;
    pop(s, &res);
    printf("%d popped from stack\n", res);
 
    return 0;
}