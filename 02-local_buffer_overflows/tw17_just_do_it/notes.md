binary crashed on started up. Ran strace, it needed a flag file present

Vulnerable buffer, reads 0x20 bytes into a 16 bytes buffer.

Binary asks for the password P@SSWORD but that fails to solve the challenge

We can't reach ip so no RCE but there is no pie and we have access to the output so we can overwrite the return message with the flag addr since its static


Flag lives at 0x0804a080