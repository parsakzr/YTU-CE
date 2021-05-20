/*
    Assignment 3: Graphs
    Description: Simple Search engine recommendations

    NOTE:  for Verbose mode, Uncomment the lines containing #LOG and #DEBUG
    NOTE2: The Frequency part was incomplete,
           but it conserves them while merging.
           only thing left is to increment and getMax().
*/

#include <stdio.h>
#include <stdlib.h>
#include <string.h>

#define MAXSTRLEN 10


typedef struct Node{
    char* query;
    int frequency;
    struct Node *next;
} Node;

typedef struct Graph{
    Node** list;
    int numVertices; // = Number of Vertices = V
} Graph;

// Methods ....................................................................

Node* createNode(const char* query){

    Node* node = (Node*) malloc(sizeof(Node));
    if(node == NULL){
        printf("- No memery to create the node: \"%s\"\n", query); // #DEBUG
        return NULL;
    }

    node->query = (char*) malloc(sizeof(strlen(query))+1);

    strcpy(node->query, query);
    node->frequency = 0;
    node->next = NULL;

    // printf("+ Node: \"%s\" created!\n"); // #LOG
    return node;
}

Node* duplicateNode(Node* node_src){
    Node* node = createNode(node_src->query);
    if(node == NULL){
        printf("- couldn't duplicate the node!\n"); // #DEBUG
        return NULL;
    }
    node->frequency = node_src->frequency;
    node->next = NULL;
    // node->next shouldn't be copied.

    return node;
}

Graph* createGraph(int numVertices){
    Graph* graph = (Graph*) malloc(sizeof(Graph));
    
    graph->numVertices = numVertices;
    graph->list = (Node**) malloc(numVertices * sizeof(Node*));

    for(int i=0; i<numVertices; i++)
        graph->list[i] = NULL;

    // printf("+ Graph created!\n"); // #LOG
    return graph;
}

void addNode(Graph* graph, const char* query){
    Node* node = createNode(query);

    // printf("[] Adding node \"%s\" ...", node->query); // #DEBUG 
    
    int i=0;
    while ((i < graph->numVertices) && (graph->list[i] != NULL))
        i++;
    
    if(i >= graph->numVertices){
        printf("- Graph is full, cannot add anymore!\n"); // #DEBUG
        return;
    }
        
    graph->list[i] = node;
    // printf("+ the node \"%s\" added to \the %dth of graph!\n",
    //         node->query, i); // #LOG
}


Node* getNode(Graph* graph, const char* query){
    // Node* node = createNode(query);

    // printf("finding node \"%s\" ... ", query); // #LOG
    
    int i=0;
    while ((i < graph->numVertices) && //not end of file
            graph->list[i] && // not null
            strcmp(graph->list[i]->query, query)) // not equal
        i++;

    if(i >= graph->numVertices || !graph->list[i]){
        // printf("- \"%s\" Not Found!\n", query); // #LOG
        return NULL;
    }
    
    // printf("+ Found the node \"%s\" at %dth index\n", query, i); // #LOG
    return graph->list[i];
}

void addEdge(Graph* graph, const char* query1, const char* query2){
    // if vertices wasn't found, it will call addNode() to appent them
    Node* node = (Node*)malloc(sizeof(Node));
    Node *node_q1, *node_q2;
    node_q1 = getNode(graph, query1);
    node_q2 = getNode(graph, query2);

    if(node_q1 == NULL){
        addNode(graph, query1);
        node_q1 = getNode(graph, query1);
    }
    if(node_q2 == NULL){
        addNode(graph, query2);
        node_q2 = getNode(graph, query2);
    }
    
    // add edge from q1 to q2
    node = createNode(query2);
    node->next = node_q1->next; // not inserting to head, but to head->next ..
    node_q1->next = node;       // .. to conserve the head as the vertex itself
    // add edge from q2 to q1 since it's undirected
    node = createNode(query1);
    node->next = node_q2->next; // conserve head, insert to head->next
    node_q2->next = node;
}

