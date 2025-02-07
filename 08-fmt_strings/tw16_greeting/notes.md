32 bit intel dynamic

No relro, canary, nx, no pie

controlled printf vuln. Don't see anything useful to overwrite or read

User inputs on the stack starts at 12.5. Need to write an initial 2 bytes before writing actual payload.


Key is to use the fini_array. An array of destructor function can be complied into the code. That is hint with the use of the init_array to use libc

For details https://docs.oracle.com/cd/E19120-01/open.solaris/819-0690/chapter2-48195/index.html


To develope the exploit, overwrite finit array with a loop back to main that is stable (this will take guess and check). Then overwrite a function candidate to run system. 

Best candidate is strlen() since it take the raw null terminated user input