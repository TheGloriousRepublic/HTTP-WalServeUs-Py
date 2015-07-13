from pyphp import executer
from pyphp import phparray
import io

def main(script, args={}):
    phpcode=script

    stdout=io.StringIO()

    a = [(x, args[x]) for x in args]
    phpglobals={
        "$_GET" : phparray.PHPArray(*a)
    }
    
    executer.execute_php(phpcode, phpglobals, stdout=stdout)

    return stdout.getvalue()

if __name__=='__main__':
    print((main(open(input().split()[0]).read())))
    input()
