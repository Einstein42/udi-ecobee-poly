

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
  'EcobeeSensorMSD': [
    { 'driver': 'ST', 'value': 0, 'uom': '17' },
  ],
}
