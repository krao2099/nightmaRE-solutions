32 bit, intel, dynamic

relro, no canary, nx, no pie,

Repeated loop of reading and printing string. From ghidra I know the flag is on the stack

No real function call to overwrite except fgets but I would need a one shot libc gadget

No shell just print flag. Repeat %?$s until I get something

`%8$s` worked. Could have optimize with gdb or ghidra