import sys
import re
try:
    import polyinterface
except ImportError:
    import pgc_interface as polyinterface
from copy import deepcopy
import json
from node_funcs import *

LOGGER = polyinterface.LOGGER

modeMap = {
  'off': 0,
  'heat': 1,
  'cool': 2,
  'auto': 3,
  'auxHeatOnly': 4
}

equipmentStatusMap = {
  'off': 0,
  'heatPump': 1,
  'compCool1': 2,
  'heatPump2': 3,
  'heatPump3': 4,
  'compCool2': 5,
  'auxHeat1': 6,
  'auxHeat2': 7,
  'auxHeat3': 8
}

windMap = {
  '0': 0,
  'N': 1,
  'NNE': 2,
  'NE': 3,
  'ENE': 4,
  'E': 5,
  'ESE': 6,
  'SE': 7,
  'SSE': 8,
  'S': 9,
  'SSW': 10,
  'SW': 11,
  'WSW': 12,
  'W': 13,
  'WNW': 14,
  'NW': 15,
  'NNW': 16
}

transitionMap = {
  'running': 0,
  'nextTransition': 1,
  'indefinite': 2
}

fanMap = {
  'auto': 0,
  'on': 1,
}

driversMap = {
  'EcobeeF': [
    { 'driver': 'ST', 'value': 0, 'uom': '17' },
    { 'driver': 'CLISPH', 'value': 0, 'uom': '17' },
    { 'driver': 'CLISPC', 'value': 0, 'uom': '17' },
    { 'driver': 'CLIMD', 'value': 0, 'uom': '67' },
    { 'driver': 'CLIFS', 'value': 0, 'uom': '68' },
    { 'driver': 'CLIHUM', 'value': 0, 'uom': '22' },
    { 'driver': 'CLIHCS', 'value': 0, 'uom': '25' },
    { 'driver': 'CLIFRS', 'value': 0, 'uom': '80' },
    { 'driver': 'GV1', 'value': 0, 'uom': '22' },
    { 'driver': 'CLISMD', 'value': 0, 'uom': '25' },
    { 'driver': 'GV4', 'value': 0, 'uom': '25' },
    { 'driver': 'GV3', 'value': 0, 'uom': '25' },
    { 'driver': 'GV5', 'value': 0, 'uom': '22' },
    { 'driver': 'GV6', 'value': 0, 'uom': '25' },
    { 'driver': 'GV7', 'value': 0, 'uom': '25' },
    { 'driver': 'GV8', 'value': 0, 'uom': '2' },
    { 'driver': 'GV9', 'value': 1, 'uom': '25' },
    { 'driver': 'GV10', 'value': 10, 'uom': '56' },
    { 'driver': 'GV11', 'value': 10, 'uom': '56' }
  ],
  'EcobeeC': [
    { 'driver': 'ST', 'value': 0, 'uom': '4' },
    { 'driver': 'CLISPH', 'value': 0, 'uom': '4' },
    { 'driver': 'CLISPC', 'value': 0, 'uom': '4' },
    { 'driver': 'CLIMD', 'value': 0, 'uom': '67' },
    { 'driver': 'CLIFS', 'value': 0, 'uom': '68' },
    { 'driver': 'CLIHUM', 'value': 0, 'uom': '22' },
    { 'driver': 'CLIHCS', 'value': 0, 'uom': '25' },
    { 'driver': 'CLIFRS', 'value': 0, 'uom': '80' },
    { 'driver': 'GV1', 'value': 0, 'uom': '22' },
    { 'driver': 'CLISMD', 'value': 0, 'uom': '25' },
    { 'driver': 'GV4', 'value': 0, 'uom': '25' },
    { 'driver': 'GV3', 'value': 0, 'uom': '25' },
    { 'driver': 'GV5', 'value': 0, 'uom': '22' },
    { 'driver': 'GV6', 'value': 0, 'uom': '25' },
    { 'driver': 'GV7', 'value': 0, 'uom': '25' },
    { 'driver': 'GV8', 'value': 0, 'uom': '2' },
    { 'driver': 'GV9', 'value': 1, 'uom': '25' },
    { 'driver': 'GV10', 'value': 10, 'uom': '56' },
    { 'driver': 'GV11', 'value': 10, 'uom': '56' }
],
  'EcobeeSensorF': [
    { 'driver': 'ST', 'value': 0, 'uom': '17' },
    { 'driver': 'GV1', 'value': 0, 'uom': '25' },
    { 'driver': 'GV2', 'value': 0, 'uom': '2' }
  ],
  'EcobeeSensorC': [
    { 'driver': 'ST', 'value': 0, 'uom': '4' },
    { 'driver': 'GV1', 'value': 0, 'uom': '25' },
    { 'driver': 'GV2', 'value': 0, 'uom': '2' }
  ],
  'EcobeeSensorHF': [
    { 'driver': 'ST', 'value': 0, 'uom': '17' },
    { 'driver': 'CLIHUM', 'value': -1, 'uom': '22' },
    { 'driver': 'GV1', 'value': 0, 'uom': '25' },
    { 'driver': 'GV2', 'value': 0, 'uom': '2' }
  ],
  'EcobeeSensorHC': [
    { 'driver': 'ST', 'value': 0, 'uom': '4' },
    { 'driver': 'CLIHUM', 'value': -1, 'uom': '22' },
    { 'driver': 'GV1', 'value': 0, 'uom': '25' },
    { 'driver': 'GV2', 'value': 0, 'uom': '2' }
  ],
  'EcobeeWeatherF': [
    { 'driver': 'ST', 'value': 0, 'uom': '17' },
    { 'driver': 'GV1', 'value': 0, 'uom': '22' },
    { 'driver': 'GV2', 'value': 0, 'uom': '22' },
    { 'driver': 'GV3', 'value': 0, 'uom': '17' },
    { 'driver': 'GV4', 'value': 0, 'uom': '17' },
    { 'driver': 'GV5', 'value': 0, 'uom': '48' },
    { 'driver': 'GV6', 'value': 0, 'uom': '25' },
    { 'driver': 'GV7', 'value': 0, 'uom': '25' },
    { 'driver': 'GV8', 'value': 0, 'uom': '25' },
    { 'driver': 'GV9', 'value': 0, 'uom': '25' }
  ],
  'EcobeeWeatherC': [
    { 'driver': 'ST', 'value': 0, 'uom': '4' },
    { 'driver': 'GV1', 'value': 0, 'uom': '22' },
    { 'driver': 'GV2', 'value': 0, 'uom': '22' },
    { 'driver': 'GV3', 'value': 0, 'uom': '4' },
    { 'driver': 'GV4', 'value': 0, 'uom': '4' },
    { 'driver': 'GV5', 'value': 0, 'uom': '48' },
    { 'driver': 'GV6', 'value': 0, 'uom': '25' },
    { 'driver': 'GV7', 'value': 0, 'uom': '25' },
    { 'driver': 'GV8', 'value': 0, 'uom': '25' },
    { 'driver': 'GV9', 'value': 0, 'uom': '25' }
  ],
}

