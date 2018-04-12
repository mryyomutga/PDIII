#include <stdio.h>
#include <string.h>
#include <unistd.h>
#include <sys/types.h>
#include <sys/socket.h>
#include <netinet/in.h>
#include <arpa/inet.h>

int main(int argc, char* argv[]){
    int sock = socket(AF_INET, SOCK_DGRAM, 0);

    struct sockaddr_in sa = {0};
    sa.sin_family = AF_INET;
    sa.sin_port = htons(12345);
    sa.sin_addr.s_addr = inet_addr("0.0.0.0");

    bind(sock, (struct sockaddr*) &sa, sizeof(sa));

    char buffer[4096];
    int recv_size = recvfrom(sock, buffer, 4096, 0, NULL, NULL);

    write(1, buffer, recv_size);

    close(sock);

    return 0;
}
