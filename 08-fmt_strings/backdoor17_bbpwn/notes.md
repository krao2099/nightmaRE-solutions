32 bit intel dynamic

partial relro, no canary, no pie, NX

Takes one string as input and prints it. Format string vuln. No buffer overflow

Since relro is partial and we have no control of eip we can overwrite GOT to get code execution. Last function to be called is fflush

We need to overwrite fflush with flag() to print the flag at 0x804870b. Use $n

Use $ style to print specific things off the stack. Guess and check

`echo "1111.%10\$x" | ./32_new` Found my input at stack offset 10

fflush is at 0x0804a028 `objdump -R 32_new | grep fflush`