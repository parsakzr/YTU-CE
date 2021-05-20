#include <stdio.h>
#include <stdlib.h>

// Struct -----------------------
typedef struct Student{
    int id;
    char* name;
    int age;
    float avg;

} Student;

// Fonksiyonler -----------------
void print_list(Student *list, int n){
    for (int i = 0; i < n; i++){
        printf("%d. ogrenci {\n", i+1);
        printf("\tID = %d\n", list[i].id);
        printf("\tAdi = %s\n", list[i].name);
        printf("\tYas = %d\n", list[i].age);
        printf("\tOrt. = %f\n", list[i].avg);
        printf("}\n");
    }
}
void sort_by_name(Student* list){
    
}

// Main -------------------------
int main(){
    Student *list;

    int n;
    printf("n = ");
    scanf("%d", &n);

    list = malloc(n * sizeof(Student));

    for (int i = 0; i < n; i++){
        printf("%d. ogrenci {\n", i+1);
        printf("\tID : "); scanf("%d", &list[i].id);
        printf("\tAdi : "); scanf("%s", &list[i].name);
        printf("\tYas : "); scanf("%d", &list[i].age);
        printf("\tOrt. : "); scanf("%f", &list[i].avg);
        printf("}\n");
    }

    print_list(list, n);
    
    // Sortler

    
    free(list);

    return 0;
}