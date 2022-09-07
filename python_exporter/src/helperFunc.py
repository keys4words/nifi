import requests
from requests.adapters import HTTPAdapter
from requests.exceptions import ConnectionError
import json
import sys
import os


def getToken(url, login, password):
  endpoint = url
  data = {"username": "admin", "password": "superpupersecret"}
  headers = {'Accept-Encoding': 'gzip, deflate, br', 'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8', 'Accept': '*/*' }

  # adapter = HTTPAdapter(max_retries=1)
  # session.mount(url, adapter)
  # try:
  #   p = session.post(url, data=data, headers=headers, verify=False, cookies=None)
  # except ConnectionError as ce:
  #   print("=====getTokenError=====" + str(ce), file=sys.stderr)
  #   return None
  endpoint = 'https://localhost:8443/nifi-api/access/token'

  session = requests.Session()
  session.verify = False
  session.trust_env = False
  os.environ['CURL_CA_BUNDLE']="" # or whaever other is interfering with 
  p = session.post(url=endpoint, data=data)
  # p = requests.api.request('post', endpoint, data=data, headers=headers, json=None, verify=False)
  
  if p.status_code == 201:
    print(p.text, file=sys.stderr)
    return p.text
  else:
    return p

def getHeaders(token):
  headers = {}
  if token != None:
    headers = {'Authorization': "Bearer {" + str(token) + "}" }
  return headers

def getCluster(session, url, token):
  headers = getHeaders(token)

  adapter = HTTPAdapter(max_retries=1)
  session.mount(url, adapter)
  try:
    response = session.get(url, headers=headers, verify=False)
    jData = json.loads(response.text)
    return jData['cluster']['nodes']
  except ConnectionError as ce:
    return ce
  

def convertStatus(status):
  if status == 'CONNECTED':
    return 1
  else:
    return 0

def getFlow( url, token ):
  headers = getHeaders(token)
  response = requests.get(url, headers=headers, verify=False)
  jData = json.loads(response.text)
  return jData['controllerStatus']

def about(url , token):
  headers = getHeaders(token)
  response = requests.get(url, headers=headers, verify=False)
  jData = json.loads(response.text)
  return jData['about']

def getProcessorFlow(url,token):
  headers = getHeaders(token)
  response = requests.get(url, headers=headers, verify=False)
  jData = json.loads(response.text)
  return jData['processGroups']