#This software is licensed under the Glorious Republic's Glorious Free Software License 1.0. Just in case you were wondering.
import Tkinter, BaseHTTPServer, cgi, socket, os, sys, datetime, atexit, re, mimetypes, socket

from plugins import *

pcodes = {      '0A':'\n',
                '0D':'\n',
                '20':' ',
                '21':'!',
                '22':'"',
                '23':'#',
                '24':'$',
                '25':'%',
                '26':'&',
                '27':'\'',
                '28':'(',
                '29':')',
                '2A':'*',
                '2B':'+',
                '2C':',',
                '2D':'-',
                '2E':'.',
                '2F':'/',
                '3A':':',
                '3B':';',
                '3C':'<',
                '3D':'=',
                '3E':'>',
                '4F':'?',
                '40':'@',
                '5B':'[',
                '5C':'\\',
                '5D':']',
                '5E':'^',
                '5F':'_',
                '60':'`',
                '7B':'{',
                '7C':'|',
                '7D':'}',
                '7E':'~'
    }

settings = {}
rw = {}
processors = {}
sub = {}

serveAsPlaintext = ['text','application']

def loadConfig(): #Open configuration files and save their options to settings
    for root, dirs, files in os.walk('config/settings/'): #Open all files in config directory
        for f in files:
            if f.endswith('.cfg'):
                for x in open('config/settings/'+f).read().split('\n'): #Separate lines in file and iterate
                    if not x[0]=='#':
                        settings[x.split('=')[0]]=x.split('=')[1] #Set the option before the equal sign in the config file line to the value in the settings dict
                    
    for root, dirs, files in os.walk('config/rewriter/'):
        for f in files:
            if f.endswith('.cfg'):
                for x in open('config/rewriter/'+f).read().split('\n'):
                    if not x[0]=='#':
                        rw[x.split('=')[0]]=x.split('=')[1]

    for root, dirs, files in os.walk('config/processors/'):
        for f in files:
            if f.endswith('.cfg'):
                for x in open('config/processors/'+f).read().split('\n'):
                    if not x[0]=='#':
                        processors[x.split('=')[0]]=x.split('=')[1]

    for root, dirs, files in os.walk('config/subdomains/'):
        for f in files:
            if f.endswith('.cfg'):
                for x in open('config/subdomains/'+f).read().split('\n'):
                    if not x[0]=='#':
                        sub[x.split('=')[0]]=x.split('=')[1]

def dictMerge(x, y):
    '''Given two dicts, merge them into a new dict as a shallow copy.'''
    z = x.copy()
    z.update(y)
    return z

def log(dat): #Print to console and save to log
    o='['+str(datetime.datetime.now())+'] '+str(dat)+'\n'
    b=open(settings['lgdir']+'/server.log', 'r+').read() #Retrieve current log
    open(settings['lgdir']+'/server.log', 'w+').write(b+o+'\n\n') #Write a concatenation of old log and new log to log
    print(o)

