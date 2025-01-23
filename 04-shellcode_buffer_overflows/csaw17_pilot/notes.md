Executable stack, 64 bit

vulnerable buffer, reads 0x40 into 32 byte buf. Prints addr of the stack, hints shellcode


`objdump -D -b binary -m i386:x86-64 -M intel shellcode.bin`