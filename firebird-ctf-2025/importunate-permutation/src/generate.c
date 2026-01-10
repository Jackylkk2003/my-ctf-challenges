#include <stdio.h>
#include <assert.h>
#include <stdlib.h>
#include <time.h>

#define N 100
#define M 10000000


void reverse(int *first, int *last) {
    // Reverses the order of the elements in the range [first, last).
    while (first < last) {
        int t = *first;
        *first = *--last;
        *last = t;
        first++;
    }
}

void next_permutation(int *first, int *last) {
    // 1. Find the largest index k such that a[k] < a[k + 1]. If no such index exists, the permutation is the last permutation.
    int *k = last - 2;
    while (k >= first && *k >= *(k + 1)) {
        k--;
    }
    if (k < first) {
        reverse(first, last);
        return;
    }

    // 2. Find the largest index l greater than k such that a[k] < a[l].
    int *l = last - 1;
    while (*k >= *l) {
        l--;
    }

    // 3. Swap the value of a[k] with that of a[l].
    int t = *k;
    *k = *l;
    *l = t;

    // 4. Reverse the sequence from a[k + 1] up to and including the final element a[n].
    reverse(k + 1, last);
}

void swap(int *a, int *b) {
    int t = *a;
    *a = *b;
    *b = t;
}

int main() {
    int g[N];
    int t;
    int i;
    int idx;
    int priv_a;
    int pub_a[N];
    int priv_b;
    int pub_b[N];
    int shared_a[N];
    int shared_b[N];
    srand(time(0));
    priv_a = rand() % M;
    priv_b = rand() % M;

    for (i = 0; i < N; i++) {
        g[i] = i;
    }
    for (i = 0; i < N; i++) {
        idx = rand() % (i + 1);
        swap(&g[i], &g[idx]);
    }
    for (i = 0; i < N; i++) {
        printf("%d%c", g[i], " \n"[i == N - 1]);
    }

    for (i = 0; i < N; i++) {
        pub_a[i] = g[i];
    }
    for (i = 0; i < priv_a; i++) {
        next_permutation(pub_a, pub_a + N);
    }

    for (i = 0; i < N; i++) {
        printf("%d%c", pub_a[i], " \n"[i == N - 1]);
    }

    
    for (i = 0; i < N; i++) {
        pub_b[i] = g[i];
    }
    for (i = 0; i < priv_b; i++) {
        next_permutation(pub_b, pub_b + N);
    }

    for (i = 0; i < N; i++) {
		printf("%d%c", pub_b[i], " \n"[i == N - 1]);
	}
    for (i = 0; i < N; i++) {
        shared_a[i] = pub_a[i];
    }

    for (i = 0; i < priv_b; i++) {
        next_permutation(shared_a, shared_a + N);
    }
    for (i = 0; i < N; i++) {
        shared_b[i] = pub_b[i];
    }
    for (i = 0; i < priv_a; i++) {
        next_permutation(shared_b, shared_b + N);
    }
    for (i = 0; i < N; i++) {
        if (shared_a[i] != shared_b[i]) {
            exit(-1);
        }
    }
	for (i = 0; i < N; i++) {
		printf("%d%c", shared_a[i], " \n"[i == N - 1]);
	}
    
	return 0;
}