#include <stdio.h>

void win() {
    FILE *fp = fopen("flag.txt", "r");
    if (fp == NULL) {
        printf("Could not open flag.txt\n");
        return;
    }
    char flag[256];
    fgets(flag, sizeof(flag), fp);
    printf("Flag: %s\n", flag);
    fclose(fp);
}

void init() {
    setvbuf(stdout, NULL, _IONBF, 0);
    setvbuf(stdin, NULL, _IONBF, 0);
}

void vuln() {
    printf("Fun fact: The init function is at %p\n", init);
    puts("===============================================================");
    puts("This is a simple fibonacci calculator. Enter a number and it will calculate the nth Fibonacci number.");
    puts("It calculates the nth Fibonacci number if you give it n");
    puts("===============================================================");
    
    long long fib[30];
    fib[0] = 0;
    fib[1] = 1;
    for (int i = 2; i < 30; i++) {
        fib[i] = fib[i - 1] + fib[i - 2];
    }
    
    printf("Enter n: ");
    int n;
    scanf("%d", &n);
    printf("Fibonacci number %d is: %lld\n", n, fib[n]);

    puts("===============================================================");
    puts("By the way, I forgot to ask for your name. Can you tell me your name?");
    char buf[50];
    scanf("%s", buf);
    printf("Nice to meet you, %s!\n", buf);
    puts("Bye!");
}

int main() {
    init();
    vuln();
    return 0;
}