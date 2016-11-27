#include <stdlib.h>
#include <stdio.h>
#include <string.h>

int main (int argc, char ** argv){
	unsigned char line[1024];
	unsigned char end = 0;
	while (!feof(stdin)){
		unsigned int idx;
		idx = 0;
		line[0]=0;
		while (1){
			int c;
			c = getchar();
			if (c == '\n' || c == EOF){
				if (c==EOF){
					return 0;
				}
				if (idx > 0)
					line[idx-1] = 0;
				else 
					return 0;
				break;
			}
			line[idx] = ((unsigned char)c);
			idx++;
		}
		for(int i=0;i<strlen(line)-1;i++){
			if (line[i] == '"' && line[i+1] == '"'){
				memmove(line+i+4,line+i+2,1024-i-4);
				line[i]='N';
				line[i+1]='U';
				line[i+2]='L';
				line[i+3]='L';
			}
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
