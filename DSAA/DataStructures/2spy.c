#include <stdio.h>
#include <stdlib.h>
 
#define MAX 100 // for all the array dimensions

// ... <STACK> ................................................................
typedef struct Stack { // a Stack of characters
    int top;
    char* array;
} Stack;

Stack* initStack(){
    Stack* stack = (Stack*)malloc(sizeof(Stack));
    stack->array = (char*)malloc(MAX * sizeof(char));
    stack->top = 0;
    return stack;
}

int isFull(Stack* stack){
    return stack->top == MAX;
}

int isEmpty(Stack* stack){
    return stack->top == 0;
}

int push(Stack* s, char value){
    if (isFull(s))
        return 0;
    s->array[s->top++] = value;
    return 1;
}

int pop(Stack* s, char *variable){
    if (isEmpty(s))
        return 0;
    *variable = s->array[--s->top];
    return 1;
}

int peek(Stack* s, char *variable){
    if (isEmpty(s))
        return 0;
    *variable = s->array[s->top - 1];
    return 1;
}

void printStack(Stack* s){
    char ch;
    while (!isEmpty(s)){
        pop(s, &ch);
        printf("%c", ch);
    }
    printf("\n");
}
// ... </STACK> ...............................................................

// ... Algorithm ..............................................................
void genKey(Stack *s, char* code){
    int isOK=1; // Exception: if popped empty stack
    int n, i, j;
    char ch, junk; // junk -> the function pop with no variable is not defined

    i=0;
    while (isOK && code[i] != '\0'){
        ch = code[i++];
        if (ch > 'a' && ch < 'z') // if ch: [a-z]
            push(s, ch);
        else if (ch > '0' && ch < '9'){ // if ch: [0-9]
            n = ch - '0';
            j = 0;
            while (isOK && j++ < n)
                isOK = pop(s, &junk); // pop the extra characters
        }
    }
    if (!isOK){
        printf("Error while generating the Key!\n");
    }
}

// ... main() .................................................................
int main(){
    Stack* stack1 = initStack();
    Stack* stack2 = initStack();
    char code1[MAX];
    char code2[MAX];
    
    // Input
    printf("Spy1, Enter the Code: ");
    scanf("%s", code1);
    printf("Spy2, Enter the Code: ");
    scanf("%s", code2);

    // Fill the stacks w/ the algorithm
    genKey(stack1, code1);
    genKey(stack2, code2);

    printf("The key generated by code1: (Reverse): ");
    printStack(stack1);
    printf("The key generated by code2: (Reverse): ");
    printStack(stack2);

    // Check if stack1 and stack2 are eqaul
    char char1, char2;
    int isEqual = 1;
    while (isEqual && !isEmpty(stack1) && !isEmpty(stack2)){
        pop(stack1, &char1);
        pop(stack2, &char2);
        if (char1 != char2)
            isEqual = 0;
    }

    // Output
    if(isEqual)
        printf("OK: They can communicate.\n");
    else
        printf("Not OK: They can't communicate.\n");
    
    return 0;
}