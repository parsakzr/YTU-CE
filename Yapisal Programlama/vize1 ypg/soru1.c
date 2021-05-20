#include <stdio.h>
#include <stdlib.h>

int enbuyuk_bul(int **mat){
    int sum, sum_max = 0;
    int indx; // indx : buldugumuz max

    int n = sizeof(mat)/sizeof(mat[0]);

    for(int i=0; i<n; i++){
        sum = mat[i][0]*mat[i][0] + mat[i][1]*mat[i][1];
        if (sum > sum_max){
            sum_max = sum;
            indx = i;
        }
        i++;
    }
    
    return indx;    
}

void liste_yazdir(int **mat){
    int i=0;
    while(mat[i]){
        printf("%d + %dj\n", mat[i][0], mat[i][1]);
        i++;
    }
}


int main(){
    int n, **mat;
    printf("n = ");
    scanf("%d", &n);

    mat = malloc(n * sizeof(int*));
    for (int i = 0; i < n; i++)
        mat[i] = (int*) malloc(2 * sizeof(int));
    if (mat == NULL){
        printf("Memory alinamiyor");
        exit(0);
    }

    printf("sayilari giriniz :\n");
    for (int i = 0; i < n; i++){
        printf("%d. sayi = ", i+1);
        scanf("%d%d", &mat[i][0], &mat[i][1]);
    }
    

    printf("max : %d. satirda.\n", enbuyuk_bul(mat));

    liste_yazdir(mat);

    for (int i = 0; i < n; i++)
        free(mat[i]);
    free(mat);

    return 0;
}