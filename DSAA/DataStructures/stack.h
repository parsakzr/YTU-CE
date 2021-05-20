/*
Data Structure: Stack
Implementation: W/ Array
*/
#define MAX 16

typedef struct Stack{
    int item[MAX];
    int top;
} Stack;

void initStack(Stack *s){
    s->top = 0;
}

int isEmpty(Stack *s){
    if (s->top)
        return 1;
    return 0;
}

int isFull(Stack *s){
    if (s->top == MAX)
        return 1;
    return 0;
}

int push(Stack *s, int value){
    if (isFull(s))
        return 0;
    s->item[s->top++] = value;
    return 1;
}

int pop(Stack *s, int *variable){
    if (isEmpty(s))
        return 0;
    *variable = s->item[--s->top];
    return 1;
}


int top(Stack *s, int *variable){
    if (isEmpty(s))
        return 0;
    *variable = s->item[s->top - 1];
    return 1;
}
