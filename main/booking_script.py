import requests
from lxml import html


STUDENTID = "11988401"
PASSWORD = "code2@learn"

LOGIN_URL = "https://sso.lib.uts.edu.au/cas/login?service=https%3A%2F%2Fwww.lib.uts.edu.au%2Froombooking%2F%3F_casCheck%3Dtrue"
BOOKING_URL = "https://www.lib.uts.edu.au/roombooking/bookings/create"
URL = [
		'https://www.lib.uts.edu.au/roombooking/bookings/index/campus/7#94',
		'https://www.lib.uts.edu.au/roombooking/bookings/index/campus/7#102',
		'https://www.lib.uts.edu.au/roombooking/bookings/index/campus/7#99',
		'https://www.lib.uts.edu.au/roombooking/bookings/index/campus/7#103',
		'https://www.lib.uts.edu.au/roombooking/bookings/index/campus/7#104',
		'https://www.lib.uts.edu.au/roombooking/bookings/index/campus/7#106',
		'https://www.lib.uts.edu.au/roombooking/bookings/index/campus/7#95',
		'https://www.lib.uts.edu.au/roombooking/bookings/index/campus/7#139',
		'https://www.lib.uts.edu.au/roombooking/bookings/index/campus/7#140',
		'https://www.lib.uts.edu.au/roombooking/bookings/index/campus/7#141',
		'https://www.lib.uts.edu.au/roombooking/bookings/index/campus/7#136',
		'https://www.lib.uts.edu.au/roombooking/bookings/index/campus/7#137',
		'https://www.lib.uts.edu.au/roombooking/bookings/index/campus/7#138',
	]


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
		"username": STUDENTID, 
		"password": PASSWORD, 
		"execution": execution_token,
		"lt": lt_token,
		"submit": 'Login',
		"_eventId": 'submit'
	}

	# perform login
	result = session_requests.post(LOGIN_URL, data = payload, headers = dict(referer = LOGIN_URL))

	timeslotfound = false
	
	firstAvailableTimeStart = 0
	firstAvailableTimeEnd = 0
	firstAvailableRoomId = 0
	
	
	# Scrape all urls (ie. rooms in B11) for available booking times, only check today's times
	for roomURL in URL:
		result = session_requests.get(roomURL, headers = dict(referer = roomURL))
		tree = html.fromstring(result.content)
		
		
		# start building booking details
		firstAvailableTimeEnd = firstAvailableTimeStart + 900
		# eg. extract the '103' https://www.lib.uts.edu.au/roombooking/bookings/index/campus/7#103
		firstAvailableRoomId = int(roomURL.replace('https://www.lib.uts.edu.au/roombooking/bookings/index/campus/7#', ''))
		
		# extract UNIX timestamp start time from id of day, (00:00 at start of that day), convert to int
		firstAvailableTimeStart = tree.xpath("//ul[class='day selectable ui-selectable']/@id")
		# above returns something like "day-103-1524405600" and we only want the ending UNIX timestamp
		stringtoremove = 'day-' + str(firstAvailableRoomId) + '-'
		firstAvailableTimeStart = int(firstAvailableTimeStart.replace(stringtoremove, '')
		
		# add 18000 as all timeslots start at 5am earliest
		firstAvailableTimeStart += 18000
		
		
		# find first available time slot for this room (there's max 76 15min timeslots each day and first <li> element is dayTitle, not timeslot)
		for timeslotindex in range(1,77):
		
			xpathstring = "//ul[class='day selectable ui-selectable']" + "[" + str(timeslotindex) + "]" + "/text()"
			timeslotclass = tree.xpath(xpathstring)
			
			# add (number of for loop iterations it took to get to the first free slot) * 900 as each slot is 15mins
			if timeslotclass is 'Free':
				firstAvailableTimeStart += (timeslotindex * 900)
				timeslotfound = true
				break
		
		# if time valid time slot found, move onto booking
		if timeslotfound:
			break
		


	# create booking payload
	payload = {
		"startTime": firstAvailableTimeStart, 
		"endTime": firstAvailableTimeEnd, 
		"roomId": firstAvailableRoomId,
		"groupName": STUDENTID
	}

	# simulate session booking using new post request
	result = session_requests.post(BOOKING_URL, data = payload, headers = dict(referer = BOOKING_URL)) 
	
	# print off all booking details (need to convert stuff to human readable)
	print firstAvailableTimeStart
	print firstAvailableTimeEnd
	print firstAvailableRoomId
	print STUDENTID

	
	
if __name__ == '__main__':
	main()
	
	