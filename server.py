import os
import http.server
import socketserver
from urllib.parse import urlparse
from urllib.parse import parse_qs
import requests
from datetime import datetime, timedelta
from dateutil.parser import parse
from multiprocessing import Process

FF_CAL = "https://nfs.faireconomy.media/ff_calendar_thisweek.json"

ICAL_TEMPLATE = """BEGIN:VEVENT
UID:{uid}
DTSTART:{date}
DTEND:{date}
DTSTAMP:{date}
SUMMARY:[{impact}]{country}-{title}
BEGIN:VALARM
ACTION:AUDIO
TRIGGER:-PT2M
END:VALARM
END:VEVENT
"""

ICAL = """BEGIN:VCALENDAR
PRODID:-//eluceo/ical//2.0/EN
VERSION:2.0
CALSCALE:GREGORIAN
{items}
END:VCALENDAR"""


class MyHttpRequestHandler(http.server.SimpleHTTPRequestHandler):
    def do_GET(self):

        presentDate = datetime.now()
        unix_timestamp = datetime.timestamp(presentDate)*1000

        resp = requests.get(url=FF_CAL)
        ff_cal = list(resp.json())
        ff_cal = list(filter(lambda x: x["impact"] == "High" or x["impact"] == "Medium", ff_cal))

        # Sending an '200 OK' response
        self.send_response(200)

        # Setting the header
        self.send_header("Content-type", "application/octet-stream")
        self.send_header("accept-ranges","bytes")

        # Whenever using 'send_header', you also have to call 'end_headers'
        self.end_headers()

        ical = "" 

        item_id = int(unix_timestamp)
        for item in ff_cal:
            c = item.copy()
            item_id = item_id + 1
            c["uid"] = str(item_id)
            parsed_date = parse(c["date"]) + timedelta(hours=-3)            
            c["date"] = (parsed_date.isoformat() + "Z").replace("-04:00Z","").replace("-","").replace(":","")
            ical = ical + ICAL_TEMPLATE.format(**c)
       
        ical_response = ICAL.format(items=ical)

        # Writing the HTML contents with UTF-8
        self.wfile.write(bytes(ical_response, "utf8"))
        
        return


def start_server():
    # Create an object of the above class
    handler_object = MyHttpRequestHandler

    PORT = 8080
    with socketserver.TCPServer(("", PORT), handler_object) as my_server:                
        my_server.serve_forever()        

if __name__ == '__main__':
    start_server()
    print("done")
