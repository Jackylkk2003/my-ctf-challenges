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

void vuln() {
    char buf[0x10];
    printf("Enter some text: ");
    scanf("%s", buf);
}

void init() {
    setvbuf(stdout, NULL, _IONBF, 0);
    setvbuf(stdin, NULL, _IONBF, 0);
}

int main() {
    init();
    vuln();
    return 0;
}