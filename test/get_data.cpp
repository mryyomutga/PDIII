/*
 * Last Change: Wed 03 Oct 2018 18:06:59.
 */
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

    char buffer[2048];
    while(1) {
        int recv_size = recvfrom(sock, buffer, 2048, 0, NULL, NULL);
        printf("%s\n", buffer);
        memset(buffer, '\0', sizeof(buffer));
    }
    close(sock);

    return 0;
}
