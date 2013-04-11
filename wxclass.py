import lxml.etree as ET
from hashlib import sha1
from copy import deepcopy
from hashlib import sha1


class WxError(Exception):
	"""docstring for WxError"""
	def __init__(self, errstr):
		super(WxError, self).__init__()
		self.errstr = errstr
		

class WxRequest(object):
	"""docstring for WxRequest"""
	def __init__(self, xmlinf, fromstr=True):
		super(WxRequest, self).__init__()
		if fromstr:
			xmlobj= ET.fromstring(xmlinf)
		else:
			xmlobj= ET.parse(xmlinf)
#		self.type= xmlobj.find('MsgType').text
#		self.api= wxapi.request[self.type]
#		self.keys= [x[0] for x in self.api]
#		self.argdict= {x:y for x,y in zip((key for key in self.keys),(xmlobj.text for xmlobj in ET.fromstring(xmlinf))) if y not in ['\n',None,'\r\n']}
		self.argdict= WxRequest._parse(xmlobj)

	@staticmethod
	def _parse(xmlobj):
		tmpdict={}
		for elem in xmlobj:
			if len(elem):
				tmpdict[elem.tag]= WxRequest.parse(elem)
			else:
				tmpdict[elem.tag]= elem.text
		return tmpdict

	def __getitem__(self, keystr):
		i=self.argdict
		for key in keystr.rsplit('.'):
			i=i[key]
		return i

	def __getattr__(self, key):
		return self[key]

#class WxResponse(object):
#	"""docstring for WxResponse"""
#	_apicache={}
#	@staticmethod
#	def _mkcache(templet, rootelm='xml'):
#		xmlparser= ET.XMLParser(strip_cdata=False)
#		for msgtype,templet in wxapi.responses.items():
#			WxResponse._apicache[msgtype]= {rootelm: ET.fromstring(templet, xmlparser)}
#			for xmlobj in WxResponse._apicache[msgtype][rootelm].iterdescendants():
#				if len(xmlobj):
#					WxResponse._apicache[msgtype][xmlobj.tag]= deepcopy(xmlobj)
#
#
# 	def __getitem__(self, keystr):
#		i=self.xmlobj
#		for key in keystr.rsplit('.'):
#			i= i.find(key)
#		return i.text
#
#	def __setitem__(self, keystr, value):
#		i=self.xmlobj
#		for key in keystr.rsplit('.'):
#			i= i.find(key)
#		i.text= value
#
#	def __init__(self, rstype):
#		super(WxResponse, self).__init__()
#		self.type = rstype
#		self.xmlobj= deepcopy(WxResponse._apicache[rstype])
#
#
#
#	def _autofill(self):
#		self.argdict[]
		

class WxAuth(object):
	"""docstring for WxAuth"""
	_check = lambda argd: argd['signature']==sha1(''.join(sorted([argd['token'],argd['timestamp'],argd['nonce']])).encode()).hexdigest()
	_sendback = lambda argd: argd['echostr']

	def __init__(self, arg, **additional):  #You should always give a token='xxxx' pram !
		super(WxAuth, self).__init__()
		self.arg = arg
		self.arg.update(additional)
		self.ok= bool(WxAuth._check(self.arg))
		

	def __bool__(self):
		return self.ok

	def reply(self):
		if self.ok:
			return WxAuth._sendback(self.arg)
		else:
			return 'FUCK YOU'
