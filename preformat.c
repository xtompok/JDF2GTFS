#include <stdlib.h>
#include <stdio.h>
#include <string.h>

int main (int argc, char ** argv){
	unsigned char line[1024];
	unsigned char end = 0;
	while (!feof(stdin)){
		unsigned int idx;
		idx = 0;
		while (1){
			int c;
			c = getchar();
			if (c == '\n' || c == EOF){
				if (c==EOF){
					end = 1;
				}
				if (idx > 0)
					line[idx-1] = 0;
				else 
					end=1;
				break;
			}
			line[idx] = ((unsigned char)c);
			idx++;
		if (end)
			break;
				
		}
		for(int i=1;i<argc; i++){
			if (strcmp(argv[i],"{}")==0){
				printf("%s",line);
			} else {
				printf("%s",argv[i]);
			}	
			if (i<(argc-1))
				putchar(',');
		}
		printf("\n");
	}
	return 0;
}
