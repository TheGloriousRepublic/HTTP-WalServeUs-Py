def main(toparse):
    return run(toparse)

def evalarg(a):
    pass

def getcommand(c):
    c=c.split('}')
    return c[0]

def getargs(c):
    c=c.split('}')
    args = c[1:-1]
    for x in range(len(args)):
        if args[x][0]=='{':
            args[x]=args[x][1:]
            evalarg(args[x])
    return args

def run(script):
    content=''
    script=script.split(';')[:-1]
    i=0
    while not getcommand(script[i]) == 'end':
        c=getcommand(script[i])
        a=getargs(script[i])
        if c == 'echo':
            content+=''.join(a)
        elif c == 'print':
            print(''.join(a))
        i+=1
    return content
