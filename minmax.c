#include <stdio.h>
#include <stdlib.h>
#include <string.h>

#define MAXN    100
int A[MAXN] = {0};


int judge_x(int n, int m, int x) {
    int i, sum = 0, seg = 0;

    for (i = 0; i < n; i++) {
        if (A[i] > x) return 0;
        sum += A[i];
        if (sum > x) {
            seg++;
            if (seg > m - 1) return 0;
            sum = A[i];
        }
    }

    return 1;
}


int main1() {
    int m, n;
    while (scanf("%d %d", &n, &m) && n && m ) {
        int i, l = -1, h = 0;

        for (i = 0; i < n; i++) {
            scanf("%d", &A[i]);
            if (l < A[i]) l = A[i];
            h += A[i];
        }
        
        while (l < h) {
            int x = (l + h) / 2;
            if (judge_x(n, m, x)) h = x;
            else l = x + 1;
        }

        printf("%d\n", l); 
    }
}


int func(char *buf) {
    char *buf_t = buf;
    int bi = 0;
    while (bi++ < 10) {
        *buf_t++ = 'X';
    }

    printf("func buf_t = %s\n", buf_t);
    printf("func buf = %s\n", buf);
    
    return 0;
}


int main() {
    char *buf = (char *) malloc(512 * sizeof(char));
    memset(buf, 0, sizeof(buf));
    func(buf);
    
    printf("main buf = %s\n", buf);

    return 0;
}
