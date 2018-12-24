# Ecobee Poly

## Installation

Install through the NodeServer Store

### Initial setup

1. On first start up you will be given a PIN.
1. Login to the Ecobee web page, click on your profile, then click 'My Apps' > 'Add Application'.
1. You will be prompted to enter the PIN provided.
1. The nodeserver will check every 60 seconds that you have completed the approval so do not restart the nodeserver. You can monitor the log to see when the approval is recognized.
1. Your thermostat will be added to ISY, along with nodes for any sensors, a node for the current weather, and a node for the forecast.

After the first run. It will refresh any changes every 3 minutes. This is
a limitation imposed by Ecobee.

## Settings

- The "Schedule Mode" is one of
  1. Running
  1. Hold Next
  1. Hold Indefinite
  If this is changed to either Hold settings then the current Cool/Heat and Fan modes are sent with that Hold type.  If Running is selected then any Holds are cancelled.

## Upgrading

1. Open the Polyglot web page
  1. Go to nodeserver store and click "Update" for "Ecobee"
  1. Wait for the update completed notice
  1. Go to the dashboard, select Details for the Ecobee Nodeserver
  1. Click Restart
1. If the release has a (Profile Change) then the profile will be updated automatically but if you had the Admin Console open, you will need to close and open it again.

### Manual Upgrade

If you already have it installed and want the update before it's in the store.
1. cd ~/.polyglot/nodeservers/Ecobee
1. git pull
1. Go to the polyglot dashboard, select Details for the Ecobee Nodeserver
1. Click Restart

## Release Notes

- 2.0.12: JimBo
  - Fix for polling not working
  - Many changes to how hold's are handled, should be more reliable
- 2.0.11: JimBo
  - Thermostat address starts with 't', existing users will need to delete the old node after fixing their programs to reference the new one.
- 2.0.10: JimBo
  - Changed setpoint up/down (BRT/DIM) to change as a hold nextTransition instead of changing the program setpoint
  - Better trapping of issues when Ecobee servers are not responding
- 2.0.9: JimBo
  - Should now be properly tracking all status when going in and out of holds.
- 2.0.8: JimBo
  - Shortend names of Sensor, Weather, and Forcast nodes.
    - Existing users will have to delete the current nodes in the Polyglot UI to get the new names, or just rename them yourself.
- 2.0.7: JimBo
  - [Changing setpoint when program running changes the actual "comfort setting"](https://github.com/Einstein42/udi-ecobee-poly/issues/6)
    - See Notes above in Settings for "Schedule Mode"
  - [Schedule Mode crash ValueError: invalid literal for int() with base 10](https://github.com/Einstein42/udi-ecobee-poly/issues/10)
  - [Setting 'Climate Type' sets hold as indefinite, should it use nextTransition?](https://github.com/Einstein42/udi-ecobee-poly/issues/9)
    - It will now use the current set "Schedule Mode"
  - [Move creating Thermostat child nodes into Thermostat](https://github.com/Einstein42/udi-ecobee-poly/issues/7)
  - [Sensor ID's are not unique when you have multiple thermostats](https://github.com/Einstein42/udi-ecobee-poly/issues/2)
    - The new sensor nodes will be created when the nodeserver is restarted.
    - IMPORTANT: Please delete the nodes from within the Polyglot UI after changing any programs that may reference the old ones.
- 2.0.6: JimBo
  - [Fix lookup for setting Mode](https://github.com/Einstein42/udi-ecobee-poly/issues/4)
  - [Fix crash when changing schedule mode](https://github.com/Einstein42/udi-ecobee-poly/issues/5)
  - Fix "Climate Type" initialization when there is a manual change
  - Automatically upload new profile when it is out of date.
  - Change current temp for F to include one signficant digit, since that's what is sent.