"""
 Address scheme:
 Devices: n<profile>_t<thermostatId> e.g. n003_t511892759243
 Thermostat Sensor: n<profile>_s<thermostatId> e.g. n003_s511892759243
 Current Weather: n<profile>_w<thermostatId> e.g. n003_w511892759243
 Forecast Weather: n<profile>_f<thermostatId> e.g. n003_f511892759243
 Sensors: n<profile>_s<sensor code> e.g. n003_rs_r6dr
"""

class Thermostat(polyinterface.Node):
    def __init__(self, controller, primary, address, thermostatId, name, revData, fullData, useCelsius):
        #LOGGER.debug("fullData={}".format(json.dumps(fullData, sort_keys=True, indent=2)))
        self.controller = controller
        self.name = name
        self.thermostatId = thermostatId
        self.tstat = fullData['thermostatList'][0]
        self.program = self.tstat['program']
        self.settings = self.tstat['settings']
        self.useCelsius = useCelsius
        self.type = 'thermostat'
        self.id = 'EcobeeC' if self.useCelsius else 'EcobeeF'
        self.drivers = self._convertDrivers(driversMap[self.id]) if self.controller._cloud else deepcopy(driversMap[self.id])
        self.id = '{}_{}'.format(self.id,thermostatId)
        self.revData = revData
        self.fullData = fullData
        # Will check wether we show weather later
        self.do_weather = None
        self.weather = None
        self.forcast = None
        # We track our driver values because we need the value before it's been pushed.
        self.driver = dict()
        super(Thermostat, self).__init__(controller, primary, address, name)

    def setDriver(self,driver,value):
        self.driver[driver] = value
        super(Thermostat, self).setDriver(driver,value)

    def getDriver(self,driver):
        if not driver in self.driver:
            self.driver[driver] = super(Thermostat, self).getDriver(driver)
        return self.driver[driver]

    def start(self):
        if 'remoteSensors' in self.tstat:
            #LOGGER.debug("{}:remoteSensors={}".format(self.address,json.dumps(self.tstat['remoteSensors'], sort_keys=True, indent=2)))
            for sensor in self.tstat['remoteSensors']:
                if 'id' in sensor and 'name' in sensor:
                    sensorAddress = self.getSensorAddress(sensor)
                    if sensorAddress is not None:
                        # Delete the old one if it exists
                        sensorAddressOld = self.getSensorAddressOld(sensor)
                        try:
                          fonode = self.controller.poly.getNode(sensorAddressOld)
                        except TypeError:
                          fonode = False
                          LOGGER.debug("caught fnode fail due to polyglot cloud bug? assuming old node not found")
                        if fonode is not False:
                            self.controller.addNotice({fnode['address']: "Sensor created with new name, please delete old sensor with address '{}' in the Polyglot UI.".format(fnode['address'])})
                        addS = False
                        # Add Sensor is necessary
                        # Did the nodedef id change?
                        nid = self.get_sensor_nodedef(sensor)
                        sensorName = get_valid_node_name('Ecobee - {}'.format(sensor['name']))
                        self.controller.addNode(Sensor(self.controller, self.address, sensorAddress,
                                                       sensorName, nid, self))
        self.check_weather()
        self.update(self.revData, self.fullData)
        self.query()

    def check_weather(self):
        # Initialize?
        if self.do_weather is None:
            try:
                dval = self.getDriver('GV9')
                LOGGER.debug('check_weather: Initial value GV9={}'.format(dval))
                dval = int(dval)
                # Set False if 0, otherwise True since initially it may be None?
                self.do_weather = False if dval == 0 else True
            except:
                LOGGER.error('check_weather: Failed to getDriver GV9, asuming do_weather=True')
                self.do_weather = True
        if self.do_weather:
            # we want some weather
            if self.weather is None:
                # and we don't have the nodes yet, so add them
                if 'weather' in self.tstat:
                    weatherAddress = 'w{}'.format(self.thermostatId)
                    weatherName = get_valid_node_name('Ecobee - Weather')
                    self.weather = self.controller.addNode(Weather(self.controller, self.address, weatherAddress, weatherName, self.useCelsius, False))
                    forecastAddress = 'f{}'.format(self.thermostatId)
                    forecastName = get_valid_node_name('Ecobee - Forecast')
                    self.forcast = self.controller.addNode(Weather(self.controller, self.address, forecastAddress, forecastName, self.useCelsius, True))
            else:
                self.weather.update(self.tstat['weather'])
                self.forcast.update(self.tstat['weather'])
        else:
            # we dont want weather
            if self.weather is not None:
                # we have the nodes, delete them
                self.controller.delNode(self.weather.address)
                self.weather = None
                self.controller.delNode(self.forcast.address)
                self.forcast = None


    def get_sensor_nodedef(self,sensor):
        # Given the ecobee sensor data, figure out the nodedef
        # 'capability': [{'id': '1', 'type': 'temperature', 'value': '724'}, {'id': '2', 'type': 'humidity', 'value': '41'}, {'id': '3', 'type': 'occupancy', 'value': 'false'}
        has_hum = False
        if 'capability' in sensor:
            for cb in sensor['capability']:
                if cb['type'] == 'humidity':
                    has_hum = True
        CorF = 'C' if self.useCelsius else 'F'
        HorN = 'H' if has_hum else ''
        return 'EcobeeSensor{}{}'.format(HorN,CorF)

    def update(self, revData, fullData):
      self.l_debug('update','')
      #LOGGER.debug("fullData={}".format(json.dumps(fullData, sort_keys=True, indent=2)))
      #LOGGER.debug("revData={}".format(json.dumps(revData, sort_keys=True, indent=2)))
      if not 'thermostatList' in fullData:
        self.l_error('update',"No thermostatList in fullData={}".format(json.dumps(fullData, sort_keys=True, indent=2)))
        return False
      self.revData = revData
      self.fullData = fullData
      self.tstat = fullData['thermostatList'][0]
      self.settings = self.tstat['settings']
      self.program  = self.tstat['program']
      self.events   = self.tstat['events']
      self._update()

    def _update(self):
      equipmentStatus = self.tstat['equipmentStatus'].split(',')
      #LOGGER.debug("settings={}".format(json.dumps(self.settings, sort_keys=True, indent=2)))
      self.runtime = self.tstat['runtime']
      self.l_debug('_update:',' runtime={}'.format(json.dumps(self.runtime, sort_keys=True, indent=2)))
      clihcs = 0
      for status in equipmentStatus:
        if status in equipmentStatusMap:
          clihcs = equipmentStatusMap[status]
          break
      # This is what the schedule says should be enabled.
      climateType = self.program['currentClimateRef']
      # And the default mode, unless there is an event
      self.clismd = 0
      # Is there an active event?
      self.l_debug('_update','events={}'.format(json.dumps(self.events, sort_keys=True, indent=2)))
      # Find the first running event
      event_running = False
      for event in self.events:
          if event['running'] and event_running is False:
              event_running = event
              self.l_debug('_update','running event: {}'.format(json.dumps(event, sort_keys=True, indent=2)))
      if event_running is not False:
        if event_running['type'] == 'hold':
            #LOGGER.debug("Checking: events={}".format(json.dumps(self.events, sort_keys=True, indent=2)))
            self.l_debug('_update'," #events={} type={} holdClimateRef={}".
                         format(len(self.events),
                                event_running['type'],
                                event_running['holdClimateRef']))
            # This seems to mean an indefinite hold
            #  "endDate": "2035-01-01", "endTime": "00:00:00",
            if event_running['endTime'] == '00:00:00':
                self.clismd = transitionMap['indefinite']
            else:
                self.clismd = transitionMap['nextTransition']
            if event_running['holdClimateRef'] != '':
                climateType = event_running['holdClimateRef']
        elif event_running['type'] == 'vacation':
            climateType = 'vacation'
        elif event_running['type'] == 'autoAway':
            # name will alwys smartAway or smartAway?
            climateType = event_running['name']
            if climateType != 'smartAway':
                self.l_error('_update','autoAway event name is "{}" which is not supported, using smartAway. Please notify developer.'.format(climateType))
                climateType = 'smartAway'
        elif event_running['type'] == 'autoHome':
            # name will alwys smartAway or smartHome?
            climateType = event_running['name']
            if climateType != 'smartHome':
                self.l_error('_update','autoHome event name is "{}" which is not supported, using smartHome. Please notify developer.'.format(climateType))
                climateType = 'smartHome'
        elif event_running['type'] == 'demandResponse':
            # What are thse names?
            climateType = event_running['name']
            self.l_error('_update','demandResponse event name is "{}" which is not supported, using demandResponse. Please notify developer.'.format(climateType))
            climateType = 'demandResponse'
        else:
            self.l_error('_update','Unknown event type "{}" name "{}" for event: {}'.format(event_running['type'],event_running['name'],event))

      self.l_debug('_update','climateType={}'.format(climateType))
      #LOGGER.debug("program['climates']={}".format(self.program['climates']))
      #LOGGER.debug("settings={}".format(json.dumps(self.settings, sort_keys=True, indent=2)))
      #LOGGER.debug("program={}".format(json.dumps(self.program, sort_keys=True, indent=2)))
      #LOGGER.debug("{}:update: equipmentStatus={}".format(self.address,equipmentStatus))
      # The fan is on if on, or we are in a auxHeat mode and we don't control the fan,
      if 'fan' in equipmentStatus or (clihcs >= 6 and not self.settings['fanControlRequired']):
        clifrs = 1
      else:
        clifrs = 0
      self.l_debug('_update','clifrs={} (equipmentStatus={} or clihcs={}, fanControlRequired={}'
                   .format(clifrs,equipmentStatus,clihcs,self.settings['fanControlRequired'])
                   )
      self.l_debug('_update','backlightOnIntensity={} backlightSleepIntensisty={}'.
                    format(self.settings['backlightOnIntensity'],self.settings['backlightSleepIntensity']))
      updates = {
        'ST': self.tempToDriver(self.runtime['actualTemperature'],True,False),
        'CLISPH': self.tempToDriver(self.runtime['desiredHeat'],True),
        'CLISPC': self.tempToDriver(self.runtime['desiredCool'],True),
        'CLIMD': modeMap[self.settings['hvacMode']],
        'CLIFS': fanMap[self.runtime["desiredFanMode"]],
        'CLIHUM': self.runtime['actualHumidity'],
        'CLIHCS': clihcs,
        'CLIFRS': clifrs,
        'GV1': self.runtime['desiredHumidity'],
        'CLISMD': self.clismd,
        'GV4': self.settings['fanMinOnTime'],
        'GV3': self.getClimateIndex(climateType),
        'GV5': self.runtime['desiredDehumidity'],
        'GV6': 1 if self.settings['autoAway'] else 0,
        'GV7': 1 if self.settings['followMeComfort'] else 0,
        'GV8': 1 if self.runtime['connected'] else 0,
        'GV10': self.settings['backlightOnIntensity'],
        'GV11': self.settings['backlightSleepIntensity']
      }
      for key, value in updates.items():
          self.l_debug('_update','setDriver({},{})'.format(key,value))
          self.setDriver(key, value)

      # Update my remote sensors.
      for sensor in self.tstat['remoteSensors']:
          saddr = self.getSensorAddress(sensor)
          if saddr in self.controller.nodes:
              if self.controller.nodes[saddr].primary == self.address:
                  self.controller.nodes[saddr].update(sensor)
              else:
                  LOGGER.debug("{}._update: remoteSensor {} is not mine.".format(self.address,saddr))
          else:
              LOGGER.error("{}._update: remoteSensor {} is not in our node list: {}".format(self.address,saddr,self.controller.nodes))
      self.check_weather()

    def getClimateIndex(self,name):
      if name in climateMap:
          climateIndex = climateMap[name]
      else:
          LOGGER.error("Unknown climateType='{}'".format(name))
          climateIndex = climateMap['unknown']
      return climateIndex

    def getCurrentClimateDict(self):
        return self.getClimateDict(self.program['currentClimateRef'])

    def getClimateDict(self,name):
      for cref in self.program['climates']:
        if name == cref['climateRef']:
            LOGGER.info('{}:getClimateDict: Returning {}'.format(self.address,cref))
            return cref
      LOGGER.error('{}:getClimateDict: Unknown climateRef name {}'.format(self.address,name))
      return None

    def getSensorAddressOld(self,sdata):
      # return the sensor address from the ecobee api data for one sensor
      if 'id' in sdata:
          return re.sub('\\:', '', sdata['id']).lower()[:12]
      return None

    def getSensorAddress(self,sdata):
      # Is it the sensor in the thermostat?
      if sdata['type'] == 'thermostat':
        # Yes, use the thermostat id
        return 's{}'.format(self.tstat['identifier'])
      # No, use the remote sensor code if available
      if 'code' in sdata:
        return 'rs_{}'.format(sdata['code'].lower())
      LOGGER.error("{}:getSensorAddress: Unable to determine sensor address for: {}".format(self.address,sdata))

    def query(self, command=None):
      self.reportDrivers()

    def getHoldType(self,val=None):
      if val is None:
          # They want the current value
          val = self.getDriver('CLISMD')
      # Return the holdType name, if set to Hold, return indefinite
      # Otherwise return nextTransition
      return getMapName(transitionMap,2) if int(val) == 2 else getMapName(transitionMap,1)

    def ecobeePost(self,command):
        return self.controller.ecobeePost(self.thermostatId, command)

    def pushResume(self):
      LOGGER.debug('{}:setResume: Cancelling hold'.format(self.address))
      func = {
        'type': 'resumeProgram',
        'params': {
          'resumeAll': False
        }
      }
      if self.ecobeePost( {'functions': [func]}):
        # All cancelled, restore settings to program
        self.setScheduleMode(0)
        # This is what the current climate type says it should be
        self.setClimateSettings()
        self.events = list()
        return True
      LOGGER.error('{}:setResume: Post failed?'.format(self.address))
      return False

    def setClimateSettings(self,climateName=None):
      if climateName is None:
          climateName = self.program['currentClimateRef']
      # Set to what the current schedule says
      self.setClimateType(climateName)
      cdict = self.getClimateDict(climateName)
      self.setCool(cdict['coolTemp'],True)
      self.setHeat(cdict['heatTemp'],True)
      # TODO: cdict contains coolFan & heatFan, should we use those?
      self.setFanMode(cdict['coolFan'])
      # We assume fan goes off, next refresh will say what it really is.
      self.setFanState(0)

    def pushScheduleMode(self,clismd=None,coolTemp=None,heatTemp=None,fanMode=None):
      LOGGER.debug("pushScheduleMode: clismd={} coolTemp={} heatTemp={}".format(clismd,coolTemp,heatTemp))
      if clismd is None:
          clismd = int(self.getDriver('CLISMD'))
      elif int(clismd) == 0:
        return self.pushResume()
      # Get the new schedule mode, current if in a hold, or hold next
      clismd_name = self.getHoldType(clismd)
      if heatTemp is None:
          heatTemp = self.getDriver('CLISPH')
      if coolTemp is None:
          coolTemp = self.getDriver('CLISPC')
      params = {
        'holdType': clismd_name,
        'heatHoldTemp': self.tempToEcobee(heatTemp),
        'coolHoldTemp': self.tempToEcobee(coolTemp),
      }
      if fanMode is not None:
          params['fan'] = getMapName(fanMap,fanMode)
      func = {
        'type': 'setHold',
        'params': params
      }
      if self.ecobeePost({'functions': [func]}):
        self.setScheduleMode(clismd_name)
        self.setCool(coolTemp)
        self.setHeat(heatTemp)
        if fanMode is not None:
          ir = self.setFanMode(fanMode)
          if int(ir) == 1:
            self.setFanState(1)
          else:
            self.setFanState(0)

    def pushBacklight(self,val):
        self.l_debug('pushBacklight','{}'.format(val))
        #
        # Push settings test
        #
        params = {
            "thermostat": {
                "settings": {
                    "backlightOnIntensity":val
                    }
                }
        }
        if self.ecobeePost(params):
            self.setBacklight(val)

    def setBacklight(self,val):
      self.setDriver('GV10', val)

    def pushBacklightSleep(self,val):
        self.l_debug('pushBacklightSleep','{}'.format(val))
        #
        # Push settings test
        #
        params = {
            "thermostat": {
                "settings": {
                'backlightSleepIntensity':val
                    }
                }
        }
        if self.ecobeePost(params):
            self.setBacklightSleep(val)

    def setBacklightSleep(self,val):
      self.setDriver('GV11', val)

    #
    # Set Methods for drivers so they are set the same way
    #
    def setScheduleMode(self,val):
      LOGGER.debug('{}:setScheduleMode: {}'.format(self.address,val))
      if not is_int(val):
          if val in transitionMap:
            val = transitionMap[val]
          else:
            logger.ERROR("{}:setScheduleMode: Unknown transitionMap name {}".format(self.address,val))
            return False
      self.setDriver('CLISMD',int(val))
      self.clismd = int(val)

    # Set current climateType
    # True = use current
    # string = looking name
    # int = just do it
    def setClimateType(self,val):
      if val is True:
        val = self.program['currentClimateRef']
      if not is_int(val):
        if val in climateMap:
          val = climateMap[val]
        else:
          LOGGER.error("Unknown climate name {}".format(val))
          return False
      self.setDriver('GV3',int(val))

    # Convert Tempearture used by ISY to Ecobee API value
    def tempToEcobee(self,temp):
      if self.useCelsius:
        return(toF(float(temp)) * 10)
      return(int(temp) * 10)

    # Convert Temperature for driver
    # FromE converts from Ecobee API value, and to C if necessary
    # By default F values are converted to int, but for ambiant temp we
    # allow one decimal.
    def tempToDriver(self,temp,fromE=False,FtoInt=True):
      try:
        temp = float(temp)
      except:
        LOGGER.error("{}:tempToDriver: Unable to convert '{}' to float")
        return False
      # Convert from Ecobee value, unless it's already 0.
      if fromE and temp != 0:
          temp = temp / 10
      if self.useCelsius:
        if fromE:
          temp = toC(temp)
        return(temp)
      else:
        if FtoInt:
          return(int(temp))
        else:
          return(temp)

    def setCool(self,val,fromE=False,FtoInt=True):
      dval = self.tempToDriver(val,fromE,FtoInt)
      LOGGER.debug('{}:setCool: {}={} fromE={} FtoInt={}'.format(self.address,val,dval,fromE,FtoInt))
      self.setDriver('CLISPC',dval)

    def setHeat(self,val,fromE=False,FtoInt=True):
      dval = self.tempToDriver(val,fromE,FtoInt)
      LOGGER.debug('{}:setHeat: {}={} fromE={} FtoInt={}'.format(self.address,val,dval,fromE,FtoInt))
      self.setDriver('CLISPH',dval)

    def setFanMode(self,val):
      if is_int(val):
          dval = val
      else:
          if val in fanMap:
            dval = fanMap[val]
          else:
            logger.ERROR("{}:Fan: Unknown fanMap name {}".format(self.address,val))
            return False
      LOGGER.debug('{}:setFanMode: {}={}'.format(self.address,val,dval))
      self.setDriver('CLIFS',dval)
      return dval

    def setFanState(self,val):
      if is_int(val):
          dval = val
      else:
          if val in fanMap:
            dval = fanMap[val]
          else:
            logger.ERROR("{}:Fan: Unknown fanMap name {}".format(self.address,val))
            return False
      LOGGER.debug('{}:setFanState: {}={}'.format(self.address,val,dval))
      self.setDriver('CLIFRS',dval)

    def cmdSetPF(self, cmd):
      # Set a hold:  https://www.ecobee.com/home/developer/api/examples/ex5.shtml
      # TODO: Need to check that mode is auto,
      #LOGGER.debug("self.events={}".format(json.dumps(self.events, sort_keys=True, indent=2)))
      #LOGGER.debug("program={}".format(json.dumps(self.program, sort_keys=True, indent=2)))
      driver = cmd['cmd']
      if driver == 'CLISPH':
        return self.pushScheduleMode(heatTemp=cmd['value'])
      elif driver == 'CLISPC':
        return self.pushScheduleMode(coolTemp=cmd['value'])
      else:
        return self.pushScheduleMode(fanMode=cmd['value'])

    def cmdSetScheduleMode(self, cmd):
      '''
        Set the Schedule Mode, like running, or a hold
      '''
      if int(self.getDriver(cmd['cmd'])) == int(cmd['value']):
        LOGGER.debug("cmdSetScheduleMode: {}={} already set to {}".format(cmd['cmd'],self.getDriver(cmd['cmd']),cmd['value']))
      else:
        self.pushScheduleMode(cmd['value'])

    def cmdSetMode(self, cmd):
      if int(self.getDriver(cmd['cmd'])) == int(cmd['value']):
        LOGGER.debug("cmdSetMode: {} already set to {}".format(cmd['cmd'],int(cmd['value'])))
      else:
        name = getMapName(modeMap,int(cmd['value']))
        LOGGER.info('Setting Thermostat {} to mode: {} (value={})'.format(self.name, name, cmd['value']))
        if self.ecobeePost( {'thermostat': {'settings': {'hvacMode': name}}}):
          self.setDriver(cmd['cmd'], cmd['value'])

    def cmdSetClimateType(self, cmd):
      LOGGER.debug('{}:cmdSetClimateType: {}={}'.format(self.address,cmd['cmd'],cmd['value']))
      # We don't check if this is already current since they may just want setpoints returned.
      climateName = getMapName(climateMap,int(cmd['value']))
      command = {
        'functions': [{
          'type': 'setHold',
          'params': {
            'holdType': self.getHoldType(),
            'holdClimateRef': climateName
          }
        }]
      }
      if self.ecobeePost(command):
        self.setDriver(cmd['cmd'], cmd['value'])
        self.setDriver('CLISMD',transitionMap[self.getHoldType()])
        # If we went back to current climate name that will reset temps, so reset isy
        #if self.program['currentClimateRef'] == climateName:
        self.setClimateSettings(climateName)

    def cmdSetFanOnTime(self, cmd):
      if int(self.getDriver(cmd['cmd'])) == int(cmd['value']):
        LOGGER.debug("cmdSetFanOnTime: {} already set to {}".format(cmd['cmd'],int(cmd['value'])))
      else:
        command = {
          'thermostat': {
            'settings': {
              'fanMinOnTime': cmd['value']
            }
          }
        }
        if self.ecobeePost( command):
          self.setDriver(cmd['cmd'], cmd['value'])

    def cmdSmartHome(self, cmd):
      if int(self.getDriver(cmd['cmd'])) == int(cmd['value']):
        LOGGER.debug("cmdSetSmartHome: {} already set to {}".format(cmd['cmd'],int(cmd['value'])))
      else:
        command = {
          'thermostat': {
            'settings': {
              'autoAway': True if cmd['value'] == '1' else False
            }
          }
        }
        if self.ecobeePost( command):
          self.setDriver(cmd['cmd'], cmd['value'])

    def cmdFollowMe(self, cmd):
      if int(self.getDriver(cmd['cmd'])) == int(cmd['value']):
        LOGGER.debug("cmdFollowMe: {} already set to {}".format(cmd['cmd'],int(cmd['value'])))
      else:
        command = {
          'thermostat': {
            'settings': {
              'followMeComfort': True if cmd['value'] == '1' else False
            }
          }
        }
        if self.ecobeePost( command):
          self.setDriver(cmd['cmd'], cmd['value'])

    def cmdSetDoWeather(self, cmd):
      value = int(cmd['value'])
      if int(self.getDriver(cmd['cmd'])) == value:
        LOGGER.debug("cmdSetDoWeather: {} already set to {}".format(cmd['cmd'],value))
      else:
        self.setDriver(cmd['cmd'], value)
        self.do_weather = True if value == 1 else False
        self.check_weather()

    def cmdSetBacklight(self,cmd):
      self.pushBacklight(cmd['value'])

    def cmdSetBacklightSleep(self,cmd):
      self.pushBacklightSleep(cmd['value'])

    # TODO: This should set the drivers and call pushHold...
    def setPoint(self, cmd):
      LOGGER.debug(cmd)
      coolTemp = self.tempToDriver(self.getDriver('CLISPC'))
      heatTemp = self.tempToDriver(self.getDriver('CLISPH'))
      if 'value' in cmd:
        value = float(cmd['value'])
      else:
        value = 1
      if cmd['cmd'] == 'DIM':
          value = value * -1

      if self.settings['hvacMode'] == 'heat' or self.settings['hvacMode'] == 'auto':
        cmdtype = 'heatTemp'
        driver = 'CLISPH'
        heatTemp += value
        newTemp = heatTemp
      else:
        cmdtype = 'coolTemp'
        driver = 'CLISPC'
        coolTemp += value
        newTemp = coolTemp
      LOGGER.debug('{} {} {} {}'.format(cmdtype, driver, self.getDriver(driver), newTemp))
      #LOGGER.info('Setting {} {} Set Point to {}{}'.format(self.name, cmdtype, cmd['value'], 'C' if self.useCelsius else 'F'))
      if self.ecobeePost(
        {
          "functions": [
            {
              "type":"setHold",
              "params": {
                "holdType":  self.getHoldType(),
                "heatHoldTemp":self.tempToEcobee(heatTemp),
                "coolHoldTemp":self.tempToEcobee(coolTemp),
              }
            }
          ]
        }):
        self.setDriver(driver, newTemp)
        self.setDriver('CLISMD',transitionMap[self.getHoldType()])

    def l_info(self, name, string):
        LOGGER.info("%s:%s:%s: %s" %  (self.id,self.name,name,string))

    def l_error(self, name, string):
        LOGGER.error("%s:%s:%s: %s" % (self.id,self.name,name,string))

    def l_warning(self, name, string):
        LOGGER.warning("%s:%s:%s: %s" % (self.id,self.name,name,string))

    def l_debug(self, name, string):
        LOGGER.debug("%s:%s:%s:%s: %s" % (self.id,self.address,self.name,name,string))

    hint = '0x010c0100'
    commands = { 'QUERY': query,
                'CLISPH': cmdSetPF,
                'CLISPC': cmdSetPF,
                'CLIFS': cmdSetPF,
                'CLIMD': cmdSetMode,
                'CLISMD': cmdSetScheduleMode,
                'GV3': cmdSetClimateType,
                'GV4': cmdSetFanOnTime,
                'GV6': cmdSmartHome,
                'GV7': cmdFollowMe,
                'BRT': setPoint,
                'DIM': setPoint,
                'GV9': cmdSetDoWeather,
                'GV10': cmdSetBacklight,
                'GV11': cmdSetBacklightSleep,
                 }

