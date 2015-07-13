import pyphp.executer
import pyphp.phparray
import cStringIO

def main(script, args={}):
    phpcode=script

    stdout=cStringIO.StringIO()

    a = [(x, args[x]) for x in args]
    phpglobals={
        "$_GET" : pyphp.phparray.PHPArray(*a)
    }
    
    pyphp.executer.execute_php(phpcode, phpglobals, stdout=stdout)

    return stdout.getvalue()

if __name__=='__main__':
    print(main(open(raw_input().split()[0]).read()))
    raw_input()
