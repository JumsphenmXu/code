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

static void init() {
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


static void solve() {
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


int main() {
    solve();
    
    while (1);
	return 0;
}