#include <stdio.h>
#include <stdlib.h>

#define MAX 2
// ...........................
typedef struct Node{
    int value;
    int row;
    int column;
    struct Node *next;
} Node;

Node* initNode(int value, int row, int column){
    Node* node = (Node*)malloc(sizeof(Node));
    if(node == NULL){
        printf("Allocation Error!\n");
        exit(0);
    }

    node->value = value;
    node->row = row;
    node->column = column;
    node->next = NULL;

    return node;
}
void printList(Node* head){
    Node* p;
    for(p=head; p!=NULL; p=p->next)
        printf("[%d -> (%d, %d)]\n", p->value, p->row, p->column);
}
// ...........................
void findEmptyColumns(Node* head){
    int cols[MAX] = {0}; // assume all are empty
    Node* p;
    for(p=head; p!=NULL; p=p->next){
        if(p->value != 0)
            cols[p->column] = 1; // is not empty
    }

    printf("Solution: \n");
    for (int i = 0; i < MAX; i++){
        if(cols[i] == 0) // still empty
            printf("%d ", i);
    }
    
}
// ...........................
int main(){
    Node* head;
    Node* n1 = initNode(0, 0, 0);
    Node* n2 = initNode(0, 0, 1);
    Node* n3 = initNode(2, 1, 0);
    Node* n4 = initNode(1, 1, 1);

    n3->next = n4;
    n2->next = n3;
    n1->next = n2;
    head = n1;


    printList(head);
    findEmptyColumns(head);
    
    return 0;
}
