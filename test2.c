#include <stdio.h>
#include <math.h>
#include <stdlib.h>
#include <string.h>


#define N   8


int g_total = 0;
int c[N];


void eight_queen(int cur) {  
    int i, j;

    if (cur == N) { 
        g_total++;
        for (i = 0; i < N; ++i) 
            if (i < N - 1) printf("c[%d] = %d ", i, c[i]);
            else printf("c[%d] = %d\n", i, c[i]);
    }
    else {
        for (i = 0; i < N; ++i) {
            int ok = 1;
            c[cur] = i;
            for (j = 0; j < cur; ++j) {
                if (c[j] == c[cur] || j - c[j] == cur - c[cur]
                                   || j + c[j] == cur + c[cur])
                    ok = 0;
                    break;
            }

            if (ok) eight_queen(cur + 1);
        }
    }
}


int is_prime(int n) {
    int i;
    for (i = 2; i * i <= n; i++) {
        if (n % i == 0) return 0;
    }

    return 1;
}


void prime_circle(int A[], int n, int cur) {
    int i, j;
    if (cur == n && is_prime(A[0] + A[n - 1])) {
          for (i = 0; i < n; i++)
              if (i < n - 1) printf("%d ", A[i]);
              else printf("%d\n", A[i]);
    }
    else {
        for (i = 1; i <= n; i++) {
            A[cur] = i;
            int ok = 1;
            for (j = 0; j < cur; j++) {
                if (A[j] == A[cur] || !is_prime(A[j] + A[j + 1])) {
                    ok = 0;
                    break;
                } 
            }         
            if (ok) prime_circle(A, n, cur + 1);
        } 
    }
}


int chess_cover(int n, int px, int py) {
    int midx = 1, midy = 1, nt = n - 1;
    if (n == 1) return 1;
    
    while (nt--) midx *= 2;
    midy = midx;

    if (px < midx && py < midy) {
        return 1 + chess_cover(n - 1, px, py) + 3 * chess_cover(n - 1, 0, 0);
    }
}


int cards(float c) {
    float fsum = 0.00;
    int t = 1;
    while (fsum - c < 0.001) {
        t++;
        fsum += 1 / (float)t;
    }

    return t - 1;
}


// p + 23 * x = e + 28 * y = i + 33 * z > d


int main() {
    printf("%d\n", cards(1.00));
    printf("%d\n", cards(3.71));
    printf("%d\n", cards(0.04));
    printf("%d\n", cards(5.19));

    return 0;
}

