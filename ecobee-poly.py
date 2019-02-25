#!/usr/bin/env python3

CLOUD = False

try:
    import polyinterface
except ImportError:
    import pgc_interface as polyinterface
    CLOUD = True
import sys
import json
import time
import http.client
import urllib.parse
import datetime
import os
import os.path
import re
from copy import deepcopy

from node_types import Thermostat, Sensor, Weather
from node_funcs import *

LOGGER = polyinterface.LOGGER

ECOBEE_API_URL = 'api.ecobee.com'

class Controller(polyinterface.Controller):
    def __init__(self, polyglot):
        super().__init__(polyglot)
        self.name = 'Ecobee Controller'
        self.auth_token = None
        self.token_type = None
        self.tokenData = {}
        self.in_discover = False
        self.discover_st = False
        self.refreshingTokens = False
        self.pinRun = False
        self.hb = 0
        self._cloud = CLOUD

    def start(self):
        #self.removeNoticesAll()
        LOGGER.info('Started Ecobee v2 NodeServer')
        self.heartbeat()
        #LOGGER.debug(self.polyConfig['customData'])
        self.serverdata = get_server_data(LOGGER)
        LOGGER.info('Ecobee NodeServer Version {}'.format(self.serverdata['version']))
        self.removeNoticesAll()
        self.heartbeat()
        # Force to false, and successful communication will fix it
        #self.set_ecobee_st(False) Causes it to always stay false.
        if 'tokenData' in self.polyConfig['customData']:
            self.tokenData = self.polyConfig['customData']['tokenData']
            self.auth_token = self.tokenData['access_token']
            self.token_type = self.tokenData['token_type']
            if self._checkTokens():
                self.discover()
        else:
            self._getPin()

    def _checkTokens(self):
        while self.refreshingTokens:
            time.sleep(.1)
        if 'access_token' in self.tokenData:
            ts_now = datetime.datetime.now()
            if 'expires' in self.tokenData:
                ts_exp = datetime.datetime.strptime(self.tokenData['expires'], '%Y-%m-%dT%H:%M:%S')
                if ts_now > ts_exp:
                    LOGGER.info('Tokens have expired. Refreshing...')
                    return self._getRefresh()
                else:
                    LOGGER.debug('Tokens valid until: {}'.format(self.tokenData['expires']))
                    return True
        else:
            LOGGER.error('tokenData or auth_token not available')
            # self.saveCustomData({})
            # this._getPin()
            return False

    def _saveTokens(self, data):
        cust_data = deepcopy(self.polyConfig['customData'])
        self.auth_token = data['access_token']
        self.token_type = data['token_type']
        if 'pinData' in cust_data:
            del cust_data['pinData']
        if 'expires_in' in data:
            ts = time.time() + data['expires_in']
            data['expires'] = datetime.datetime.fromtimestamp(ts).strftime("%Y-%m-%dT%H:%M:%S")
        cust_data['tokenData'] = data
        self.tokenData = deepcopy(data)
        self.saveCustomData(cust_data)
        self.removeNoticesAll()

    def _getRefresh(self):
        if 'refresh_token' in self.tokenData:
            self.refreshingTokens = True
            LOGGER.debug('Refresh Token found. Attempting to refresh tokens...')
            with open('server.json') as sf:
                server_data = json.load(sf)
                sf.close()
            auth_conn = http.client.HTTPSConnection(ECOBEE_API_URL)
            payload = 'grant_type=refresh_token&client_id={}&refresh_token={}'.format(server_data['api_key'], self.tokenData['refresh_token'])
            try:
                auth_conn.request('POST', '/token?{}'.format(payload))
            except Exception as e:
                LOGGER.error('getRefresh: Ecobee API Connection error: {}'.format(e))
                auth_conn.close()
                self.refreshingTokens = False
                self.set_ecobee_st(False)
                return False
            try:
                res = auth_conn.getresponse()
            except Exception as e:
                LOGGER.error('getRefresh: Ecobee API Response error: {}'.format(e))
                auth_conn.close()
                self.refreshingTokens = False
                self.set_ecobee_st(False)
                return False
            try:
                data = json.loads(res.read().decode('utf-8'))
            except Exception as e:
                LOGGER.error('getRefresh: Ecobee API Read/Parse error: {}'.format(e))
                auth_conn.close()
                self.refreshingTokens = False
                self.set_ecobee_st(False)
                return False
            auth_conn.close()
            self.set_ecobee_st(True)
            if 'error' in data:
                LOGGER.error('Requesting Auth: {} :: {}'.format(data['error'], data['error_description']))
                self.auth_token = None
                self.refreshingTokens = False
                if data['error'] == 'invalid_grant':
                    # Need to re-auth!
                    LOGGER.error('Found {}, need to re-authorize'.format(data['error']))
                    cust_data = deepcopy(self.polyConfig['customData'])
                    del cust_data['tokenData']
                    self.saveCustomData(cust_data)
                    self._getPin()
                return False
            elif 'access_token' in data:
                self._saveTokens(data)
                self.refreshingTokens = False
                return True
        else:
            LOGGER.info('Refresh Token not Found...')
            self.refreshingTokens = False
            return False

    def _getTokens(self, pinData):
        LOGGER.debug('PIN: {} found. Attempting to get tokens...'.format(pinData['ecobeePin']))
        with open('server.json') as sf:
            server_data = json.load(sf)
            sf.close()
        auth_conn = http.client.HTTPSConnection(ECOBEE_API_URL)
        payload = 'grant_type=ecobeePin&client_id={}&code={}'.format(server_data['api_key'], pinData['code'])
        try:
            auth_conn.request('POST', '/token?{}'.format(payload))
        except Exception as e:
            LOGGER.error('Ecobee API Connection error: {}'.format(e))
            auth_conn.close()
            return False
        try:
            res = auth_conn.getresponse()
        except Exception as e:
            LOGGER.error('getRefresh: Ecobee API Response error: {}'.format(e))
            auth_conn.close()
            self.refreshingTokens = False
            return False
        try:
            data = json.loads(res.read().decode('utf-8'))
        except Exception as e:
            LOGGER.error('getRefresh: Ecobee API Read/Parse error: {}'.format(e))
            auth_conn.close()
            self.refreshingTokens = False
            return False
        auth_conn.close()
        LOGGER.debug(data)
        if 'error' in data:
            LOGGER.error('{} :: {}'.format(data['error'], data['error_description']))
            return False
        if 'access_token' in data:
            LOGGER.debug('Got first set of tokens sucessfully.')
            self._saveTokens(data)
            return True

    def _getPin(self):
        with open('server.json') as sf:
            server_data = json.load(sf)
            sf.close()
        auth_conn = http.client.HTTPSConnection(ECOBEE_API_URL)
        payload = 'response_type=ecobeePin&client_id={}&scope=smartWrite'.format(server_data['api_key'])
        try:
            auth_conn.request('GET', '/authorize?{}'.format(payload))
        except Exception as e:
            LOGGER.error('Ecobee API Connection error: {}'.format(e))
            auth_conn.close()
            return False
        try:
            res = auth_conn.getresponse()
        except Exception as e:
            LOGGER.error('getRefresh: Ecobee API Response error: {}'.format(e))
            auth_conn.close()
            self.refreshingTokens = False
            return False
        try:
            data = json.loads(res.read().decode('utf-8'))
        except Exception as e:
            LOGGER.error('getRefresh: Ecobee API Read/Parse error: {}'.format(e))
            auth_conn.close()
            self.refreshingTokens = False
            return False
        auth_conn.close()
        LOGGER.debug(data)
        if 'ecobeePin' in data:
            self.addNotice({'myNotice': 'Click <a target="_blank" href="https://www.ecobee.com/home/ecobeeLogin.jsp">here</a> to login to your Ecobee account. Click on Profile > My Apps > Add Application and enter PIN: <b>{}</b>. Then restart the nodeserver. You have 10 minutes to complete this. The NodeServer will check every 60 seconds.'.format(data['ecobeePin'])})
            # cust_data = deepcopy(self.polyConfig['customData'])
            # cust_data['pinData'] = data
            # self.saveCustomData(cust_data)
            waitingOnPin = True
            while waitingOnPin:
                time.sleep(60)
                if self._getTokens(data):
                    waitingOnPin = False
                    self.discover()

    def shortPoll(self):
        pass

    def longPoll(self):
        # Call discovery if it failed on startup
        LOGGER.debug("{}:longPoll".format(self.address))
        self.heartbeat()
        if self.in_discover:
            LOGGER.debug("{}:longPoll: Skipping since discover is still running".format(self.address))
            return
        if self.discover_st is False:
            self.discover()
        self.updateThermostats()

    def heartbeat(self):
        LOGGER.debug('heartbeat hb={}'.format(self.hb))
        if self.hb == 0:
            self.reportCmd("DON",2)
            self.hb = 1
        else:
            self.reportCmd("DOF",2)
            self.hb = 0

    def updateThermostats(self):
        LOGGER.debug("{}:updateThermostats:".format(self.address))
        thermostats = self.getThermostats()
        if not isinstance(thermostats, dict):
            LOGGER.error('Thermostats instance wasn\'t dictionary. Skipping...')
            return
        for thermostatId, thermostat in thermostats.items():
            if self.checkRev(thermostat):
                address = self.thermostatIdToAddress(thermostatId)
                if address in self.nodes:
                    LOGGER.debug('Update detected in thermostat {}({}) doing full update.'.format(thermostat['name'], address))
                    fullData = self.getThermostatFull(thermostatId)
                    if fullData is not False:
                        self.nodes[address].update(thermostat, fullData)
                    else:
                        LOGGER.error('Failed to get updated data for thermostat: {}({})'.format(thermostat['name'], thermostatId))
                else:
                    LOGGER.error("Thermostat id '{}' address '{}' is not in our node list. thermostat: {}".format(thermostatId,address,thermostat))
            else:
                LOGGER.info("No {} '{}' update detected".format(thermostatId,thermostat['name']))

    def checkRev(self, tstat):
        if tstat['thermostatId'] in self.revData:
            curData = self.revData[tstat['thermostatId']]
            if (tstat['thermostatRev'] != curData['thermostatRev']
                    or tstat['alertsRev'] != curData['alertsRev']
                    or tstat['runtimeRev'] != curData['runtimeRev']
                    or tstat['intervalRev'] != curData['intervalRev']):
                return True
        return False

    def query(self):
        self.reportDrivers()
        for node in self.nodes:
            self.nodes[node].reportDrivers()

    def stop(self):
        LOGGER.debug('NodeServer stoping...')
        self.set_ecobee_st(False)

    def thermostatIdToAddress(self,tid):
        return 't{}'.format(tid)

    def discover(self, *args, **kwargs):
        # True means we are in dsocvery
        if self.in_discover:
            LOGGER.info('Discovering Ecobee Thermostats already running?')
            return True
        self.in_discover = True
        self.discover_st = False
        try:
            self.discover_st = self._discover()
        except Exception as e:
            LOGGER.error('discover failed: {}'.format(e))
            self.discover_st = False
        self.in_discover = False
        return self.discover_st

    def _discover(self, *args, **kwargs):
        LOGGER.info('Discovering Ecobee Thermostats')
        if self.auth_token is None:
            return False
        self.revData = {} # Intialize in case we fail
        thermostats = self.getThermostats()
        if thermostats is False:
            LOGGER.error("Discover Failed, No thermostats returned!  Will try again on next long poll")
            return False
        self.revData = deepcopy(thermostats)
        #
        # Build or update the profile first.
        #
        self.check_profile(thermostats)
        #
        # Now add our thermostats
        #
        for thermostatId, thermostat in thermostats.items():
            address = self.thermostatIdToAddress(thermostatId)
            if not address in self.nodes:
                fullData = self.getThermostatFull(thermostatId)
                if fullData is not False:
                    tstat = fullData['thermostatList'][0]
                    useCelsius = True if tstat['settings']['useCelsius'] else False
                    self.addNode(Thermostat(self, address, address, thermostatId,
                                            'Ecobee - {}'.format(get_valid_node_name(thermostat['name'])),
                                            thermostat, fullData, useCelsius))
        return True

    def check_profile(self,thermostats):
        self.profile_info = get_profile_info(LOGGER)
        #
        # First get all the climate programs so we can build the profile if necessary
        #
        climates = dict()
        for thermostatId, thermostat in thermostats.items():
            # Only get program data if we have the node.
            fullData = self.getThermostatSelection(thermostatId,includeProgram=True)
            if fullData is not False:
                programs = fullData['thermostatList'][0]['program']
                climates[thermostatId] = list()
                for climate in programs['climates']:
                    climates[thermostatId].append({'name': climate['name'], 'ref':climate['climateRef']})
        LOGGER.debug("check_profile: climates={}".format(climates))
        #
        # Set Default profile version if not Found
        #
        cdata = deepcopy(self.polyConfig['customData'])
        LOGGER.info('check_profile: profile_info={0} customData={1}'.format(self.profile_info,cdata))
        if not 'profile_info' in cdata:
            update_profile = True
        elif self.profile_info['version'] == cdata['profile_info']['version']:
            # Check if the climates are different
            update_profile = False
            LOGGER.info('check_profile: update_profile={} checking climates.'.format(update_profile))
            if 'climates' in cdata:
                current = cdata['climates']
                if not update_profile:
                    # Check if the climates have changed.
                    for id in climates:
                        if id in current:
                            if len(climates[id]) == len(current[id]):
                                for i in range(len(climates[id])):
                                    if climates[id][i] != current[id][i]:
                                        update_profile = True
                            else:
                                update_profile = True
                        else:
                            update_profile = True
            else:
                update_profile = True
        else:
            update_profile = True
        LOGGER.info('check_profile: update_profile={}'.format(update_profile))
        if update_profile:
            self.write_profile(climates)
            self.poly.installprofile()
            cdata['profile_info'] = self.profile_info
            cdata['climates'] = climates
            self.saveCustomData(cdata)

    def write_profile(self,climates):
      pfx = '{}:write_profile:'.format(self.address)
      #
      # Start the nls with the template data.
      #
      en_us_txt = "profile/nls/en_us.txt"
      make_file_dir(en_us_txt)
      LOGGER.info("{0} Writing {1}".format(pfx,en_us_txt))
      nls_tmpl = open("template/en_us.txt", "r")
      nls      = open(en_us_txt,  "w")
      for line in nls_tmpl:
        nls.write(line)
      nls_tmpl.close()
      # Open the nodedef custom for writing
      nodedef_f = 'profile/nodedef/custom.xml'
      LOGGER.info("{0} Writing {1}".format(pfx,nodedef_f))
      nodedef_h = open(nodedef_f, "w")
      nodedef_h.write('<nodedefs>\n')
      # Open the editor custom for writing
      editor_f = 'profile/editor/custom.xml'
      LOGGER.info("{0} Writing {1}".format(pfx,editor_f))
      editor_h = open(editor_f, "w")
      editor_h.write('<editors>\n')
      for id in climates:
        # Read thermostat template to write the custom version.
        in_h  = open('template/thermostat.xml','r')
        for line in in_h:
            nodedef_h.write(re.sub(r'tstatid',r'{0}'.format(id),line))
        in_h.close()
        # Read the editor template to write the custom version
        in_h  = open('template/editors.xml','r')
        for line in in_h:
            line = re.sub(r'tstatid',r'{0}'.format(id),line)
            line = re.sub(r'tstatcnta',r'{0}'.format(len(climateList)-1),line)
            # This is minus 2 because we don't allow selecting vacation.
            line = re.sub(r'tstatcnt',r'{0}'.format(len(climateList)-2),line)
            editor_h.write(line)
        in_h.close()
        # Then the NLS lines.
        nls.write("\n")
        nls.write('ND-EcobeeC_{0}-NAME = Ecobee Thermostat {0} (C)\n'.format(id))
        nls.write('ND-EcobeeC_{0}-ICON = Thermostat\n'.format(id))
        nls.write('ND-EcobeeF_{0}-NAME = Ecobee Thermostat {0} (F)\n'.format(id))
        nls.write('ND-EcobeeF_{0}-ICON = Thermostat\n'.format(id))
        # ucfirst them all
        customList = list()
        for i in range(len(climateList)):
            customList.append(climateList[i][0].upper() + climateList[i][1:])
        # Now see if there are custom names
        for i in range(len(climateList)):
            name = climateList[i]
            # Find this name in the map and replace with our name.
            for cli in climates[id]:
                if cli['ref'] == name:
                    customList[i] = cli['name']
        LOGGER.debug("{} customList={}".format(pfx,customList))
        for i in range(len(customList)):
            nls.write("CT_{}-{} = {}\n".format(id,i,customList[i]))
      nodedef_h.write('</nodedefs>\n')
      nodedef_h.close()
      editor_h.write('</editors>\n')
      editor_h.close()
      nls.close()
      LOGGER.info("{} done".format(pfx))

    def getThermostats(self):
        if not self._checkTokens():
            LOGGER.debug('getThermostat failed. Couldn\'t get tokens.')
            return False
        data = urllib.parse.quote_plus(json.dumps({
                'selection': {
                    'selectionType': 'registered',
                    'selectionMatch': '',
                    'includesEquipmentStatus': True
                }
            }))
        auth_conn = http.client.HTTPSConnection(ECOBEE_API_URL)
        headers = {
            'Content-Type': 'application/json',
            'Authorization': '{} {}'.format(self.token_type, self.auth_token)
        }
        try:
            auth_conn.request('GET', '/1/thermostatSummary?json={}'.format(data), headers = headers)
        except Exception as e:
            LOGGER.error('Ecobee API Connection error: {}'.format(e))
            auth_conn.close()
            self.set_ecobee_st(False)
            return False
        try:
            res = auth_conn.getresponse()
        except Exception as e:
            LOGGER.error('Ecobee getresponse failed: {}'.format(e))
            auth_conn.close()
            self.set_ecobee_st(False)
            return False
        if res is None:
            LOGGER.error("Bad response {} from thermostatSummary".format(res))
            self.set_ecobee_st(False)
            return False
        rdata = res.read().decode('utf-8')
        auth_conn.close()
        if rdata is None:
            LOGGER.error("Bad read {} from thermostatSummary".format(rdata))
            self.set_ecobee_st(False)
            return False
        try:
            data = json.loads(rdata)
        except Exception as e:
            LOGGER.error('Ecobee API data format error: {} for: {}'.format(e,rdata))
            self.set_ecobee_st(False)
            return False
        self.set_ecobee_st(True)
        thermostats = {}
        if 'revisionList' in data:
            for thermostat in data['revisionList']:
                revisionArray = thermostat.split(':')
                thermostats['{}'.format(revisionArray[0])] = {
                    'name': revisionArray[1],
                    'thermostatId': revisionArray[0],
                    'connected': revisionArray[2],
                    'thermostatRev': revisionArray[3],
                    'alertsRev': revisionArray[4],
                    'runtimeRev': revisionArray[5],
                    'intervalRev': revisionArray[6]
                }
        return thermostats

    def getThermostatFull(self, id):
        return self.getThermostatSelection(id,True,True,True,True,True,True,True,True,True,True,True,True)

    def getThermostatSelection(self,id,
                               includeEvents=False,
                               includeProgram=False,
                               includeSettings=False,
                               includeRuntime=False,
                               includeExtendedRuntime=False,
                               includeLocation=False,
                               includeEquipmentStatus=False,
                               includeVersion=False,
                               includeUtility=False,
                               includeAlerts=False,
                               includeWeather=False,
                               includeSensors=False
                               ):
        if not self._checkTokens():
            LOGGER.error('getThermostat failed. Couldn\'t get tokens.')
            return False
        LOGGER.info('Getting Thermostat Data for {}'.format(id))
        data = urllib.parse.quote_plus(json.dumps({
                'selection': {
                    'selectionType': 'thermostats',
                    'selectionMatch': id,
                    'includeEvents': includeEvents,
                    'includeProgram': includeProgram,
                    'includeSettings': includeSettings,
                    'includeRuntime': includeRuntime,
                    'includeExtendedRuntime': includeExtendedRuntime,
                    'includeLocation': includeLocation,
                    'includeEquipmentStatus': includeEquipmentStatus,
                    'includeVersion': includeVersion,
                    'includeUtility': includeUtility,
                    'includeAlerts': includeAlerts,
                    'includeWeather': includeWeather,
                    'includeSensors': includeSensors
                }
            }))
        auth_conn = http.client.HTTPSConnection(ECOBEE_API_URL)
        headers = {
            'Content-Type': 'application/json',
            'Authorization': '{} {}'.format(self.token_type, self.auth_token)
        }
        try:
            auth_conn.request('GET', '/1/thermostat?json={}'.format(data), headers = headers)
        except Exception as e:
            LOGGER.error('Ecobee API Connection error: {}'.format(e))
            auth_conn.close()
            self.set_ecobee_st(False)
            return False
        self.set_ecobee_st(True)
        LOGGER.info('Reading response for {}'.format(id))
        try:
            res = auth_conn.getresponse()
        except Exception as e:
            LOGGER.error('Ecobee API Response error: {}'.format(e))
            auth_conn.close()
            return False
        try:
          data = json.loads(res.read().decode('utf-8'))
        except Exception as e:
            LOGGER.error('Ecobee API Read/Parse Response error: {}'.format(e))
            auth_conn.close()
            return False
        auth_conn.close()
        LOGGER.debug('getThermostatSelection {} done'.format(id))
        LOGGER.debug('getThermostatSelection data={}'.format(data))
        return data

    def ecobeePost(self, thermostatId, postData = {}):
        if not self._checkTokens():
            LOGGER.error('ecobeePost failed. Tokens not available.')
            return False
        LOGGER.info('Posting Update Data for Thermostat {}'.format(thermostatId))
        postData['selection'] = {
            'selectionType': 'thermostats',
            'selectionMatch': thermostatId
        }
        LOGGER.debug('Post Data : {}'.format(json.dumps(postData,sort_keys=True, indent=2)))
        data = json.dumps(postData)
        headers = {
            'Content-Type': 'application/json',
            'Authorization': '{} {}'.format(self.token_type, self.auth_token),
            'Content-Length': len(data)
        }
        auth_conn = http.client.HTTPSConnection(ECOBEE_API_URL)
        try:
            auth_conn.request('POST', '/1/thermostat?json=true', data, headers)
        except Exception as e:
            LOGGER.error('Ecobee API Connection error: {}'.format(e))
            auth_conn.close()
            self.set_ecobee_st(False)
            return False
        self.set_ecobee_st(True)
        res = auth_conn.getresponse()
        data = json.loads(res.read().decode('utf-8'))
        auth_conn.close()
        #LOGGER.debug('Got : {}'.format(json.dumps(data,sort_keys=True, indent=2)))
        if 'error' in data:
            LOGGER.error('{} :: {}'.format(data['error'], data['error_description']))
            return False
        if 'status' in data:
            if 'code' in data['status']:
                if data['status']['code'] == 0:
                    return True
                else:
                    LOGGER.error('Bad return code {}:{}'.format(data['status']['code'],data['status']['message']))
        return False

    def cmd_poll(self,  *args, **kwargs):
        LOGGER.debug("{}:cmd_poll".format(self.address))
        self.updateThermostats()
        self.query()

    def cmd_query(self, *args, **kwargs):
        LOGGER.debug("{}:cmd_query".format(self.address))
        self.query()

    def set_ecobee_st(self,val):
      ival = 1 if val else 0
      LOGGER.debug("{}:set_ecobee_st: {}={}".format(self.address,val,ival))
      self.setDriver('GV1',ival)

    id = 'ECO_CTR'
    commands = {'DISCOVER': discover, 'QUERY': cmd_query, 'POLL': cmd_poll}
    drivers = [
        {'driver': 'ST', 'value': 1, 'uom': 2},
        {'driver': 'GV1', 'value': 0, 'uom': 2}
    ]

if __name__ == "__main__":
    try:
        polyglot = polyinterface.Interface('Ecobee')
        polyglot.start()
        control = Controller(polyglot)
        control.runForever()
    except (KeyboardInterrupt, SystemExit):
        sys.exit(0)