class Sensor(polyinterface.Node):
    def __init__(self, controller, primary, address, name, id, parent):
      super().__init__(controller, primary, address, name)
      self.type = 'sensor'
      # self.code = code
      self.parent = parent
      self.id = id
      self.drivers = self._convertDrivers(driversMap[self.id]) if self.controller._cloud else deepcopy(driversMap[self.id])

    def start(self):
      self.query()

    def update(self, sensor):
      LOGGER.debug("{}:update:".format(self.address))
      LOGGER.debug("{}:update: sensor={}".format(self.address,sensor))
      updates = {
          'GV1': 2 # Default is N/A
      }
      # Cross reference from sensor capabilty to driver
      xref = {
          'temperature': 'ST',
          'humidity': 'CLIHUM',
          'occupancy': 'GV1',
          'responding': 'GV2'
      }
      for item in sensor['capability']:
          if item['type'] in xref:
              val = item['value']
              if val == "true":
                val = 1
              elif val == "false":
                val = 0
              if item['type'] == 'temperature':
                # temperature unknown seems to mean the sensor is not responding.s
                if val == 'unknown':
                  updates[xref['responding']] = 0
                else:
                  updates[xref['responding']] = 1
                  val = self.parent.tempToDriver(val,True,False)
              if val is not False:
                updates[xref[item['type']]] = val
          else:
            LOGGER.error("{}:update: Unknown capabilty: {}".format(self.address,item))
      LOGGER.debug("{}:update: updates={}".format(self.address,updates))
      for key, value in updates.items():
        self.setDriver(key, value)

    def query(self, command=None):
      self.reportDrivers()

    hint = '0x01030200'
    commands = {'QUERY': query, 'STATUS': query}

