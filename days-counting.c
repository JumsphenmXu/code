#include <stdio.h>
#include <string.h>
#include <stdlib.h>


#define OUT
#define IN
#define IS_LEAP_YEAR(x)\
  (((x) % 4 == 0 || ((x) % 400 == 0 && (x) % 100 != 0)) ? 1 : 0)


typedef struct Date_t {
    int year;
    int month;
    int day;
} Date_t;


int template[10][7] = {
    {1, 0, 1, 1, 1, 1, 1},
    {0, 0, 0, 0, 1, 0, 1},
    {1, 1, 1, 0, 1, 1, 0},
    {1, 1, 1, 0, 1, 0, 1},
    {0, 1, 0, 1, 1, 0, 1},
    {1, 1, 1, 1, 0, 0, 1},
    {1, 1, 1, 1, 0, 1, 1},
    {0, 0, 1, 0, 1, 0, 1},
    {1, 1, 1, 1, 1, 1, 1},
    {0, 1, 1, 1, 1, 0, 1}
};


int year_month_day[2][13] = {
    {0, 31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31},
    {0, 31, 29, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31}
};


int day_of_year(int year) {
    int month, days = 0;

    for (month = 1; month <= 12; month++) {
        days += year_month_day[IS_LEAP_YEAR(year)][month]; 
    }

    return days;
}


int calculate_days(Date_t from, Date_t to) {
    if (from.year > to.year) return -1;
    if (from.year == to.year && from.month > to.month) return -1;
    if (from.year == to.year && from.month == to.month
                             && from.day > to.day) return -1;

    int from_day = 0, to_day = 0;
    int  yi, mi;

    for (mi = 0; mi < from.month; mi++) {
        from_day += year_month_day[IS_LEAP_YEAR(from.year)][mi];
    }
    from_day += from.day;

    for (yi = from.year; yi < to.year; yi++) {
        to_day += day_of_year(yi);
    }
    for (mi = 0; mi < to.month; mi++) {
        to_day += year_month_day[IS_LEAP_YEAR(yi)][mi];
    }
    to_day += to.day;

    return (to_day - from_day);
}


int display(int IN num, unsigned char OUT *ptr) {
    int num_t = num, ai = 4, pi = 0, ti = 0;
    if (num < 10000 || num > 99999) return -1;
    int arr[5] = {0};

    while (num_t) {
        arr[ai--] = num_t % 10;
        num_t = num_t / 10;
    }

    memset(ptr, 0, sizeof(ptr));

    for (pi = 0; pi < 5; pi++) {
        for (ai = pi, ti = 0; ti < 7; ti++) {
            if (template[arr[ai]][ti]) ptr[pi] |= (1 << ti);
        }
    }
    
    for (pi = 0; pi < 5; pi++) printf("%x ", ptr[pi]);
     
    printf("\n");

    return 0;
}


int even_div2_or_odd_mul3_add1(int x) {
    int cnt = 0;
    while (x != 1) {
        if (x & 1) {
            x = ((x - 1)/2) * 3 + 2;
            cnt += 2;
        }
        else {
            x = x / 2;
            cnt += 1;
        }
    }
    
    return cnt;
}


void print_permutation(int n, int P[], int A[], int cur) {
    int i, j, A_cnt, P_cnt;

    if (cur == n) {
        for (i = 0; i < n; ++i) 
            if (i < n -1) printf("%d ", A[i]);
            else printf("%d\n", A[i]);
    }
    else { 
        for (i = 0; i < n; ++i) {
            if (!i || P[i] != P[i - 1]) {
                A_cnt = P_cnt = 0;
                for (j = 0; j < cur; ++j) if (A[j] == P[i]) A_cnt++;
                for (j = 0; j < n; ++j) if (P[j] == P[i]) P_cnt++;

                if (A_cnt < P_cnt) {
                    A[cur] = P[i];
                    print_permutation(n, P, A, cur + 1); 
                }

            }   // if (!i || P[i] != P[i - 1]) 
        }   // for (i = 0; i < n; ++i)  
    }   // else
}


int main(int argc, char **argv) {
    int n = 5;
    int P[5] = {1, 1, 2, 2, 4};
    int A[5] = {0};
    print_permutation(n, P, A, 0);
    return 0;
}
