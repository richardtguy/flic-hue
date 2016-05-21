import requests, json

class HueLight():
	"""
	Implements a simplified API for a Philips hue light
	"""
	username = ''
	IP = ''
	
	def __init__(self, name, ID):
		self.name = name
		self.ID = ID
		
	def get_name(self):
		"""
		Returns the name of the light
		"""
		return self.name
		
	def on(self):
		"""
		Switches the light on
		"""
		self.__on_or_off('on')
	
	def off(self):
		"""
		Switches the light off
		"""
		self.__on_or_off('off')
		
	def __on_or_off(self, operation):
		print (self.name, end='... ')
		url = 'http://'+self.IP+'/api/'+self.username+'/lights/'+self.ID+'/state'
		if operation == 'on':
			payload = '{"on": true}'
		else:
			payload = '{"on": false}'
		r = requests.put(url, data=payload)
		if r.status_code == 200:
			print (operation)
		else:
			print ('failed')
		return r.json()

def init_hue_lights(username, IP):
	"""
	Returns a dictionary of HueLight objects with light names as keys
	"""
	
	url = 'http://'+IP+'/api/'+username+'/lights'
	r = requests.get(url).json()
	
	lights = {}	
	for id in r:
		name = (r[id]['name'])
		lights[name] = HueLight(name,id)

	HueLight.username = username
	HueLight.IP = IP
	
	return lights
	

