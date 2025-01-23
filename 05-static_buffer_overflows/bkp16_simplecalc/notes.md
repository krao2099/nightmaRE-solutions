64 bit, statically linked

no pie, no canary

Number of calc must be between 3 and 0x100

Vulnerable buffer 40 bytes. Can write up to 0x99 * 4 bytes to it

buffer is 0x48 bytes away from rip. ROP needed

Need to make execve call so

rax = 0x3b, rdi -> /bin/sh\x00, rsi = 0x0, rdx, 0x0

`sudo -H python3 -m pip install ROPgadget`