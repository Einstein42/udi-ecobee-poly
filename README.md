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

## Monitoring

See https://forum.universal-devices.com/topic/25016-polyglot-nodeserver-monitoring/ for info on how to use the heartbeats.  You can also check the thermostat GV8 True/False to see if the Ecobee servers can see the thermostats.

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

- 2.0.27: JimBo
  - [Issue with custom climate names](https://github.com/Einstein42/udi-ecobee-poly/issues/32)
- 2.0.26: JimBo
  - Changed logic for adding sensors and checking sensor updates, so we know if there is a problem with sensor not found
- 2.0.25: JimBo
  - Build the profile before adding any nodes, shouldn't make any difference, but is just the right thing to do.
- 2.0.24: JimBo
  - Set Fan State on when manually turned on and off when Climate Type = Resume, will get updated on next long poll if not the actual status.
- 2.0.23: JimBo
  - [Add heartbeat](https://github.com/Einstein42/udi-ecobee-poly/issues/29)
    - See https://forum.universal-devices.com/topic/25016-polyglot-nodeserver-monitoring/ for info on how to use it.
- 2.0.22: JimBo
  - [Ecobee server issues caused nodeserver to hang](https://github.com/Einstein42/udi-ecobee-poly/issues/28)
    - More trapping
  - [Set Fan driver on/off based on heat setting when fanControlRequired setting](https://github.com/Einstein42/udi-ecobee-poly/issues/25)
    - Should actually work this time.
- 2.0.21: JimBo
  - [Ecobee server issues caused nodeserver to hang](https://github.com/Einstein42/udi-ecobee-poly/issues/28)
    - Not a sure fix, but should improve stablity.
  - [Add control of fan on/auto state](https://github.com/Einstein42/udi-ecobee-poly/issues/23)
  - [Set Fan driver on/off based on heat setting when fanControlRequired setting](https://github.com/Einstein42/udi-ecobee-poly/issues/25)
- 2.0.20: JimBo
  - Fix for old Ecobee's that don't have the same sensor data.
- 2.0.19: JimBo
  - Fix bug when installing
- 2.0.18: JimBo
  - Support sensors with or without Humidity
  - Fix Sensor update to not report drivers on every check.  Will reduce a lot of updates to ISY.
- 2.0.17: JimBo
  - Add Connected to Thermostat, set to False when Ecobee servers can't see the Thermostat
  - Fix crash where Sensor temp was 'unknown' when it hasn't reported yet
  - Fix bug where profile is not rebuilt when a climate name is Changed
  - If an invalid climate type is somehow selected, meaning it isn't named in the app, then smart<n> is shown.  I can't figure out how this can happen, but seems possible.
- 2.0.16: JimBo
  - Fix issues with custom climate types for mutliple thermostats
- 2.0.15: JimBo
  - [Add support for custom named climate type's](https://github.com/Einstein42/udi-ecobee-poly/issues/1)
    - With this change the custom Climate Types (Comfort Settings) names you have created in the thermostat will show up on the ISY, but this means that during discover it will build custom profiles that will be loaded and will require the admin console to be closed if it's open.
- 2.0.14: JimBo
  - [When I select hold-indefinite on schedule mode, it sets the heat setpoint to 26 degrees C and holds it there indefinitely.](https://github.com/Einstein42/udi-ecobee-poly/issues/16)
  - [Temperature is being displayed in the console in deg F (even though it says deg C)](https://github.com/Einstein42/udi-ecobee-poly/issues/17)
  - [The Occupancy variable does change for the the satellite sensors, but not for the thermostats itself.](https://github.com/Einstein42/udi-ecobee-poly/issues/18)
    - Also added Humidity support to sensors, which will show up after restarting the nodeserver and restarting admin console.
- 2.0.13: JimBo
  - Reorganize hold functions for changing setpoints, climate type, ...
  - Fix Illegal node names
  - More trapping of bad return data from Ecobee servers
  - More debugging info to find issues
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
