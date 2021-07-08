from http.server import BaseHTTPRequestHandler,HTTPServer
import json,os
from colorama import Fore,init
init(autoreset=True)

print(Fore.CYAN+" _   _       _\n\
| | | | __ _| |_ ___  __ _\n\
| |_| |/ _` | __/ __|/ _` |\n\
|  _  | (_| | |_\__ \ (_| |\n\
|_| |_|\__,_|\__|___/\__,_|\n")

class config:
     file=None
     configObj=None
     hostName="0.0.0.0"
     with open("server.json") as file:
          configObj=json.load(file)
          port=configObj["serverConfig"]["port"]
          pageNotFound=configObj["errorPages"]["404"]
          internalErro=configObj["errorPages"]["500"]
          urlsFile=configObj["urlsFile"]
          varsFile=configObj["variables"]

varsFileNew=open(config.varsFile).readlines()
Lines=len(varsFileNew)
cLines=0
varList=[]
while cLines!=Lines:
	var=varsFileNew[cLines].split(" => ")
	varList.append(var[0].replace("\n",""))
	cLines=cLines+1
urlsFileNew=open(config.urlsFile).readlines()
Lines=len(urlsFileNew)
cLines=0
urlList=[]
while cLines!=Lines:
	url=urlsFileNew[cLines].split(" => ")
	urlList.append(url[0].replace("\n",""))
	cLines=cLines+1

class MyServer(BaseHTTPRequestHandler):
     def log_message(self,format,*args):
          url=str(args[0])
          url=url+" "*(30-len(url))
          claddr=str(self.client_address[0])+":"+str(self.client_address[1])
          claddr=claddr+" "*(25-len(claddr))
          print(Fore.CYAN+"--> "+str(url)+" | "+str(args[1])+" | "+str(claddr)+" | "+self.log_date_time_string())

     def readFile(self,path:str):
          fin=open(path.replace("\n",""))
          content=fin.read()
          fin.close()
          for var in varList:
               if var in content:
                    varsFileNew=open(config.varsFile).readlines()
                    Lines=len(varsFileNew)
                    cLines=0
                    while cLines!=Lines:
                         varsmap=varsFileNew[cLines].split(" => ")
                         if var==varsmap[0]:
                              content=content.replace("{["+str(varsmap[0])+"]}",str(varsmap[1]))
                              break
                         cLines=cLines+1
          return content

     def do_GET(self):
          try:
               if self.path in urlList:
                    urlsFileNew=open(config.urlsFile).readlines()
                    Lines=len(urlsFileNew)
                    cLines=0
                    while cLines!=Lines:
                         urlmap=urlsFileNew[cLines].split(" => ")
                         if self.path==urlmap[0]:
                              urlpath=urlmap[1]
                              self.send_response(200)
                              self.send_header("Content-type","text/html")
                              self.end_headers()
                              self.wfile.write(bytes(self.readFile(urlpath),"utf-8"))
                              break
                         cLines=cLines+1
               else:
                    self.send_response(404)
                    self.send_header("Content-type","text/html")
                    self.end_headers()
                    self.wfile.write(bytes(self.readFile(config.pageNotFound),"utf-8"))
          except Exception as e:
               print(Fore.CYAN+"---> Internal Server Error: \""+str(e)+"\"...")
               self.send_response(500)
               self.send_header("Content-type","text/html")
               self.end_headers()
               self.wfile.write(bytes(self.readFile(config.internalErro),"utf-8"))

if __name__=="__main__":
     webServer=HTTPServer((config.hostName,config.port),MyServer)
     print(Fore.CYAN+"-> Server Started on Port %s."%(config.port))
     try:
          webServer.serve_forever()
     except KeyboardInterrupt:
          webServer.server_close()
          print(Fore.RED+"-> Server Stopped.")
          os._exit(1)
