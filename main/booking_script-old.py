import requests
from lxml import htm


USERNAME = "11988401"
PASSWORD = "code2@learn"


LOGIN_URL = "https://sso.lib.uts.edu.au/cas/login?service=https%3A%2F%2Fwww.lib.uts.edu.au%2Froombooking%2F%3F_casCheck%3Dtrue"
URL = "https://www.lib.uts.edu.au/roombooking/bookings#20"
BOOKING_URL = "https://www.lib.uts.edu.au/roombooking/bookings/create"



def main():

	# begin session requests
	session_requests = requests.session()
	result = session_requests.get(LOGIN_URL)
	tree = html.fromstring(result.text)

	# get hidden login tokens
	execution_token = list(set(tree.xpath("//input[@name='execution']/@value")))[0]
	lt_token = list(set(tree.xpath("//input[@name='lt']/@value")))[0]
	
	# create login payload
	payload = {
		"username": USERNAME, 
		"password": PASSWORD, 
		"execution": execution_token,
		"lt": lt_token,
		"submit": 'Login',
		"_eventId": 'submit'
	}

	# perform login
	result = session_requests.post(LOGIN_URL, data = payload, headers = dict(referer = LOGIN_URL))
	
	# print out html of login landing page
	print(result.text)
	
	# Scrape url
	result = session_requests.get(URL, headers = dict(referer = URL))
	tree = html.fromstring(result.content)	

	# create booking payload
	payload = {
		"startTime": '1524434400^', 
		"endTime": '1524437100^', 
		"roomId": '20^',
		"groupName": 'Hackathon2018'
	}

	# simulate session booking using new post request
	result = session_requests.post(BOOKING_URL, data = payload, headers = dict(referer = BOOKING_URL)) 
	

if __name__ == '__main__':

	main()