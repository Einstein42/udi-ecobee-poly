import sys
import re
try:
    import polyinterface
except ImportError:
    import pgc_interface as polyinterface
from copy import deepcopy
# For debugging only
import json

LOGGER = polyinterface.LOGGER

modeMap = {
  'off': 0,
  'heat': 1,
  'cool': 2,
  'auto': 3
}

climateMap = {
  'away': 0,
  'home': 1,
  'sleep': 2,
  'smart1': 3,
  'smart2': 4,
  'smart3': 5,
  'smart4': 6,
  'smart5': 7,
  'smart6': 8,
  'smart7': 9,
  'unknown': 10
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

driversMap = {
  'EcobeeF': [
    { 'driver': 'ST', 'value': 0, 'uom': '17' },
    { 'driver': 'CLISPH', 'value': 0, 'uom': '17' },
    { 'driver': 'CLISPC', 'value': 0, 'uom': '17' },
    { 'driver': 'CLIMD', 'value': 0, 'uom': '67' },
    { 'driver': 'CLIHUM', 'value': 0, 'uom': '22' },
    { 'driver': 'CLIHCS', 'value': 0, 'uom': '25' },
    { 'driver': 'CLIFRS', 'value': 0, 'uom': '80' },
    { 'driver': 'GV1', 'value': 0, 'uom': '22' },
    { 'driver': 'CLISMD', 'value': 0, 'uom': '25' },
    { 'driver': 'GV4', 'value': 0, 'uom': '25' },
    { 'driver': 'GV3', 'value': 0, 'uom': '25' },
    { 'driver': 'GV5', 'value': 0, 'uom': '22' },
    { 'driver': 'GV6', 'value': 0, 'uom': '25' },
    { 'driver': 'GV7', 'value': 0, 'uom': '25' }
  ],
  'EcobeeC': [
    { 'driver': 'ST', 'value': 0, 'uom': '4' },
    { 'driver': 'CLISPH', 'value': 0, 'uom': '4' },
    { 'driver': 'CLISPC', 'value': 0, 'uom': '4' },
    { 'driver': 'CLIMD', 'value': 0, 'uom': '67' },
    { 'driver': 'CLIHUM', 'value': 0, 'uom': '22' },
    { 'driver': 'CLIHCS', 'value': 0, 'uom': '25' },
    { 'driver': 'CLIFRS', 'value': 0, 'uom': '80' },
    { 'driver': 'GV1', 'value': 0, 'uom': '22' },
    { 'driver': 'CLISMD', 'value': 0, 'uom': '25' },
    { 'driver': 'GV4', 'value': 0, 'uom': '25' },
    { 'driver': 'GV3', 'value': 0, 'uom': '25' },
    { 'driver': 'GV5', 'value': 0, 'uom': '22' },
    { 'driver': 'GV6', 'value': 0, 'uom': '25' },
    { 'driver': 'GV7', 'value': 0, 'uom': '25' }
  ],
  'EcobeeSensorF': [
    { 'driver': 'ST', 'value': 0, 'uom': '17' },
    { 'driver': 'GV1', 'value': 0, 'uom': '25' }
  ],
  'EcobeeSensorC': [
    { 'driver': 'ST', 'value': 0, 'uom': '4' },
    { 'driver': 'GV1', 'value': 0, 'uom': '25' }
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

def toC(tempF):
  # Round to the nearest .5
  return round(((tempF - 32) / 1.8) * 2) / 2

def toF(tempC):
  # Round to nearest whole degree
  return int(round(tempC * 1.8) + 32)

def getMapName(map,val):
  val = int(val)
  for name in map:
    if int(map[name]) == val:
      return name

"""
 Address scheme:
 Devices: n<profile>_t<thermostatId> e.g. n003_t511892759243
 Thermostat Sensor: n<profile>_s<thermostatId> e.g. n003_s511892759243
 Current Weather: n<profile>_w<thermostatId> e.g. n003_w511892759243
 Forecast Weather: n<profile>_f<thermostatId> e.g. n003_f511892759243
 Sensors: n<profile>_s<sensor code> e.g. n003_rs_r6dr
"""

class Thermostat(polyinterface.Node):
    def __init__(self, controller, primary, address, name, revData, fullData, useCelsius):
        self.controller = controller
        self.name = name
        self.tstat = fullData['thermostatList'][0]
        self.program = self.tstat['program']
        self.settings = self.tstat['settings']
        self.useCelsius = useCelsius
        self.type = 'thermostat'
        self.id = 'EcobeeC' if self.useCelsius else 'EcobeeF'
        self.drivers = self._convertDrivers(driversMap[self.id]) if self.controller._cloud else deepcopy(driversMap[self.id])
        self.revData = revData
        self.fullData = fullData
        super(Thermostat, self).__init__(controller, primary, address, name)

    def start(self):
        if 'remoteSensors' in self.tstat:
            #LOGGER.debug("remoteSensors={}".format(json.dumps(self.tstat['remoteSensors'], sort_keys=True, indent=2)))
            for sensor in self.tstat['remoteSensors']:
                if 'id' in sensor and 'name' in sensor:
                    sensorAddressOld = self.getSensorAddressOld(sensor)
                    sensorAddress = self.getSensorAddress(sensor)
                    # Delete the old one if it exists
                    fnode = self.controller.poly.getNode(sensorAddressOld)
                    if fnode is not False:
                        self.controller.addNotice({fnode['address']: "Sensor created with new name, please delete old sensor with address '{}' in the Polyglot UI.".format(fnode['address'])})
                        self.controller.delNode(fnode['address'])
                    #else:
                    #    self.controller.removeNotice(fnode['address'])
                    if sensorAddress is not None and not sensorAddress in self.controller.nodes:
                        sensorName = 'Ecobee - {}'.format(sensor['name'])
                        self.controller.addNode(Sensor(self.controller, self.address, sensorAddress, sensorName, self.useCelsius))
        if 'weather' in self.tstat:
            weatherAddress = 'w{}'.format(self.address)
            weatherName = 'Ecobee - Weather'
            self.controller.addNode(Weather(self.controller, self.address, weatherAddress, weatherName, self.useCelsius, False))
            forecastAddress = 'f{}'.format(self.address)
            forecastName = 'Ecobee - Forecast'
            self.controller.addNode(Weather(self.controller, self.address, forecastAddress, forecastName, self.useCelsius, True))
        self.update(self.revData, self.fullData)

    def update(self, revData, fullData):
      #LOGGER.debug("fullData={}".format(json.dumps(fullData, sort_keys=True, indent=2)))
      #LOGGER.debug("revData={}".format(json.dumps(revData, sort_keys=True, indent=2)))
      if not 'thermostatList' in fullData:
        LOGGER.error("No thermostatList in fullData={}".format(json.dumps(fullData, sort_keys=True, indent=2)))
        return False
      self.revData = revData
      self.fullData = fullData
      self.tstat = fullData['thermostatList'][0]
      self.settings = self.tstat['settings']
      self.program  = self.tstat['program']
      self.events   = self.tstat['events']
      self._update()

    def _update(self):
      #LOGGER.debug("events={}".format(json.dumps(events, sort_keys=True, indent=2)))
      equipmentStatus = self.tstat['equipmentStatus'].split(',')
      #LOGGER.debug("settings={}".format(json.dumps(self.settings, sort_keys=True, indent=2)))
      runtime = self.tstat['runtime']
      clihcs = 0
      for status in equipmentStatus:
        if status in equipmentStatusMap:
          clihcs = equipmentStatusMap[status]
          break
      # This is what the schedule says should be enabled.
      climateType = self.program['currentClimateRef']
      # And the default mode, unless there is an event
      clismd = 0
      # Is there an active event?
      if len(self.events) > 0 and self.events[0]['type'] == 'hold' and self.events[0]['running']:
        LOGGER.debug("events={}".format(json.dumps(self.events, sort_keys=True, indent=2)))
        # This seems to mean an indefinite hold
        #  "endDate": "2035-01-01", "endTime": "00:00:00",
        if self.events[0]['endTime'] == '00:00:00':
            clismd = transitionMap['indefinite']
        else:
            clismd = transitionMap['nextTransition']
        if self.events[0]['holdClimateRef'] != '':
          climateType = self.events[0]['holdClimateRef']
      tempCurrent = runtime['actualTemperature'] / 10 if runtime['actualTemperature'] != 0 else 0
      tempHeat = runtime['desiredHeat'] / 10
      tempCool = runtime['desiredCool'] / 10
      if (self.useCelsius):
        tempCurrent = toC(tempCurrent)
        tempHeat = toC(tempHeat)
        tempCool = toC(tempCool)
      else:
        # F set points must be integer
        tempHeat = int(float(tempHeat))
        tempCool = int(float(tempCool))

      #LOGGER.debug("program['climates']={}".format(self.program['climates']))
      #LOGGER.debug("settings={}".format(json.dumps(self.settings, sort_keys=True, indent=2)))
      #LOGGER.debug("program={}".format(json.dumps(self.program, sort_keys=True, indent=2)))
      updates = {
        'ST': tempCurrent,
        'CLISPH': tempHeat,
        'CLISPC': tempCool,
        'CLIMD': modeMap[self.settings['hvacMode']],
        'CLIHUM': runtime['actualHumidity'],
        'CLIHCS': clihcs,
        'CLIFRS': 1 if 'fan' in equipmentStatus else 0,
        'GV1': runtime['desiredHumidity'],
        'CLISMD': clismd,
        'GV4': self.settings['fanMinOnTime'],
        'GV3': self.getClimateIndex(climateType),
        'GV5': runtime['desiredDehumidity'],
        'GV6': 1 if self.settings['autoAway'] else 0,
        'GV7': 1 if self.settings['followMeComfort'] else 0
      }
      for key, value in updates.items():
        self.setDriver(key, value)
      for address, node in self.controller.nodes.items():
        if node.primary == self.address and node.type == 'sensor':
          for sensor in self.tstat['remoteSensors']:
            if node.address == self.getSensorAddress(sensor):
              node.update(sensor)
        if node.primary == self.address and (node.type == 'weather' or node.type == 'forecast'):
          weather = self.tstat['weather']
          if weather:
            node.update(weather)

    def getClimateIndex(self,name):
      if name in climateMap:
          climateIndex = climateMap[name]
      else:
          LOGGER.error("Unknown climateType='{}'".format(name))
          climateIndex = climateMap['unknown']
      return climateIndex

    def getSensorAddressOld(self,sdata):
      # return the sensor address from the ecobee api data for one sensor
      if 'id' in sdata:
          return re.sub('\:', '', sdata['id']).lower()[:12]
      return None

    def getSensorAddress(self,sdata):
      # Is it the sensor in the thermostat?
      if sdata['type'] == 'thermostat':
        # Yes, use the thermostat id
        return 's{}'.format(self.tstat['identifier'])
      # No, use the remote sensor code
      return 'rs_{}'.format(sdata['code'].lower())

    def query(self, command=None):
      self.reportDrivers()

    def tempToE(self,temp):
      if self.useCelsius:
        return(toF(float(temp)) * 10)
      return(int(temp) * 10)

    def getHoldType(self,val=None):
      if val is None:
          # They want the current value
          val = self.getDriver('CLISMD')
      # Return the holdType name, if set to Hold, return indefinite
      # Otherwise return nextTransition
      return getMapName(transitionMap,2) if int(val) == 2 else getMapName(transitionMap,1)

    def pushHold(self):
      #
      # Push the current hold info to the thermostat
      # If there is nothing to hold, then cancel it and resume
      #
      push = False
      params = dict()
      params = {
        'holdType': self.getHoldType(),
      }
      # This is what the schedule says should be enabled.
      climateType = self.program['currentClimateRef']
      # This is what is desired
      gv3 = self.getDriver('GV3')
      climateTypeR = getMapName(climateMap,gv3)
      LOGGER.debug("pushHold: climateType={} GV3={}={}".format(climateType,gv3,climateTypeR))
      if climateTypeR == None:
        LOGGER.debug("pushHold: Unknwon climateType index {}".format(gv3))
      elif climateTypeR != climateType:
        params['holdClimateRef'] = climateTypeR
        push = True
      if push:
        command = {
          'functions': [{
            'type': 'setHold',
            'params': params,
          }]
        }
        if self.controller.ecobeePost(self.address, command):
          self.setDriver('CLISMD',transitionMap[self.getHoldType()])
      else:
        LOGGER.debug("pushHold: Nothing to push")

    def cmdSetPoint(self, cmd):
      # Set a hold:  https://www.ecobee.com/home/developer/api/examples/ex5.shtml
      # TODO: Need to check that mode is auto,
      #LOGGER.debug("self.events={}".format(json.dumps(self.events, sort_keys=True, indent=2)))
      #LOGGER.debug("program={}".format(json.dumps(self.program, sort_keys=True, indent=2)))
      driver = cmd['cmd']
      if driver == 'CLISPH':
        cmdtype  = "Heat"
        heatTemp = int(cmd['value'])
        coolTemp = int(self.getDriver('CLISPC'))
      else:
        cmdtype  = "Cool"
        coolTemp = int(cmd['value'])
        heatTemp = int(self.getDriver('CLISPH'))
      LOGGER.info('Setting {} {} Set Point to {}{}'.format(self.name, cmdtype, cmd['value'], 'C' if self.useCelsius else 'F'))
      if self.controller.ecobeePost(self.address,
        {
          "functions": [
            {
              "type":"setHold",
              "params": {
                "holdType":  self.getHoldType(),
                "heatHoldTemp":heatTemp * 10,
                "coolHoldTemp":coolTemp * 10,
              }
            }
          ]
        }):
        self.setDriver(driver, cmd['value'])
        self.setDriver('CLISMD',transitionMap[self.getHoldType()])

    def cmdSetMode(self, cmd):
      if int(self.getDriver(cmd['cmd'])) == int(cmd['value']):
        LOGGER.debug("cmdSetMode: {} already set to {}".format(cmd['cmd'],int(cmd['value'])))
      else:
        name = getMapName(modeMap,int(cmd['value']))
        LOGGER.info('Setting Thermostat {} to mode: {} (value={})'.format(self.name, name, cmd['value']))
        if self.controller.ecobeePost(self.address, {'thermostat': {'settings': {'hvacMode': name}}}):
          self.setDriver(cmd['cmd'], cmd['value'])


    def cmdSetScheduleMode(self, cmd):
      if int(self.getDriver(cmd['cmd'])) == int(cmd['value']):
        LOGGER.debug("cmdSetScheduleMode: {}={} already set to {}".format(cmd['cmd'],self.getDriver(cmd['cmd']),cmd['value']))
      else:
        resume = False
        func = {}
        if int(cmd['value']) == 0:
          func['type'] = 'resumeProgram'
          func['params'] = {
            'resumeAll': False
          }
          resume = True
        else:
          func['type'] = 'setHold'
          heatHoldTemp = int(float(self.getDriver('CLISPH')))
          coolHoldTemp = int(float(self.getDriver('CLISPC')))
          if self.useCelsius:
            headHoldTemp = toF(heatHoldTemp)
            coolHoldTemp = toF(coolHoldTemp)
          func['params'] = {
            'holdType': self.getHoldType(cmd['value']),
            'heatHoldTemp': heatHoldTemp * 10,
            'coolHoldTemp': coolHoldTemp * 10
          }
        if self.controller.ecobeePost(self.address, {'functions': [func]}):
          self.setDriver('CLISMD', int(cmd['value']))
          # Update climate back to schdule when we resume
          if resume:
              self.events = list()
              self._update()

    def cmdSetClimate(self, cmd):
      self.setDriver(cmd['cmd'], cmd['value'])
      self.pushHold()

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
        if self.controller.ecobeePost(self.address, command):
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
        if self.controller.ecobeePost(self.address, command):
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
        if self.controller.ecobeePost(self.address, command):
          self.setDriver(cmd['cmd'], cmd['value'])

    def setPoint(self, cmd):
      LOGGER.debug(cmd)
      coolTemp = float(self.getDriver('CLISPC'))
      heatTemp = float(self.getDriver('CLISPH'))
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
      if self.controller.ecobeePost(self.address,
        {
          "functions": [
            {
              "type":"setHold",
              "params": {
                "holdType":  self.getHoldType(),
                "heatHoldTemp":self.tempToE(heatTemp),
                "coolHoldTemp":self.tempToE(coolTemp),
              }
            }
          ]
        }):
        self.setDriver(driver, newTemp)
        self.setDriver('CLISMD',transitionMap[self.getHoldType()])


    commands = { 'QUERY': query,
                'CLISPH': cmdSetPoint,
                'CLISPC': cmdSetPoint,
                'CLIMD': cmdSetMode,
                'CLISMD': cmdSetScheduleMode,
                'GV3': cmdSetClimate,
                'GV4': cmdSetFanOnTime,
                'GV6': cmdSmartHome,
                'GV7': cmdFollowMe,
                'BRT': setPoint,
                'DIM': setPoint
                 }

class Sensor(polyinterface.Node):
    def __init__(self, controller, primary, address, name, useCelsius):
      super().__init__(controller, primary, address, name)
      self.type = 'sensor'
      # self.code = code
      self.useCelsius = useCelsius
      self.id = 'EcobeeSensorC' if self.useCelsius else 'EcobeeSensorF'
      self.drivers = self._convertDrivers(driversMap[self.id]) if self.controller._cloud else deepcopy(driversMap[self.id])

    def start(self):
      pass

    def update(self, sensor):
      try:
        tempCurrent = int(sensor['capability'][0]['value']) / 10 if int(sensor['capability'][0]['value']) != 0 else 0
      except ValueError as e:
        tempCurrent = 0
      if self.useCelsius:
        tempCurrent = toC(tempCurrent)
      updates = {
        'ST': tempCurrent,
        'GV1': 1 if sensor['capability'][1]['value'] == "true" else 0
      }
      for key, value in updates.items():
        self.setDriver(key, value)

    def query(self, command=None):
      self.reportDrivers()

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
        pass

    def update(self, weather):
      currentWeather = weather['forecasts'][self.forecastNum]
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

    commands = {'QUERY': query, 'STATUS': query}
