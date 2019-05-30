"""
Work on makeing this a generic session handler for all Polyglot's
"""

import requests,json,warnings

class pgSession():

    def __init__(self,parent,l_name,logger,host,port=None,debug_level=-1):
        self.parent = parent
        self.l_name = l_name
        self.logger = logger
        self.host   = host
        self.port   = port
        self.debug_level = debug_level
        if port is None:
            self.port_s = ""
        else:
            self.port_s = ':{}'.format(port)
        self.session = requests.Session()

    def get(self,path,payload,auth=None):
        url = "https://{}{}/{}".format(self.host,self.port_s,path)
        self.l_debug('get',0,"Sending: url={0} payload={1}".format(url,payload))
        # No speical headers?
        headers = {
            "Content-Type": "application/json"
        }
        if auth is not None:
            headers['Authorization'] = auth
        self.l_debug('get', 1, "headers={}".format(headers))
        # Some are getting unclosed socket warnings due to garbage collection?? no idea why, so just ignore them since we dont' care
        warnings.filterwarnings("ignore", category=ResourceWarning, message="unclosed.*<socket.socket.*>")
        #self.session.headers.update(headers)
        try:
            response = self.session.get(
                url,
                params=payload,
                headers=headers,
                timeout=60,
            )
            self.l_debug('get', 1, "url={}".format(response.url))
        # This is supposed to catch all request excpetions.
        except requests.exceptions.RequestException as e:
            self.l_error('get',"Connection error for %s: %s" % (url, e))
            return False
        return(self.response(response,'get'))

    def response(self,response,name):
        fname = 'reponse:'+name
        self.l_debug(fname,0,' Got: code=%s' % (response.status_code))
        self.l_debug(fname,2,'      text=%s' % (response.text))
        json_data = False
        if response.status_code == 200:
            self.l_debug(fname,0,' All good!')
            st = True
        elif response.status_code == 400:
            self.l_error(fname,"Bad request: %s: text: %s" % (response.url,response.text) )
        elif response.status_code == 404:
            self.l_error(fname,"Not Found: %s: text: %s" % (response.url,response.text) )
        elif response.status_code == 401:
            # Authentication error
            self.l_error(fname,"Unauthorized: %s: text: %s" % (response.url,response.text) )
        elif response.status_code == 500:
            self.l_error(fname,"Server Error: %s %s: text: %s" % (response.status_code,response.url,response.text) )
        else:
            self.l_error(fname,"Unknown response %s: %s %s" % (response.status_code, response.url, response.text) )
            self.l_error(fname,"Check system status: https://status.ecobee.com/")
        # No matter what, return the code and error
        try:
            json_data = json.loads(response.text)
        except (Exception) as err:
            self.l_error(fname,'Failed to convert to json {0}: {1}'.format(response.text,err), exc_info=True)
            json_data = False
        return { 'code': response.status_code, 'data': json_data }

    def post(self,path,payload={},params={},dump=True,auth=None):
        url = "https://{}{}/{}".format(self.host,self.port_s,path)
        if dump:
            payload = json.dumps(payload)
        self.l_debug('post',0,"Sending: url={0} payload={1}".format(url,payload))
        headers = {
            'Content-Length': str(len(payload))
        }
        if 'json' in params and ( params['json'] or params['json'] == 'true'):
            headers['Content-Type'] = 'application/json'
        if auth is not None:
            headers['Authorization'] = auth
        self.l_debug('post', 1, "headers={}".format(headers))
        #self.session.headers.update(headers)
        # Some are getting unclosed socket warnings due to garbage collection?? no idea why, so just ignore them since we dont' care
        warnings.filterwarnings("ignore", category=ResourceWarning, message="unclosed.*<socket.socket.*>")
        try:
            response = self.session.post(
                url,
                params=params,
                data=payload,
                headers=headers,
                timeout=60
            )
            self.l_debug('post', 1, "url={}".format(response.url))
        # This is supposed to catch all request excpetions.
        except requests.exceptions.RequestException as e:
            self.l_error('post',"Connection error for %s: %s" % (url, e))
            return False
        return(self.response(response,'post'))


    def l_info(self, name, string):
        self.logger.info("%s:%s: %s" %  (self.l_name,name,string))

    def l_error(self, name, string, exc_info=False):
        self.logger.error("%s:%s: %s" % (self.l_name,name,string), exc_info=exc_info)

    def l_warning(self, name, string):
        self.logger.warning("%s:%s: %s" % (self.l_name,name,string))

    def l_debug(self, name, debug_level, string):
        if self.debug_level >= debug_level:
            self.logger.debug("%s:%s: %s" % (self.l_name,name,string))
