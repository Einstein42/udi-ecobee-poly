import sys
import polyinterface
from copy import deepcopy

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
  'custom1': 3,
  'custom2': 4,
  'custom3': 5,
  'custom4': 6,
  'custom5': 7,
  'custom6': 8,
  'custom7': 9,
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

"""
 Address scheme:
 Devices: n<profile>_t<thermostatId> e.g. n003_t511892759243
 Sensors: n<profile>_s<sensor code> e.g. n003_sr6dr
 Current Weather: n<profile>_w<thermostatId> e.g. n003_w511892759243
 Forecast Weather: n<profile>_f<thermostatId> e.g. n003_f511892759243
"""

class Thermostat(polyinterface.Node):
    def __init__(self, controller, primary, address, name, revData, fullData, useCelsius):
        super().__init__(controller, primary, address, name)
        self.controller = controller
        self.name = name
        self.tstat = fullData['thermostatList'][0]
        self.program = self.tstat['program']
        self.settings = self.tstat['settings']
        self.useCelsius = useCelsius
        self.type = 'thermostat'
        self.id = 'EcobeeC' if self.useCelsius else 'EcobeeF'
        self.drivers = driversMap[self.id]
        self.revData = revData
        self.fullData = fullData
        
    def start(self):
        self.update(self.revData, self.fullData)

    def update(self, revData, fullData):
      self.revData = revData
      self.fullData = fullData
      self.tstat = fullData['thermostatList'][0]
      self.program = self.tstat['program']
      events = self.tstat['events']
      equipmentStatus = self.tstat['equipmentStatus'].split(',')
      self.settings = self.tstat['settings']
      runtime = self.tstat['runtime']
      clihcs = 0
      for status in equipmentStatus:
        if status in equipmentStatusMap:
          clihcs = equipmentStatusMap[status]
          break
      clismd = 0
      if len(events) > 0 and events[0]['type'] == 'hold' and events[0]['running']:
        clismd = 1 if self.settings['holdAction'] == 'nextPeriod' else 2
      tempCurrent = runtime['actualTemperature'] / 10 if runtime['actualTemperature'] != 0 else 0
      tempHeat = runtime['desiredHeat'] / 10
      tempCool = runtime['desiredCool'] / 10
      if (self.useCelsius):
        tempCurrent = toC(tempCurrent)
        tempHeat = toC(tempHeat)
        tempCool = toC(tempCool)
      
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
        'GV3': climateMap[self.program['currentClimateRef']],
        'GV5': runtime['desiredDehumidity'],
        'GV6': 1 if self.settings['autoAway'] else 0,
        'GV7': 1 if self.settings['followMeComfort'] else 0
      }
      for key, value in updates.items():
        self.setDriver(key, value)
      for address, node in self.controller.nodes.items():
        if node.primary == self.address and node.type == 'sensor':
          for sensor in self.tstat['remoteSensors']:
            if 'code' in sensor and node.code == sensor['code']:
              node.update(sensor)
        if node.primary == self.address and (node.type == 'weather' or node.type == 'forecast'):
          weather = self.tstat['weather']
          if weather:
            node.update(weather)

    def query(self, command=None):
        self.reportDrivers()

    def cmdSetPoint(self, cmd):
      if cmd['cmd'] == 'CLISPH':
        cmdtype = 'heatTemp'
        driver = 'CLISPH'
      else:
        cmdtype = 'coolTemp'
        driver = 'CLISPC'
      LOGGER.info('Setting {} {} Set Point to {}{}'.format(self.name, cmdtype, cmd['value'], 'C' if self.useCelsius else 'F'))
      currentProgram = deepcopy(self.program)
      for climate in currentProgram['climates']:
        if climate['climateRef'] == currentProgram['currentClimateRef']:
          if self.useCelsius:
              climate[cmdtype] = toF(float(cmd['value'])) * 10
          else:
            climate[cmdtype] = int(cmd['value']) * 10
          if self.controller.ecobeePost(self.address, {'thermostat': {'program': currentProgram}}):
            self.setDriver(driver, cmd['value'])

    def cmdSetMode(self, cmd):
      if self.getDriver(cmd['cmd']) != cmd['value']:
        LOGGER.info('Setting Thermostat {} to mode: {}'.format(self.name, [*modeMap][int(cmd['value'])]))
        if self.controller.ecobeePost(self.address, {'thermostat': {'settings': {'hvacMode': [*modeMap][int(cmd['value'])]}}}):
          self.setDriver(cmd['cmd'], cmd['value'])

    def cmdSetScheduleMode(self, cmd):
      if self.getDriver(cmd['cmd']) != cmd['value']:
        func = {}
        if cmd['value'] == '0':
          func['type'] = 'resumeProgram'
          func['params'] = {
            'resumeAll': False
          }
        else:
          func['type'] = 'setHold'
          heatHoldTemp = int(self.getDriver('CLISPH'))
          coolHoldTemp = int(self.getDriver('CLISPH'))
          if self.useCelsius:
            headHoldTemp = toF(heatHoldTemp)
            coolHoldTemp = toF(coolHoldTemp)
          func['params'] = {
            'holdType': 'nextTransition' if cmd['value'] == "1" else 'indefinite',
            'heatHoldTemp': heatHoldTemp * 10,
            'coolHoldTemp': coolHoldTemp * 10
          }
        if self.controller.ecobeePost(self.address, {'functions': [func]}):
          self.setDriver('CLISMD', cmd['value'])

    def cmdSetClimate(self, cmd):
      if self.getDriver(cmd['cmd']) != cmd['value']:
        command = {
          'functions': [{
            'type': 'setHold',
            'params': {
              'holdType': 'indefinite',
              'holdClimateRef': [*climateMap][int(cmd['value'])]
            }
          }]
        }
        if self.controller.ecobeePost(self.address, command):
          self.setDriver(cmd['cmd'], cmd['value'])

    def cmdSetFanOnTime(self, cmd):
      if self.getDriver(cmd['cmd']) != cmd['value']:
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
      if self.getDriver(cmd['cmd']) != cmd['value']:
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
      if self.getDriver(cmd['cmd']) != cmd['value']:
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
      currentProgram = deepcopy(self.program)
      for climate in currentProgram['climates']:
        if climate['climateRef'] == currentProgram['currentClimateRef']:
          cmdtype = 'coolTemp'
          driver = 'CLISPC'
          value = 1
          if self.settings['hvacMode'] == 'heat' or self.settings['hvacMode'] == 'auto':
            cmdtype = 'heatTemp'
            driver = 'CLISPH'
          currentValue = float(self.getDriver(driver))
          if 'value' in cmd:
            value = float(cmd['value'])
          if cmd['cmd'] == 'BRT':
            newTemp = currentValue + value
          else:
            newTemp = currentValue - value
          if self.useCelsius:
              climate[cmdtype] = toF(float(newTemp)) * 10
          else:
            climate[cmdtype] = int(newTemp) * 10
          LOGGER.debug('{} {} {} {} {}'.format(cmdtype, driver, self.getDriver(driver), newTemp, climate[cmdtype]))
          if self.controller.ecobeePost(self.address, {'thermostat': {'program': currentProgram}}):
            self.setDriver(driver, newTemp)

    def getDriver(self, driver):
      for item in self.drivers:
        if item['driver'] == driver:
          return item['value']

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
    def __init__(self, controller, primary, address, name, code, useCelsius):
      super().__init__(controller, primary, address, name)
      self.type = 'sensor'
      self.code = code
      self.useCelsius = useCelsius
      self.id = 'EcobeeSensorC' if self.useCelsius else 'EcobeeSensorF'
      self.drivers = driversMap[self.id]
        
    def start(self):
      pass

    def update(self, sensor):
      tempCurrent = int(sensor['capability'][0]['value']) / 10 if int(sensor['capability'][0]['value']) != 0 else 0
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

    commands = {}

class Weather(polyinterface.Node):
    def __init__(self, controller, primary, address, name, useCelsius, forecast):
        super().__init__(controller, primary, address, name)
        self.type = 'forecast' if forecast else 'weather'
        self.forecastNum = 1 if forecast else 0
        self.useCelsius = useCelsius
        self.id = 'EcobeeWeatherC' if self.useCelsius else 'EcobeeWeatherF'
        self.drivers = driversMap[self.id]
        
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

    commands = {}