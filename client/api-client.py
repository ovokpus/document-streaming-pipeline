import linecache
import json
import requests


def run():
    i = 1
    end = 50
    
    while i <= end:
        # read a specific line
        line = linecache.getline("./data/output.txt", i)
        
        print(line)
        
        # write line to the API
        jsonline = json.loads(line)
        
        print(jsonline)
        
        response = requests.post("http://localhost:80/invoiceitem", json=jsonline)
        
        print("status_code", response.status_code)
        print("Printing Entire Post Request")
        print(response.json())
        
        # increment the counter
        i += 1

if __name__ == '__main__':
    run()