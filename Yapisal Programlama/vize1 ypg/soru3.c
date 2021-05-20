 #include <stdio.h>
#include <stdlib.h>

// Struct -----------------------
typedef struct Room{
    int id;
    float height, width, lenght;
    float volume;
} Room;

float volume(Room self){
    return self.height * self.width * self.lenght;
}
// Fonksiyonler -----------------
void getInfo(Room *list, int n){
    for (int i = 0; i < n; i++){
        printf("%d. Room {\n", i+1);
        printf("\tID : "); scanf("%d", &list[i].id);
        printf("\tYukseklik : "); scanf("%f", &list[i].height);
        printf("\tGenislik : "); scanf("%f", &list[i].width);
        printf("\tUzunluk : "); scanf("%f", &list[i].lenght);
        printf("}\n");
    }
}
void printInfo(Room *list, int n){
    for (int i = 0; i < n; i++){
        printf("%d. Room {", i+1);
        printf("ID = %d, ", list[i].id);
        printf("yukseklik = %f, ", list[i].height);
        printf("genislik = %f, ", list[i].width);
        printf("uzunluk = %f, ", list[i].lenght);
        printf("Volume = %f ", volume(list[i]));
        printf("}\n");
    }
}


void sortByVolume(Room* list, int n){
    Room temp;
    int i, j;
    for (i = 0; i < n-1; i++)           
       for (j = 0; j < n-i-1; j++)  
            if (volume(list[j]) > volume(list[j+1])){ 
                temp = list[j];
                list[j] = list[j+1];
                list[j+1] = temp;
            }
}

void scanRooms(Room* list, int n){
    float vlm; // i. odanin hacimi
    for (int i = 1; i < n-1; i++){ // en basi ve en sonu yok.
        vlm = volume(list[i]);
        if(vlm > volume(list[i-1]) && vlm > volume(list[i+1]))
            printf("%d ", list[i].id);
    }
    printf("\n");
}

// Main -------------------------
int main(){
    Room *list;

    int n;
    printf("n = ");
    scanf("%d", &n);

    list = malloc(n * sizeof(Room));

    getInfo(list, n); // #Madde a

    printf("------------\n");
    printInfo(list, n); // #Madde c
    
    printf("------------\n");
    printf("scanRoom() IDs:\n");
    scanRooms(list, n); // #Madde b

    printf("------------\n");
    printf("Sort edikten sonra:\n");
    sortByVolume(list, n); // #Madde d
    printInfo(list, n); // #Madde f

    
    free(list);

    return 0;
}