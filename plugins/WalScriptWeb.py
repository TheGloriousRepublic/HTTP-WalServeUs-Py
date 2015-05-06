#import

runtime={}

def main(toparse, dat):
    global runtime
    runtime=dict(dat)
    return run(toparse)

def evalarg(a):
    global runtime
    for x in runtime:
        a=a.replace('$'+x+'$',str(runtime[x]))

    a=eval(a, {'__builtins__':None})
    return a

def getcommand(c):
    c=c.split('}')
    return c[0]

def getargs(c):
    c=c.split('}')
    args = c[1:-1]
    for x in range(len(args)):
        if args[x][0]=='{':
            args[x]=args[x][1:]
            args[x]=evalarg(args[x])
    return args

def run(script, mode='main'):
    global runtime
    head=''
    body=''
    script=script.split(';')[:-1]
    i=0
    while not getcommand(script[i]) == 'send':
        c=getcommand(script[i])
        a=getargs(script[i])

        if c == 'echo': #Append to file
            body+=''.join(a)
            
        elif c == 'load': #Load a file
            if a[0].split('.')[-1] == 'wsw':
                head+=run(open(a[0]).read(), mode='recursive')[0]
                body+=run(open(a[0]).read(), mode='recursive')[1]
            elif a[0].split('.')[-1] == 'css':
                body+='<style>'+open(a[0]).read()+'</style>'
            elif a[0].split('.')[-1] == 'js':
                body+='<script>'+open(a[0]).read()+'</script>'
            else:
                body+=+open(a[0]).read()
        
        elif c == 'var': #Save a variable
            runtime[a[0]]=''.join(a[1:])
            
        elif c == 'print': #Print to console
            print(''.join(a))
        i+=1

        elif c == '':
            pass
        
    if mode == 'main':
        return '<head>'+head+'</head><body>'+body+'</body>'
    elif mode == 'recursion':
        return [head, body]
