from http.server import BaseHTTPRequestHandler, HTTPServer  
from urllib.parse import parse_qs
import requests
import urllib.request
import json

class S(BaseHTTPRequestHandler): 
    def _set_headers(self):

        # response code
        self.send_response(200)   

        # response header
        self.send_header('Content-type', 'application/json') 

        # separate a header and a body
        self.end_headers()

    # override do_POST() method in BaseHTTPRequestHandler class
    # this method is called when the post request is made
    def do_POST(self): 

        content_length = int(self.headers['Content-Length'])

        # read request body
        # body : b'{"keyword" : "playground"}'
        body = self.rfile.read(content_length) 

        # query : {'keyword': 'playground'} 
        query = json.loads(body)

        # search all indices
        url = 'http://localhost:9200/_all/_search'

        data = search(url, query["keyword"])

        # sent response
        self._set_headers()

        # if a message text is set, it is written in 'wfile' which covers response socket
        self.wfile.write(data) 

# choose handle when server object is made
def run(server_class=HTTPServer, handler_class=S, port=8080):
    server_address = ('', port)
    httpd = server_class(server_address, handler_class)
    print('Starting http port ' + str(port))

    # if run, the server waits for reqeust by this method
    # when request comes, the server pass information to the registered handler.
    httpd.serve_forever() 

def search(uri, term):

  #curl command example :: localhost:9200/index17/_search?q=playground&size=100000

  headers ={'Content-Type' : 'application/json'} 
  keyWordSearch = {'q' : term, 'size' : 2, '_source' : ['title', 'link']}
  response = requests.get(uri, headers = headers, params = keyWordSearch)

  results = json.loads(response.text)

  return results

if __name__ == "__main__":
    from sys import argv

    if len(argv) == 2:
        run(port=int(argv[1]))
    else:
        run()