int isEdge(Graph* graph, const char* query1, const char* query2){
    Node* node_q1 = getNode(graph, query1);
    if(node_q1 == NULL){
        // printf("- Edge: %s -> %s Doesn't exist;"
        //         " %s not found!\n", query1, query2, query1); // #DEBUG
        return 0;
    }
    // Found the source vertex, now finding in its edges. 
    while(node_q1 && strcmp(node_q1->query, query2))
        node_q1 = node_q1->next;

    if(node_q1 == NULL){ // reached end of the list ==> not found
        // printf("- Edge: %s -> %s Doesn't exist;"
        //         " %s not found!\n", query1, query2, query2); // #DEBUG
        return 0;
    }
    // Found the destination vertex
    printf("+ Edge: \"%s\" -> \"%s\" found!\n", query1, query2);
    return 1;
}

void printGraph(Graph* graph) {
    // prints the adjacency list
    for (int i = 0; i < graph->numVertices; i++) {
        Node* temp = graph->list[i];
        if(temp != NULL){
            while (temp) {
                printf("%s", temp->query);
                if(temp->next)printf(" -> ");
                temp = temp->next;
            }
            printf("\n");
        }
    }
}

// void appendGraph(Graph* graph_dest, Graph* graph_src){
//     // Append to an empty graph_dest to duplicateGraph()
//     // Appending to a graph_dest with a lower capacity slices the graph_src
// }

void copyGraph(Graph* graph_dest, Graph* graph_src){

    Node *node_src, *node_dest, *temp; // node_X is for node[i] of graph_X
    for (int i=0; i < graph_src->numVertices; i++){
        node_src = graph_src->list[i];
        if(node_src){
            graph_dest->list[i] = duplicateNode(node_src);
            node_dest = graph_dest->list[i];
            while(node_src->next){
                // insert to the end
                node_dest->next = duplicateNode(node_src->next);
                node_dest = node_dest->next;
                node_src = node_src->next;
            }
        }
    }
    
}

Graph* mergeGraphs(Graph* graph1, Graph* graph2){
    // Merges two graphs and returns the merged graph
    Graph* graph_merged = createGraph(graph1->numVertices+graph2->numVertices);
    if(graph_merged == NULL){
        printf("- Couldn't merge the graphs; memory not allocated!\n"); // #DEBUG
        return NULL;
    }

    graph_merged->numVertices = graph1->numVertices + graph2->numVertices;

    // copy the graph1, then merge with graph2
    copyGraph(graph_merged, graph1);
    
    // merge with graph2
    Node *node2, *node_merged; // nodeX used for graphX
    int i, j; // i for graph2.list[i], j= i+graph1.numVertices for graph_merged
    for (i=0; i < graph2->numVertices; i++){
        node2 = graph2->list[i];
        node_merged = getNode(graph_merged, node2->query);
        if(node_merged == NULL){ // non-common
            j = i + graph1->numVertices;
            graph_merged->list[j] = duplicateNode(node2);
            node_merged = graph_merged->list[j]; // changed only if NULL
            while(node2->next){
                // insert to the end
                node_merged->next = duplicateNode(node2->next);
                node_merged = node_merged->next;
                node2 = node2->next;
            }
        }
        else{// node_merged was found by query2
            // common ==> only append edges to related vertex
            Node* temp = duplicateNode(node2->next);
            temp->next = node_merged->next; // inserting to beginning, ...
            node_merged->next = temp; // contd. conserving head
        }
    }

    return graph_merged;
}


int main(){
    Graph *graph1 = createGraph(4),
          *graph2 = createGraph(5),
          *graph_merged; // will be the merged graph of graph1 and graph2

    addEdge(graph1, "A", "B"); // can be longer strings as well
    addEdge(graph1, "A", "C"); // contd. the test cases given as one char
    addEdge(graph1, "A", "D");

    addEdge(graph2, "F", "C");
    addEdge(graph2, "F", "H");
    addEdge(graph2, "F", "I");
    addEdge(graph2, "F", "B");


    printf("[] Printing graph1:\n"); // #LOG
    printGraph(graph1);

    printf("[] Printing graph2:\n"); // #LOG
    printGraph(graph2);

    printf("[] MERGING the graphs...\n"); // #LOG
    graph_merged = mergeGraphs(graph1, graph2);

    printf("[] Printing graph_merged:\n"); // #LOG
    printGraph(graph_merged);


    free(graph1);
    free(graph2);
    free(graph_merged);
    return 0;
}