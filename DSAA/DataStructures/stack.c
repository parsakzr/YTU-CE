#include <stdio.h>
#include "stack.h"

int main(){

    Stack* s;
    int val1, val2;
    int err1, err2;
    initStack(s);

    printf("Hello World!\n");

    push(s, 3);
    push(s, 4);

    err1 = pop(s, &val1);
    err2 = top(s, &val2);

    printf("Popped: %d, Peeked: %d\n", err1, err2);
    
    return 0;
}
