import time
from zapv2 import ZAPv2
import hmac
import hashlib

apikey = 'CHANGEME'
SLEEP_INTERVAL = 1
# A breakpoint is specified by the following arguments
#     string: Any,
#     location: Any,
#     match: Any,
#     inverse: Any,
#     ignorecase: Any,
#     apikey: str = ''
BREAKPOINTS = [("[a-zA-Z.]{0,}example\.com","url","regex",False,False)]


zap = ZAPv2(apikey=apikey, proxies={'http': 'http://127.0.0.1:8081', 'https': 'http://127.0.0.1:8081'})
# break on both request and response
zap.brk.brk("http-all",True)
zap.brk.set_http_message
for breakpoint in BREAKPOINTS:
    zap.brk.add_http_breakpoint(*breakpoint)

# Read some value, apply some function, write some value
isDone = False
while(not isDone):
    if(data := zap.brk.http_message):
        # let say you want to:
        # 1. append some data in the request body
        # 2. generate a HMAC for the request body
        # 3. add a custom header with the value of the HMAC
        modified_body = data.split('\r\n\r\n')[1] + 'igotoschoolbybus'
        some_value = hmac.new(
            bytes('Inevitable', 'utf-8'), 
            msg=bytes(modified_body, 'utf-8'), 
            digestmod=hashlib.sha256
        ).hexdigest()
        modified_headers = data.split('\r\n\r\n')[0] + f'\nX-Means-Of-Transportation: {some_value}'
        zap.brk.set_http_message(modified_headers,modified_body)
        zap.brk.step()
        time.sleep(SLEEP_INTERVAL)
        resp = zap.brk.http_message
        print("Modified request headers:\n{}\n\nResponse: {}".format(modified_headers,resp.split('\r\n\r\n')[0].split('\n')[0]))
        zap.brk.cont()
        isDone = True
    time.sleep(SLEEP_INTERVAL)

for breakpoint in BREAKPOINTS:
    zap.brk.remove_http_breakpoint(*breakpoint)

