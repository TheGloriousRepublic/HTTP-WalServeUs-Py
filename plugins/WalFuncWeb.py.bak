directory=''
prompt='prelude'

functionStructure = {
    'commandname': {
        'args':['Arguments'],
        'value': {
            'case1':'return for case 1',
            'case2':'return for case 2'
            }
        }
    }

functionsbase = {
    'else': {
        'args':[],
        'value': {
            'True':'True'
            }
        }
    }

functions = functionsbase

def main(toparse, dat):
    for x in dat:
        functions[x]={'args':[],'value':{'True':dat[x]}}
    build(toparse)
    return evalcom('#content}#')

def throw(t,e):
    print('Error: '+t+': '+e)
    while 1:
        pass
    
def isconst(v):
    if (v[0]=='"' and v[-1]=='"') or (v[0]=='\'' and v[-1]=='\''):
        return True
    else:
        try:
            int(v)
            return True
        except:
            return False
        

def evalexp(exp):
    while '#' in exp:
        s=exp.find('#')
        e=exp.find('#', s+1)
        exp=exp[:s]+str(evalfunc(exp[s:e+1]))+exp[e+1:]
    return eval(exp)#, {'__builtins__': [True,False]})

def evalfunc(func):
    func=func.strip('#')
    func=func.split('}')[:-1]
    arg=func[1:]
    com=func[0]
    for x in range(len(arg)):
        arg[x]=evalexp(arg[x])

    farg = functions[com]['args']

    argmap={}
    for x in range(len(farg)):
        argmap['$'+farg[x]+'$']=arg[x]
    for key in functions[com]['value']:
        pseudokey=key
        for x in argmap:
            pseudokey = pseudokey.replace(x, str(argmap[x]))
            
        if evalexp(pseudokey)==True:
            exp=functions[com]['value'][key]
            break

    for x in argmap:
        exp = exp.replace(x, str(argmap[x]))

    return(evalexp(exp))

def evalcom(com):
    global directory, prompt
    if com[0]==':':
        com = com[1:]
        args=com.split(' ')[1:]
        com=com.split(' ')[0]
        #if com=='type' or com == 't':
        #    return type(args[0])
        if com == 'cd':
            directory=args[0].replace('\\','/')
            if directory[-1]!='/':
                directory=directory+'/'
            return('Directory changed to '+directory)
        elif com == 'load' or com == 'l':
            build(open(directory+args[0]).read().replace('/n','').replace('/t',''))
            prompt='main*'
            return('File '+directory+args[0]+' loaded')
        elif com == 'unload' or com == 'u':
            functions=functionsbase
            prompt = 'prelude'
            return('All modules unloaded')
        elif com == 'tests':
            evalcom(':cd C:/Users/Nathan/Desktop/Programming/WalrusOS/WalFunc/Tests/')
            return('To Tests!')
        else:
            return('Unrecognized command')
    else:
        return evalfunc('#'+com.strip('#')+'#')

def build(c):
    c=c.replace('\n', '').replace('\t', '')
    c=c.split(';')[:-1]
    for x in c:
        x=x.split(':=')
        com=x[0].split('}')[0]
        arg=x[0].split('}')[1:-1]
        x[1]=x[1].split(',')
        for i in range(len(x[1])):
            x[1][i]=x[1][i].split(':')

        if not com in functions:
            functions[com]={}
            functions[com]['args']=arg
            functions[com]['value']={}

            for i in range(len(x[1])):
                functions[com]['value'][x[1][i][0]]=x[1][i][1]
