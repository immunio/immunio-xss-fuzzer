
from selenium import webdriver
from threading import Thread
from datetime import datetime
import signal,sys,time,base64
import tornado.ioloop,tornado.web,tornado.options


SERVER_PORT=8787
BASE_URL='http://127.0.0.1:9999/?xss='
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
#Web Driver

def DriverThread(DRIVER,BASE_URL,PAYLOADS,DELAY):
	with open(PAYLOADS,'r') as f:
		payload_collection=f.readlines()
	print "Started Fuzzing\n Press Ctrl + C to Quit"
	count=0
	for payload in payload_collection:
		count+=1
		DAT="No: "+ str(count) +" Data: " +str(payload)
		LOG(DAT)
		#print DAT
		try:
			DRIVER.get(BASE_URL+payload)
			time.sleep(DELAY)
		except Exception as e:
			print "[ERROR] Selenium - " + str(e)
			pass
	print "Fuzzing Completed"
	DRIVER.quit()

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


