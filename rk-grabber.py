import json, requests
from selectolax.parser import HTMLParser
import argparse

parser = argparse.ArgumentParser(description='Get Google Drive Resource Keys')
parser.add_argument('URL', metavar='URL', type=str,
                    help='drive URL to access, points to file or folder')


args = parser.parse_args()
URL = args.URL

#URL = "https://drive.google.com/drive/folders/0B19OoIC31UN0eUE4OERjSXYxcUE"
#resourcekey=0-5kInovIu-ZcFFXgTcW--XA

#URL = "https://drive.google.com/drive/u/0/folders/0B3L0CT834bhTYU11bGFVMVFaeFU"
#resourcekey = 0-oz8necicakxBrwXbyx5aVA

#URL = "https://drive.google.com/file/d/0B4p1SsI5fon7NFVGc1I0MG03S1k"
#resourcekey=0-5uPdMmBQSeblPymyp6QkKg

resp = requests.get(URL)
HTMLtree = HTMLParser(resp.text)
#FOLDER ROUTINE
if '/folders/' in URL: 
    #print(HTMLtree.css('html > body > script'))
    HTMLtarget = HTMLtree.css('html > body > script')[12].text()
    HTMLtarget = HTMLtarget[HTMLtarget.find('{'):]
    HTMLtarget = HTMLtarget[:HTMLtarget.rfind('}')+1]
    JSONtarget = HTMLtarget.replace('key','"key"').replace('isError','"isError"').replace('hash','"hash"').replace('data','"data"').replace('sideChannel','"sideChannel"').replace("'",'"')
    JSONtree = json.loads(JSONtarget)
    Treasure = JSONtree['data'][-2][-1]
if '/file/' in URL:
    HTMLtarget = HTMLtree.css('html > head > script')[0].text()
    HTMLtarget = HTMLtarget[HTMLtarget.find('{'):]
    HTMLtarget = HTMLtarget[:HTMLtarget.rfind('};')+1]
    JSONtarget=HTMLtarget.replace("'",'"')
    #print(JSONtarget)
    JSONtree = json.loads(JSONtarget)
    Treasure = JSONtree['info_params']['resourcekey'][1]

try:
    print(Treasure)
except Exception as e:
    print("Unable to find resource key.")
    print(e)
