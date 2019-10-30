import requests
import sys
import getopt

url    = 'https://maps.googleapis.com/maps/api/geocode/json'
apikey = ''

def getGeocode(address):
	params = {
		'address': address,
		'key': apikey
	}
	r = requests.get(url, params=params)
	return r

def getLatLng(address):
	r = getGeocode(address)

	body = {
		'status_code': r.status_code,
		'status': r.json()['status'],
		'success': False,
		'lat': None,
		'lng': None,
		'error_msg': None
	}

	if (body['status_code'] - 200) // 100 == 0:
		# Status code 2XX
		if body['status'].lower() == 'ok':
			location = r.json()['results'][0]['geometry']['location']
			body['lat'] = location['lat']
			body['lng'] = location['lng']
			body['success'] = True
		else:
			if 'error_message' in r.json():
				body['error_msg'] = r.json()['error_message']
			else:
				body['error_msg'] = r.text
	else:
		# Status code other than 2xx
		body['error_msg'] = r.text
	return body

def formatLatLngMsg(address):
	body = getLatLng(address)
	if body['success']:
		msg = '{}, {}, {}'.format(body['lat'],body['lng'],address.rstrip())
	else:
		msg = '{}, {}, {}'.format(body['status'],body['error_msg'],address.rstrip())
	return msg

def main(argv):
	msg = ''
	try:
		opts, args = getopt.getopt(argv,"f:a:")
	except getopt.GetoptError:
		print('python geocode.py [-a "ADDRESS"] [-f FILENAME]')
		sys.exit(2)

	for opt, arg in opts:
		if opt == '-f':
			f = open(arg, 'r')
			for line in f:
				print(formatLatLngMsg(line))
			f.close()
		elif opt == '-a':
			print(formatLatLngMsg(arg))
		else:
			msg = 'python geocode.py [-a "ADDRESS"] [-f FILENAME]'
			print(msg)

if __name__ == "__main__":
	main(sys.argv[1:])
