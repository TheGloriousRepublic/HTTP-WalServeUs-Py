#import

runtime={}

def main(toparse, dat):
    runtime=dat
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
    global runtime
    content=''
    script=script.split(';')[:-1]
    i=0
    while not getcommand(script[i]) == 'send':
        c=getcommand(script[i])
        a=getargs(script[i])
        if c == 'echo':
            content+=''.join(a)
        elif c == 'load':
            if a[0].split('.')[-1] == 'wsw':
                content+=run(open(a[0]).read())
            elif a[0].split('.')[-1] == 'css':
                content+='<style>'+open(a[0]).read()+'</style>'
            elif a[0].split('.')[-1] == 'js':
                content+='<script>'+open(a[0]).read()+'</script>'
            else:
                content+=+open(a[0]).read()
        elif c == 'var':
            runtime[a[0]]=''.join(a[1:])
        elif c == 'print':
            print(''.join(a))
        i+=1
    return content
