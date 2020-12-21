

try:
    from polyinterface import Node,LOGGER
except ImportError:
    from pgc_interface import Node,LOGGER
    
from copy import deepcopy
from const import driversMap,windMap

class Weather(Node):
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
        LOGGER.error("Weather can not update no weather['forecasts'][{}] in weather={}".format(self.forecastNum,weather))
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
