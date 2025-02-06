32 bit no pie, no canary, NX. So ROP.

Gives a nice diagram with the stack and return pointer


Dont try to put system string on the stack

`docker build -t server_netcat . && docker run --rm -p 12345:12345 server_netcat`