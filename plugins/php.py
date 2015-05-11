import pyphp.executer
import StringIO

def main(script, args=None):
    stdout = StringIO.StringIO()

    pyphp.executer.execute_php(script, stdout=stdout)

    return repr(stdout.getvalue())
