
from selenium import webdriver
from threading import Thread
from datetime import datetime
import signal,sys,time,base64,urllib2
import tornado.ioloop,tornado.web,tornado.options

SERVER_PORT=8787
#BASE_URL='http://localhost:10080/xss/inline?injected_code='
BASE_URL='http://localhost:9999/?xss='
PAYLOADS='payload.dat'
DELAY=3


#Logger
def LOG(data):
	with open('logs.txt','a') as f:
		f.write(data +"\n")

#Marking Timestamp
LOG("Fuzzer Started at : "+ str(datetime.now()))

#Firefox Driver Configuration

fp = webdriver.FirefoxProfile()
fp.set_preference("general.useragent.override","immunio-fuzzer")
fp.update_preferences()
DRIVER=webdriver.Firefox(firefox_profile=fp)

#Exit Fuzzer
is_closing = False
def signal_handler(signum, frame):
    global is_closing
    print "Exiting...!"
    is_closing = True

def try_exit(): 
    global is_closing
    if is_closing:
    	try:
        	DRIVER.quit()
        except:
        	pass
        tornado.ioloop.IOLoop.instance().stop()

#Server Reachable
def Ping(NO,PAYLOAD,BASE_URL):
	try:
		urllib2.urlopen(BASE_URL)
	except urllib2.HTTPError, e:
		print(e)
		pass
	except urllib2.URLError, e:
		DAT = "\n\n[ERROR] Server is not Reachable, Last tried [PAYLOAD]: " + str(NO) +". "+ PAYLOAD+" [URL]: "+BASE_URL+" Error: "+ str(e.args)
		print DAT
		LOG(DAT)
		sys.exit(0)

#Web Driver

def DriverThread(DRIVER,BASE_URL,PAYLOADS,DELAY):
	with open(PAYLOADS,'r') as f:
		payload_collection=f.readlines()
	print "Started Fuzzing\nPress Ctrl + C to Quit"
	count=0
	for payload in payload_collection:
		count+=1
		DAT="No: "+ str(count) +" Data: " +str(payload)
		LOG(DAT)
		try:
			DRIVER.get(BASE_URL+payload)
	    		Ping(count,payload,BASE_URL)
	    		time.sleep(DELAY)
		except Exception as e:
			#print "[ERROR] Selenium - " + str(e)
			pass
	print "Fuzzing Completed"
	DRIVER.quit()
	sys.exit(0)

thread = Thread(target=DriverThread,args=[DRIVER,BASE_URL,PAYLOADS,DELAY])
thread.setDaemon(True)
thread.start()

#CallbackHandler
class MainHandler(tornado.web.RequestHandler):
    def get(self):
    	try:
            b64 = self.get_argument('b64', True)
            DAT="[EXECUTED] Payload Executed: " + base64.b64decode(b64)
            LOG(DAT)
            self.set_header('Access-Control-Allow-Origin', '*')
            self.write(b64)
        except:
            self.write("ERROR")    	


application = tornado.web.Application([
    (r"/", MainHandler),
])

signal.signal(signal.SIGINT, signal_handler)
application.listen(SERVER_PORT)
tornado.options.parse_command_line()
tornado.ioloop.PeriodicCallback(try_exit, 100).start() 
tornado.ioloop.IOLoop.instance().start()


