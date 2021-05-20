#include <stdio.h>
#include <time.h>

int power_fast(int base, int exponent){ // O(logN)
    if( exponent == 0)
        return 1;
    if ( exponent == 1)
        return base;
    if (exponent%2 == 0)
        return power_fast(base, exponent/2) * power_fast(base, exponent/2);
    if (exponent%2 == 1)
        return power_fast(base, exponent/2) * base * power_fast(base, exponent/2);
}

float power_rational( int base, int exp_num, int exp_denum, int step_limit){
    /*                                    aD
                        y[i]      y[i] xN
        y[i+1] = y[i] - ⎼⎼⎼⎼ + ⎼⎼⎼⎼⎼⎼⎼⎼⎼⎼⎼⎼⎼⎼
                         aD           aD   aN
                                aD y[i]   xD
    */
    float yi = 1.0;
    for (int i = 0; i < step_limit; ++i){
       yi = yi - (float)(yi/exp_denum) + (float)(yi * power_fast(base, exp_num) / (exp_num * power_fast(yi, exp_denum)));
       /*if (i % (step_limit/10) == 0){ //prints selected 10 steps
           printf("%d -> %f\n", i, yi);
       }*/
       
    }
    return yi;
}

int main(){
    int x, a, b; // x^(a/b)
    clock_t start_t = clock();

    printf("Enter: ");
    scanf("%d%d%d", &x, &a, &b);

    printf("Calculating...\n");
    float res = power_rational(x, a, b, 2000000);
    printf("%f\n", res);

    return 0;
}