#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <unistd.h>

#include <sys/types.h>
#include <sys/socket.h>
#include <netinet/in.h>
#include <arpa/inet.h>

int main(int argc, const char *argv[]) {
    int sock = socket(AF_INET, SOCK_DGRAM, 0);
    struct sockaddr_in sa = {0};
    sa.sin_family = AF_INET;
    sa.sin_port = htons(8888);
    sa.sin_addr.s_addr = inet_addr("0.0.0.0");

    bind(sock, (struct sockaddr *)&sa, sizeof(sa));
    while(1) {
        char buffer[2048];
        int recv_size = recvfrom(sock, buffer, 2048, 0, NULL, NULL);
        printf("%d %s\n",recv_size, buffer);
    }
    close(sock);

    return 0;
}
