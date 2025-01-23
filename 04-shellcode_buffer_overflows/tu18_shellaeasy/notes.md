Executable stack, 32 bits

Has a small custom stack canary. 0xcafebabe

Need to replace it with 0xdeadbeef to make it to ret

Uses vulnerable gets function to a 64 byte buffer

Leaks addr of the buffer