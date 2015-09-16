#include <iostream>
#include <cstdio>
#include <algorithm>
#include <cstring>
#include <cstdlib>
#include <utility>
#include <string>
#include <map>
#include <cctype>
#include <queue>

#pragma warning (disable: 4996)

using namespace std;

#define     MAX_LENGTH      100010


char input[MAX_LENGTH];
int n, pos;
bool error;


static int get_next() {
    if (pos >= n) {
        ++pos;
        return EOF;
    }

    return input[pos++];
}


static inline void put_back() {
    --pos;
}


static void skip() {
    char ch = get_next();
    while (ch == ' ') {
        ch = get_next();
    }

    put_back();
}


static int parse_num() {
    int res = 0;
    char ch = get_next();
    if (ch == EOF || !isdigit(ch)) {
        put_back();
        return 1;
    }

    while (isdigit(ch)) {
        res = 10 * res + ch - '0';
        ch = get_next();
    }

    put_back();
    return res;
}


static int get_length() {
    int res = 0;
    char ch = get_next();

    if (ch == ')') {
        return res;
    }

    while (true) {
        if (ch == '(') {
            int part = get_length();
            res += part * parse_num();
        } else if ('A' <= ch && ch <= 'Z') {
            res += parse_num();
        } else {
            break;
        }
		ch = get_next();
    }

    return res;
}


static pair<long long, bool> get_exp() {
	long long res = 0L;
	skip();

	char ch = get_next();
	if (isdigit(ch)) {
		put_back();
		res = (long long) parse_num();
		return make_pair(res, true);
	}

	if (ch != '(') {
		put_back();
		return make_pair(0, false);
	}

	int arg_cnt = 0;
	skip();
	ch = get_next();
	if (ch == '+') {
		arg_cnt = 0;
		res = 0L;
		while (true) {
			pair<long long, bool> plb = get_exp();
			if (!plb.second) {
				skip();
				if (get_next() != ')') {
					error = true;
					return make_pair(0, false);
				} else {
					break;
				}
			} else {
				res += plb.first;
				++arg_cnt;
			}
		}

		if (arg_cnt < 1) {
			error = true;
			return make_pair(0, false);
		}

		return make_pair(res, true);
	} else if (ch == '-') {
		res = 0L;
		pair<long long, bool> lhs = get_exp();
		pair<long long, bool> rhs = get_exp();
		skip();
		// This following statement can not be written as
		// if (!lhs.second || (!rhs.second && get_next() != ')')) 
		// because get_next() can be left un-executed if !rhs.second is identified as false
		// this is so called ***short-circuit calculation***
		if (!lhs.second || (get_next() != ')' && !rhs.second)) {
			error = true;
			return make_pair(0, false);
		} 

		return make_pair((rhs.second ? lhs.first - rhs.first : -lhs.first), true);
	} else if (ch == '*') {
		arg_cnt = 0;
		res = 1L;
		while (true) {
			pair<long long, bool> plb = get_exp();
			skip();
			if (!plb.second) {
				if (get_next() != ')') {
					error = true;
					return make_pair(0, false);
				} else {
					break;
				}
			} else {
				res *= plb.first;
				++arg_cnt;
			}
		}

		if (arg_cnt < 2) {
			error = true;
			return make_pair(0, false);
		}

		return make_pair(res, true);
	}

	error = true;
	put_back();
	return make_pair(0, false);
}


static void solve_length() {
    cin >> input;
    n = strlen(input);
    pos = 0;
    cout << get_length() << endl;
}


static void solve_exp() {
	gets(input);
	n = strlen(input);
	error = false;
	pos = 0;

	pair<long long, bool> res = get_exp();
	if (!res.second || error || get_next() != EOF) {
		cout << "invalid expression" << endl;
	} else {
		cout << res.first << endl;
	}
}

int main() {
	while (1) {
		solve_exp();
	}
    return 0;
}
