import requests, json
import log

class HueBridge():
	"""
	Implement a simplified API for a Philips hue bridge.
	Iterating over HueBridge returns each HueLight object
	"""

	# set up log
	log = log.TerminalLog()

	def __init__(self, username, IP):
		"""
		Query hue bridge using given username and IP address to get list
		of lights. Create a dictionary containing HueLight object for
		each light, with names as keys
		"""
		url = 'http://'+IP+'/api/'+username+'/lights'
		r = requests.get(url).json()
	
		self.lights = {}	
		for light_id in r:
			name = (r[light_id]['name'])
			self.lights[name] = HueLight(name,light_id)

		# set username and IP address for all HueLight objects
		HueLight.username = username
		HueLight.IP = IP
					
	def __iter__(self):
		# create a list of HueLight objects to iterate over by index
		self.lights_list = list(self.lights.values())
		self.num_lights = len(self.lights_list)
		self.counter = -1
		return self
	
	def __next__(self):
		self.counter = self.counter + 1
		if self.counter == self.num_lights:
			raise StopIteration
		return self.lights_list[self.counter]
	
	def get(self, name):
		"""
		Return named HueLight object
		"""
		return self.lights[name]
		
class HueLight():
	"""
	Implement a simplified API for a Philips hue light
	"""
	username = ''
	IP = ''
	
	def __init__(self, name, ID):
		self.name = name
		self.ID = ID
		
	def get_name(self):
		"""
		Return the name of the light
		"""
		return self.name
		
	def on(self):
		"""
		Switch the light on
		"""
		self.__on_or_off('on')
	
	def off(self):
		"""
		Switches the light off
		"""
		self.__on_or_off('off')
		
	def __on_or_off(self, operation):
		url = 'http://'+self.IP+'/api/'+self.username+'/lights/'+self.ID+'/state'
		if operation == 'on':
			payload = '{"on": true}'
		else:
			payload = '{"on": false}'
		r = requests.put(url, data=payload)
		if r.status_code == 200:
			HueBridge.log.success(self.name + ' ' + operation)
		else:
			print ('failed')
		return r.json()
