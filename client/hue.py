import requests, json

class HueLight():
	'Class to implement simplified API for a Philips hue light'
	username = ''
	IP = ''
	
	def __init__(self, name, ID):
		self.name = name
		self.ID = ID
		
	def get_name(self):
		return self.name
		
	def on(self):
		print (self.name)
		url = 'http://'+self.IP+'/api/'+self.username+'/lights/'+self.ID+'/state'
		payload = '{"on": true}'
		r = requests.put(url, data=payload)
	
	def off(self):
		print (self.name)
		url = 'http://'+self.IP+'/api/'+self.username+'/lights/'+self.ID+'/state'
		payload = '{"on": false}'
		r = requests.put(url, data=payload)

def init_hue_lights(username, IP):
	'Returns a dictionary of HueLight objects with light names as keys'
	
	url = 'http://'+IP+'/api/'+username+'/lights'
	r = requests.get(url).json()
	
	lights = {}	
	for id in r:
		name = (r[id]['name'])
		lights[name] = HueLight(name,id)

	HueLight.username = username
	HueLight.IP = IP
	
	return lights
	

