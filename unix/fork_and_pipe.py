from os import fork, getpid, pipe, read, write

read_end, write_end = pipe()

child_pid = fork()

if child_pid:
    # parent
    print("parent (pid" + getpid() + ") is about to read")
    data = read(read_end, 1024)
    print("parent read data: ", data)
else:
    # child
    print("child (pid" + getpid() + ") is about to wite")
    write(write_end, "Hello from a forked process")
    print("child is done... existing")
