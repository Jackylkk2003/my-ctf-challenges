#include <stdio.h>
#include <stdlib.h>

int main() {
	setvbuf(stdin, NULL, _IONBF, 0);
	setvbuf(stdout, NULL, _IONBF, 0);

	printf("Tell me your favourite number:\n");
	int n = 0;
	scanf("%d", &n);
	if (n % 2 == 1) {
		printf("Odd numbers are odd, I don't like them :<\n");
		return 0;
	}
	if (n % 3 == 0) {
		printf("I don't like numbers that are divisible by 3, I always have a hard time cutting a cake into 3 pieces :<\n");
		return 0;
	}
	if (n % 3 == 1) {
		printf("Why would you choose a number that when I divide into 3 parts, there is a little bit left over? :<\n");
		return 0;
	}
	if (n % 3 == 2) {
		printf("I thought a little piece is missing when I divide the number by 3, why leave me with a missing piece? :<\n");
		return 0;
	}
	if (abs(n) != n) {
		printf("Negative numbers are evil, it always made me calculate things incorrectly :<\n");
		return 0;
	}
	printf("This number looks good, I like it :>\n");
	printf("Next time tell me your favourite list instead.\n");
	printf("\n");
	printf("You want a flag? Do you mean this one? %s\n", getenv("FLAG"));
	return 0;
}