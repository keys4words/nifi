import requests
from urllib3.exceptions import InsecureRequestWarning
import json
import sys
import os


def run_script(script, stdin=None):
    """Returns (stdout, stderr), raises error on non-zero return code"""
    import subprocess
    # print('===============', str(script), file=sys.stderr)
    proc = subprocess.Popen(['bash', '-c', script],
        stdout=subprocess.PIPE, stderr=subprocess.PIPE,
        stdin=subprocess.PIPE)
    stdout, stderr = proc.communicate()
    if proc.returncode:
        raise ScriptException(proc.returncode, stdout, stderr, script)
    return stdout

class ScriptException(Exception):
    def __init__(self, returncode, stdout, stderr, script):
        self.returncode = returncode
        self.stdout = stdout
        self.stderr = stderr
        Exception().__init__('Error in script')


def getToken(url, login, password):
  endpoint = url
  data = f"username={login}&password={password}"
  headers = "Content-Type: application/x-www-form-urlencoded"
  script = f"curl -d '{data}' -H '{headers}' -X POST {endpoint} --insecure"
  token = run_script(script)
  # p = requests.post(endpoint, data=data, headers=headers, verify='/app/certs/nifi-cert.pem')
  return str(token, "utf-8")

def getHeaders(token):
  headers = {}
  if token != None:
    headers = {'Authorization': "Bearer " + str(token)}
  return headers

def getCluster(url, token):
  headers = getHeaders(token)

  response = requests.get(url, headers=headers, verify=False)
  #logger.debug( response.text)
  jData = json.loads(response.text)
  return jData['cluster']['nodes']
  

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