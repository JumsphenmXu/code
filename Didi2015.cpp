#include <iostream>
#include <vector>
#include <queue>
#include <algorithm>
#include <cstdlib>
#include <cstring>
#include <cstdio>
#include <string>
#include <set>
#include <utility>
#include <cctype>
#include <cmath>
#include <functional>

using namespace std;


#define MAXN    10010

int val[MAXN];
// int dp[MAXN][MAXN];
int n;


static void problem1_init() {
    // cin >> n;
    int t, i = 0;
    while (scanf("%d", &t)) {
        val[i++] = t;
    }
    n = i;
    /*
    for (int i = 0; i < n; ++i) {
        cin >> val[i];
    }*/

    // memset(dp, 0, sizeof(dp));
}


static void problem1_solve() {
    int i, j, k;
    init();
    for (i = n; i > 0; --i) {
        for (j = 0; i + j <= n; ++j) {
            int sum = 0;
            for (k = j; k < i + j; ++k) {
                sum += val[k];
            }
            if (sum == 0) {
                for (k = j; k < i + j; ++k) {
                    printf("%d%c", val[k], k == i + j - 1 ? '\n' : ' ');
                }
                return;
            }
        }
    }

    // return 0;
}

// ********************************** //
// For problem2
int mat[MAXN][MAXN];
int m, sz, pos;
char str[MAXN<<2];


static int get_next() {
    if (pos >= sz) {
        ++pos;
        return EOF;
    }
    return str[pos++];
}


static inline void put_back() {
    --pos;
}


static int parse_num() {
    char ch = get_next();
    int num = 0, sgn = 1;
    if (ch == '-') {
        sgn = -1;
        ch = get_next();
    }

    while ('0' <= ch && ch <= '9') {
        num = 10 * num + ch - '0';
        ch = get_next();
    }

    put_back();
    return num * sgn;    
}


static void skip() {
    char ch = get_next();
    while (ch == ' ') {
        ch = get_next();
    }

    put_back();
}

static void print_mat() {
      for (int i = 0; i < m; ++i) {
            for (int j = 0; j < n; ++j) {
                printf("%d%c", mat[i][j], j == n - 1 ? '\n' : ' ');
            }
      }
}

static void init() {
    memset(str, 0, sizeof(str));
    gets(str);

    // cin >> m >> n;
    sz = strlen(str);
    m = n = pos = 0;
    int i = 0;

    skip();
    char ch = get_next();
    while (ch != EOF) {
        if (ch == ';') {
            ++m;
            n = i;
            i = 0;
        } else if (ch == '-' || '0' <= ch && ch <= '9') {
            put_back();
            mat[m][i++] = parse_num();
        }
        skip();
        ch = get_next();
    }

    ++m;
}

/*
static void init() {
    cin >> m >> n;
    for (int i = 0; i < m; ++i) {
          for (int j = 0; j < n; ++j) {
                cin >> mat[i][j];
          }
    }
}*/


static int solve() {
    int i, j, res = -(1 << 30);
    init();

    print_mat();
    for (i = 0; i < m - 1; ++i) {
        for (j = 0; j < n - 1; ++j) {
            int sum = mat[i][j] + mat[i][j+1] + mat[i+1][j] + mat[i+1][j+1];
            res = sum > res ? sum : res;
        }
    }

    return res;
}



int main() {
    problem1_solve();
    
    while (1);
	return 0;
}