class Weather(polyinterface.Node):
    def __init__(self, controller, primary, address, name, useCelsius, forecast):
        super().__init__(controller, primary, address, name)
        self.type = 'forecast' if forecast else 'weather'
        self.forecastNum = 1 if forecast else 0
        self.useCelsius = useCelsius
        self.id = 'EcobeeWeatherC' if self.useCelsius else 'EcobeeWeatherF'
        self.drivers = self._convertDrivers(driversMap[self.id]) if self.controller._cloud else deepcopy(driversMap[self.id])

    def start(self):
        self.query()

    def update(self, weather):
      try:
        currentWeather = weather['forecasts'][self.forecastNum]
      except IndexError:
        LOGGER.error("forcast {} not in weather['forcasts']={}".format(self.forcastNum,weather['forcasts']))
        return
      windSpeed = 0
      if self.type == 'weather' and currentWeather['windSpeed'] == 0 and weather['forecasts'][5]['windSpeed'] > 0:
        windSpeed = weather['forecasts'][5]['windSpeed']
      else:
        windSpeed = currentWeather['windSpeed']

      tempCurrent = currentWeather['temperature'] / 10 if currentWeather['temperature'] != 0 else 0
      tempHeat = currentWeather['tempHigh'] / 10 if currentWeather['tempHigh'] != 0 else 0
      tempCool = currentWeather['tempLow'] / 10 if currentWeather['tempLow'] != 0 else 0
      if self.useCelsius:
        tempCurrent = toC(tempCurrent)
        tempHeat = toC(tempHeat)
        tempCool = toC(tempCool)
      updates = {
        'ST': tempCurrent,
        'GV1': currentWeather['relativeHumidity'],
        'GV2': currentWeather['pop'],
        'GV3': tempHeat,
        'GV4': tempCool,
        'GV5': windSpeed,
        'GV6': windMap[currentWeather['windDirection']],
        'GV7': weather['forecasts'][5]['sky'] if currentWeather['sky'] == -5002 else currentWeather['sky'],
        'GV8': currentWeather['weatherSymbol'],
        'GV9': currentWeather['weatherSymbol']
      }
      for key, value in updates.items():
        self.setDriver(key, value)

    def query(self, command=None):
        self.reportDrivers()

    hint = '0x010b0100'
    commands = {'QUERY': query, 'STATUS': query}
