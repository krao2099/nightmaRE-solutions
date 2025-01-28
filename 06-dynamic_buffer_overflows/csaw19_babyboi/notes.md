No buffering in the binary

Messy to install dependencies. Had to install gems to get one_gadget

Have to use docker to run the binary

`docker build -t baby_boi_netcat .`
`docker run --rm -p 12345:12345 baby_boi_netcat`


Prints address of printf and uses vulnerable get.

Can use the mem leak to get addr of one shot in libc

used `one_gadget libc-2.27.so` since the buffer is so small