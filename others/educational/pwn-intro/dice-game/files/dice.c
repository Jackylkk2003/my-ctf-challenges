#include <stdio.h>
#include <stdlib.h>
#include <time.h>

void flag() {
    FILE *fp = fopen("flag.txt", "r");
    if (fp == NULL) {
        printf("Could not open flag.txt\n");
        return;
    }
    char flag[256];
    fgets(flag, sizeof(flag), fp);
    printf("You rolled a 100! Here is your flag: %s\n", flag);
    fclose(fp);
}

void dice() {
    int roll = (rand() % 6) + 1; // Generate a random number between 1 and 6
    char prayer[50];
    
    printf("You can get a flag if you roll a 100\n");
    printf("Pray to the dice god to boost your luck: ");
    scanf("%s", prayer);

    if (roll == 100) {
        flag();
    } else {
        printf("You rolled a %d. Better luck next time!\n", roll);
    }
}

int main() {
    setvbuf(stdout, NULL, _IONBF, 0); // Disable buffering for stdout
    setvbuf(stdin, NULL, _IONBF, 0);  // Disable buffering for stdin
    srand(time(NULL)); // Seed the random number generator
    
    dice();

    return 0;
}