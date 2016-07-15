#-------------------------------------------------------------------------------
# Name:        main
# Purpose:
#
# Author:      m.j_banitaba
#
# Created:     14/07/2016
# Copyright:   (c) User 2016
# Licence:     <your licence>
#-------------------------------------------------------------------------------
import BaseHTTPServer
import subprocess
import traceback
import os
class HTTPHandler(BaseHTTPServer.BaseHTTPRequestHandler):
    cgi_path="./cgi/cgi_demo.py"
    web_path="/www"
    def get_environment(self):
        env=os.environ
        env['PATH_INFO']=self.path.replace("/",os.sep).replace("\\",os.sep)
        env['SERVER_PORT']=''
        env['SERVER_ADDR']=''
        env['SERVER_NAME']=''
        env['SERVER_SOFTWARE']=''
        env['ALL_HTTP']=''
        env['URL']=''
        env['PATH_TRANSLATED']=''
        env['SCRIPT_NAME']=''
        env['DOCUMENT_ROOT']=self.web_path.replace("/",os.sep).replace("\\",os.sep)
        return env
    def get_message(self):
        p=subprocess.Popen(['C:\Python27\python.exe',self.cgi_path],shell=True,
                           stdout=subprocess.PIPE,
                           stderr=subprocess.PIPE,
                           env=self.get_environment())
        out, err = p.communicate()
        if err :
            raise Exception(err)
        return out
    def do_GET(self):
        print self.headers
        print self.command
        print self.path
        print self.protocol_version

        try:
            message=self.get_message()
            self.send_response(200)
##            self.end_headers()
            self.wfile.write(message)
        except :
            traceback.print_exc()
            self.send_error(500)
            return
        pass
    pass
def main():
    pass

if __name__ == '__main__':
    main()
