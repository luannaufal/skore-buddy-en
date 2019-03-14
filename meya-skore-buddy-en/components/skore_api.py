import requests
import json
from log import logger

class Skore():
    def __init__(self, email, password, companyId = "5704", token = ""):
		self.baseUrl = "https://knowledge.skore.io/workspace/"		
		self.companyId = companyId
		self.token = token
		if not self.token: self.login(email, password)

    def query(self, action, method = "GET", parameters = {}, headers = {}, payload = {}):
		# Create request Headers
		queryHeaders = {
			"Content-type": "application/json",
			"Accept": "text/plain"
		}
		if hasattr(self, "token"):
			queryHeaders.update({"Authorization": self.token})
		queryHeaders.update(headers)

		url = self.baseUrl + action

		# Generate request parameters
		request_parameters = {
			"method" : method, 
			"url" : url, 
			"headers" : queryHeaders, 
			"allow_redirects" : False
		}

		# Convert payload to str
		if payload:
			str_payload = json.dumps(payload)
			request_parameters.update({"data" : str_payload})
		
		response = requests.request(**request_parameters)

		return self._checkRequestOutput(response)

    def _checkRequestOutput(self, response):
		print("Request returned with status code {}".format(response.status_code))
		if response.status_code != requests.codes.ok:
			print("Request failed with status {}: {}".format(response.status_code, response.text))
			return False
		try:
			return json.loads(response.text)
		except Exception as e:
			print("Exception found: {}",format(e))
			print("Request Output:", request.text)
			return False
    
    @logger()
    def login(self, email, password):
        action = "v3/login"
        payload = {
        	"email": email,
        	"password": password,
        	"company_id": self.companyId
        }
        print("Requesting login for user {}".format(email))
        response = self.query(action = action, method = "POST", payload = payload)
        if response:
            print("RESPONSE", response)
            self.token = response["token"]
            self.tokenExpiration = response["token_expiration_date"]
        return response

    @logger()
    def getSpaceContents(self, spaceId):
		action = "v2/spaces/{}/contents".format(spaceId)
		print("Requesting contents for spaceId {}".format(spaceId))
		response = self.query(action)
		return response

    @logger()
    def getContentProvision(self, contentId):
		action = "v2/contents/{}/provision".format(contentId)
		print("Requestings extra information from contentId {}".format(contentId))
		response = self.query(action)
		return response
	
    @staticmethod
    def tokenValid(tokenExpiration):
	    import time
	    
	    todayUnix = time.time() * 1000
	    return int(todayUnix) < tokenExpiration
	    
	    
	    
