#include <stdio.h>
#include <string.h>
#include <unistd.h>
#include <sys/types.h>
#include <sys/socket.h>
#include <netinet/in.h>
#include <arpa/inet.h>

#define MESSAGE "Hello World!"

int main(int argc, char* argv[]){
    int sock = socket(AF_INET, SOCK_DGRAM, 0);

    struct sockaddr_in sa = {0};
    sa.sin_family = AF_INET;
    sa.sin_port = htons(12345);
    sa.sin_addr.s_addr = inet_addr("127.0.0.1");

    sendto(sock, MESSAGE, strlen(MESSAGE),0, (struct sockaddr *)&sa, sizeof(sa));
    // この時点で自動的にバインドされる

    close(sock);
    return 0;
}
