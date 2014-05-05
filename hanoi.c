#include <stdio.h>


int hanoi(int n, char A, char B, char C) {
    if (n == 1) {
        printf("%c-->%c\n", A, B);
        return 1;
    }

    return  1 + hanoi(n - 1, A, C, B) + hanoi(n - 1, C, B, A);
}


int main() {
    char A, B, C;
    A = 'A';
    B = A + 1;
    C = B + 1;
    printf("count = %d\n", hanoi(10, A, B, C)); 
    return 0;
}
