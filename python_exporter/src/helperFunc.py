import requests
from urllib3.exceptions import InsecureRequestWarning
import json
import sys
import os


def getToken(url, login, password):
  endpoint = url
  data = {"username":login, "password":password}
  headers = {'Content-Type' : 'application/x-www-form-urlencoded' }

  p = requests.post(endpoint, data=data, headers=headers, verify='/app/certs/nifi-cert.pem')

  print('===============', resp, file=sys.stderr)
  
  if p.status_code == 201:
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