class webServer(BaseHTTPServer.BaseHTTPRequestHandler): #Main handler class
    def wfileclear(self):
        self.wfile=''

    def send_error(self, code, message=None):
        self.send_response(code)#, message)
        self.send_header("Content-Type", self.error_content_type)
        
        self.end_headers()
            
    def gendat(self):
        global connected, visitors, individualvisitors
        return {'command':self.command,
                'path':self.path,
                'interpretedpath':self.getPath(),
                'clientip':self.client_address[0],
                'clientport':self.client_address[1],
                #'connected':connected,
                'visitors':visitors,
                'individualvisitors':individualvisitors
            }

    def extractVars(self):
        if len(self.path.split('?')) >= 2:
            r={}
            v=self.path.split('?')[-1] #Get the query
            v=v.split('&') #Separate them

            for x in range(len(v)):
                v[x]=v[x].split('=') #Separate the ~~Boys from the Men~~ variable names from the values
            for x in v:
                r[x[0]]=self.psub(x[1])

            self.path=self.path.split('?')[0]
            return r
        else:
            return {}

    def log_message(*args):
        pass

    def logCommand(self):
        log(self.client_address[0]+' on port '+str(self.client_address[1])+' to '+self.headers['host']+': \''+self.command+' '+self.path+'\', interpreted as \''+self.command+' '+self.getPath()+'\'') #Log the time and client address/client port of a request, followed by the request submitted and what it was interpreted to.

    def logConnected(self):
        global connected, visitors, individualvisitors
        if not self.client_address[0] in connected:
            if not self.headers.get('DNT') or self.headers.get('DNT')==None: #Respect Do Not Track requests
                connected+=self.client_address[0]
            individualvisitors+=1
        visitors+=1

    def getPath(self):
        p=self.path
        if p.endswith('/'):
            p=self.path[:-1]
        for x in rw:
            if re.match(x, p):
                p=rw[x]
                break
        return(p)

    def psub(self, s):
        for x in pcodes:
            s=s.replace('%'+x, pcodes[x])
        return(s)
            
    def do_HEAD(self):
        self.logCommand()
        self.sendHeader()
        
    def sendHeader(self):
        p=self.getPath()
        self.logConnected()
        self.send_response(200)
        self.send_header('Content-type', mimetypes.guess_type(p)[0])
        self.end_headers()


    def do_GET(self):
        a=self.extractVars()
        p=self.getPath()
        self.logCommand()
        ext=p.split('.')[-1]
        self.sendHeader()
        m=dictMerge(self.gendat(), a)
        if os.path.isfile(settings['pgdir']+'/'+p):
            if ext in settings['pgexr'].split('|') or ('*' in settings['pgexr'].split('|') and mimetypes.guess_type(p)[0].split('/')[0] in serveAsPlaintext):
                content=open(settings['pgdir']+'/'+p).read()
                if ext in processors:
                    content=eval(processors[ext]+'.main(\''+content.replace('\n','').replace('\t','')+'\', '+str(m).replace('\'','"')+')')
                self.wfile.write(content)

            elif ext in settings['pgexb'].split('|') or ('*' in settings['pgexb'].split('|') and not (mimetypes.guess_type(p)[0].split('/')[0] in serveAsPlaintext)):
                content=open(settings['pgdir']+'/'+p,'rb').read()
                if ext in processors:
                    content=eval(processors[ext]+'.main(\''+content.replace('\n','').replace('\t','')+'\', \''+str(dictMerge(self.gendat(),a)).replace('\'','"')+'\')')
                self.wfile.write(content)
                
            elif os.path.isfile(settings['erdir']+'/403.html'):
                content=open(settings['erdir']+'/403.html').read()
                self.wfile.write(content)
                
            else:
                self.send_response(403)
                self.wfile.write('<center><h1>Error 403</h1><h2>You are forbidden to access this file on this server</h2>Furthermore, no 403.html file was found in the local server\'s error directory</center>')
                
        elif os.path.isfile(settings['erdir']+'/404.html'):
            #self.send_response(404)
            content=open(settings['erdir']+'/404.html').read()
            self.wfile.write(content)
            
        else:
            self.send_response(404)
            self.wfile.write('<center><h1>Error 404</h1><h2>File not found</h2>Furthermore, no 404.html file was found in the local server\'s error directory</center>')

    def do_POST(self):
        p=self.getPath()
        self.logCommand()
        ctype, pdict = cgi.parse_header(self.headers.getheader('content-type'))
        if ctype == 'multipart/form-data':
            print(self.rfile)
            query=cgi.parse_multipart(self.rfile, pdict)
        
        self.send_response(301, '')
        self.end_headers()
        self.fileContent=query.get('upfile')[0]
        if len(self.fileContent)<=8192: #Check maximum POSTed file size
            open(settings['rcdir']+'/'+str(datetime.datetime.now()).replace(':', '.')+'.txt', 'w+').write(self.fileContent) #record POSTed files
        else:
            log('File too large to record (>'+int(settings['rcmax'])+'b)')

    def do_OPTIONS(self):
        self.sendHeaders()
        op=dir(self)
        o=[]
        for method in dir:
            if method[:2]=='do_':
                self.wfile.write(method[2:]+' ')
    def do_KILL(self):        
        #gracefulShutdown()
        pass

    def run(self):
        while True:
            loadConfig() #load configuration files
            handle_request()

def gracefulShutdown():
    global s
    log('Server stops')
    s.server_close
    c='\n'.join(connected)
    f=open(settings['lgdir']+'/connected.log', 'w+')
    f.write(c)
    f=open(settings['lgdir']+'/visitorcount.log', 'w+')
    f.write(str(individualvisitors))
    f.close()

def serve():
    log('Server starts')
    try:
        s.serve_forever()
    except:
        pass

#class interface(Tkinter.Tk):
    #pass

loadConfig() #load configuration files

connected=list(open(settings['lgdir']+'/connected.log', 'w+').read().split('\n')) #Retrieve list of connected IPs
visitors=0#int(open(settings['lgdir']+'/visitorcount.log').read()) #Retrieve number of connectors
individualvisitors=len(connected) #Get number of unique connectors

atexit.register(gracefulShutdown) #Record logs at shutdown

if __name__ == '__main__':
    s = BaseHTTPServer.HTTPServer(('', int(settings['port'])), webServer)
    #print(s)
    serve()
