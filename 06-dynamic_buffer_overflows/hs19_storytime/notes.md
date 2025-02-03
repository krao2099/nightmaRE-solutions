64 bit, nx. No pie, no canary, Perfect for stack leak and rop chain. NO relro

Scans 400 bytes into a 48 byte buffer, then returns. 56 bytes to rip

Symbols in binary (write and read). Use write to leak glibc to combat alsr

write: rdi 0x1 (stdout), rsi GOT(write), rdx >=0x8 

`ROPgadget --binary storytime | grep rsi`

`one_gadget libc.so.6`

Useful function, end(). Calls write. Can use parts of it to leak write()

`./ld-2.23.so --library-path /home/cheerierflame/development/nightmaRE-solutions/06-dynamic_buffer_overflows/hs19_storytime ./storytime`

`gdb --args ./ld-2.23.so --library-path /home/cheerierflame/development/nightmaRE-solutions/06-dynamic_buffer_overflows/hs19_storytime ./storytime`

`docker build -t storytime_netcat . && docker run --rm -p 12345:12345 storytime_netcat`

Use a script to launch with LD preload