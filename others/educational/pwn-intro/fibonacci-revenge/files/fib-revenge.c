#include <stdio.h>
#include <stdlib.h>
#include <string.h>

unsigned int password;

void win() {
    puts("What? Why are you here? You shouldn't be here! I am not giving you the flag! It is password protected!");

    FILE *fp = fopen("flag.txt", "r");
    if (fp == NULL) {
        printf("Could not open flag.txt\n");
        return;
    }
    
    puts("Now, enter the password to get the flag:");
    unsigned int input_password;
    scanf("%u", &input_password);
    if (input_password != password) {
        puts("Incorrect password! You are not allowed to see the flag!");
        fclose(fp);
        exit(1);
    }
    else {
        puts("Well, you have the correct password! Here is the flag.");
        char flag[256];
        fgets(flag, sizeof(flag), fp);
        printf("Flag: %s\n", flag);
        fclose(fp);
    }
}

void init() {
    setvbuf(stdout, NULL, _IONBF, 0);
    setvbuf(stdin, NULL, _IONBF, 0);

    // Initialize password with /dev/urandom
    FILE *fp = fopen("/dev/urandom", "r");
    if (fp == NULL) {
        printf("Could not open /dev/urandom\n");
        exit(1);
    }
    fread(&password, sizeof(password), 1, fp);
    fclose(fp);
}

void vuln() {
    printf("Fun fact: The init function is at %p\n", init);
    puts("===============================================================");
    puts("This is a simple fibonacci calculator. Enter a number and it will calculate the nth Fibonacci number.");
    puts("It calculates the nth Fibonacci number if you give it n");
    puts("===============================================================");
    
    unsigned int pw = password; // Unused variable, doesn't matter anyway

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

    // Buffer overflow is bad :<
    if (strlen(buf) > 49) {
        puts("Input too long! Attack detected!");
        exit(1);
    }

    printf("Nice to meet you, %s!\n", buf);
    puts("Bye!");
}

int main() {
    init();
    vuln();
    return 0;
}