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

## Node info

1. Controller node - Nodeserver Online
   * The Nodeserver process status
1. Controller node - Ecobee Connection Status
   * The Nodeserver communication to the Ecobee server status.
1. Main thermostat node (n00x_t) - Connected
   * The Ecobee servers can see the thermostat
1. Main thermostat sensor node (n00x_s) - Responding
   * Probably node needed since main sensor is inside the thermostat
1. Remote sensor node (n00x_rs) - Responding
   * The thermostat can see the sensor, this going False can indicate dead battery or out-of-range.

## Monitoring

See https://forum.universal-devices.com/topic/25016-polyglot-nodeserver-monitoring/ for info on how to use the heartbeats.  You can also check the thermostat GV8 True/False to see if the Ecobee servers can see the thermostats.

## Upgrading

When a new release is published, it should be released to the polyglot web store within an hour, currently around 40 minutes past the hour.

1. Open the Polyglot web page
  1. Go to nodeserver store and click "Update" for "Ecobee"
  1. Wait for the update completed notice
  1. Go to the dashboard, select Details for the Ecobee Nodeserver
  1. Click Restart
1. If the release has a (Profile Change) then the profile will be updated automatically but if you had the Admin Console open, you will need to close and open it again.

### Manual Upgrade

If you already have it installed and want the update before it's in the store.
1. Polisy: cd /var/spolyglot/nodeservers/Ecobee
1. Others: cd ~/.polyglot/nodeservers/Ecobee
1. git pull
1. Go to the polyglot dashboard, select Details for the Ecobee Nodeserver
1. Click Restart

## Release Notes

- 2.1.32: JImBo 11/14/2020
  - Fix syntax error in last release when token is expired on startup.
- 2.1.31: JimBo 11/14/2020
  - Don't force user reauthorization when invalid_grant is returned and token has not expired.  This is to hopefully get around the issue where Ecobee servers return invalid_grant when it's really not.  Ecobee support is no longer responding to us for help on this issue.
- 2.1.30: JimBo 09/13/2020
  - Temporary fix for https://github.com/Einstein42/udi-ecobee-poly/issues/60
    - May have to update after hearing back from Ecobee.
- 2.1.29: JimBo 09/11/2020
  - Fix bug introduced in previous version that only affects a new install
  - Also fix ecobee login url
- 2.1.28: JimBo 09/09/2020
  - Change timeout from 60 to 10,61 to see if that stops read timeout issue
  - Also added connect retries
- 2.1.27: JimBo 09/07/2020
  - More fixes for https://github.com/Einstein42/udi-ecobee-poly/issues/57
    - Clean up DB lock/unlock more
    - Add retry if save custom data doesn't seem to happen
    - Set Auth driver to False to trigger programs
- 2.1.26: JimBo 09/06/2020
  - Enhance Fix for https://github.com/Einstein42/udi-ecobee-poly/issues/57
    - Add timeout in saveCustomDataWait method
- 2.1.25: JimBo 09/04/2020
  - Enhance Fix for https://github.com/Einstein42/udi-ecobee-poly/issues/57
    - To workaround possible DB write order issue, do not continue until DB data is confirmed to be saved when locking/unlocking
- 2.1.24: JimBo 08/30/2020
  - Fix for https://github.com/Einstein42/udi-ecobee-poly/issues/57
- 2.1.23: JImBo 06/06/2020
  - Fix to not set auth status False when starting refresh
- 2.1.22: JimBo 06/05/2020
  - Refresh token before it expires,
  - Don't save tokenData in customData because it will increase PGC cost.
- 2.1.21: JimBo 06/04/2020
  - Fix crash for another authentication issue.
- 2.1.20: JimBo 06/03/2020
  - Print msg to log when requesting a pin in case it doesn't show up in Polyglot UI
  - Print customData on restart
  - Store current nodeserver version in customData for reference
  - Increase waitingOnPin sleep time to 30 and increment by 30 on each loop up to 180
- 2.1.19: JimBo 05/26/2020
  - Fix another crash when Ecobee servers are not responding
- 2.1.18: JimBo 05/07/20202
  - When refresh_token goes missing, force a reAuth.  No idea how that happens, but we can track it now.
- 2.1.17: JimBo 05/07/2020
  - Keep track of old tokenData when it becomes invalid, along with the reason in the DB.
- 2.1.16: JimBo 03/17/2020
  - Fix for https://github.com/Einstein42/udi-ecobee-poly/issues/52
- 2.1.15: JimBo 02/06/2020
  - Add fix for https://github.com/Einstein42/udi-ecobee-poly/issues/51 not fully tested since I can't repeat, but should trap the error.
- 2.1.14: JimBo 02/02/2020
  - Add Support for auxHeat https://github.com/Einstein42/udi-ecobee-poly/issues/50
  - profile update required, must restart AC after retarting Nodeserver
- 2.1.13: JimBo 09/09/2019
  - Fix issue with new installs where profile/nls didn't exist on initial start
- 2.1.12: JimBo 09/08/2019
  - Added simple fix for [ClimateType of 'wakeup' not found, halts further processing](https://github.com/Einstein42/udi-ecobee-poly/issues/46)
  - Proper fix is defered for later [climateList should be pulled from API](https://github.com/Einstein42/udi-ecobee-poly/issues/47)
  - New profile will be generated on restart, make sure to close and re-open admin console
- 2.1.11: JimBo 06/19/2019
  - Better trapping for expired tokens
- 2.1.10: JimBo 05/09/2019
  - Ignore socket not closed warnings (hopefully for @larryllix)
- 2.1.9: JimBo 05/05/2019
  - Fixed backlightSleepIntensity
- 2.1.8: JimBo 04/23/2019
  - Add backlightSleepIntensity
- 2.1.7: JimBo 04/22/2019
  - Add Upload Profile to Controller, should never be needed, but just in case.
- 2.1.6: JimBo
  - [Crash due to bad json returned from Ecobee](https://github.com/Einstein42/udi-ecobee-poly/issues/45)
- 2.1.5: JimBo
  - [Crash due to bad json returned from Ecobee](https://github.com/Einstein42/udi-ecobee-poly/issues/45)
  - [Not properly recognizing expired token response?](https://github.com/Einstein42/udi-ecobee-poly/issues/44)
  - [Track Vacation along with Smart Home/Away](https://github.com/Einstein42/udi-ecobee-poly/issues/31)
    - Properly support Vacation, SmartAway, SmartHome and DemandResponse Events in 'Climate Type'
  - [Support changing backlightOnIntensity](https://github.com/Einstein42/udi-ecobee-poly/issues/42)
- 2.1.4: JimBo
  - [Crash due to bad json returned from Ecobee](https://github.com/Einstein42/udi-ecobee-poly/issues/45)
- 2.1.3: JimBo
  - More fixing flakey Ecobee servers.
- 2.1.2: JimBo
  - Fix re-authorization, but can not completely verify because Ecobee site is flakey.
- 2.1.1: JimBo
  - [Add setting to include/exclude weather and forcast](https://github.com/Einstein42/udi-ecobee-poly/issues/40)
- 2.1.0: JimBo
  - Changed communcation with Ecobee to use sessions.  This has fixed the hanging issue and made network connections to Ecobee servers more robust.
  - Added logger level to controller which defaults to warning, however polyglot doesn't udpate the DB so it's not changeable from the ISY until this magically happens, not sure when.
- 2.0.39: JimBo
  - Add more debugging to see where hang is happening
- 2.0.38: JimBo
  - Fixed typo when initial discover fails.
- 2.0.37: JimBo
  - Trap any error in discover in case Ecobee servers are not responding when starting up, and we hit an error that is not being trapped.
- 2.0.36: JimBo
  - [Trap: ConnectionResetError: [Errno 104] Connection reset by peer](https://github.com/Einstein42/udi-ecobee-poly/issues/39)
- 2.0.35: JimBo
  - Fix initialization of "Ecobee Connection Status".  Try to set it to False on exit, but doesn't work due to polyglot issue.
  - Add debug in getThermostatSelection to see where it's hanging
- 2.0.34: JimBo
  - [AttributeError: 'Controller' object has no attribute 'revData'](https://github.com/Einstein42/udi-ecobee-poly/issues/36)
  - Send Heartbeat on startup
- 2.0.33: JimBo
  - Fix another crash from Ecobee server returning bad json data.
- 2.0.32: JimBo
  - [Fix issue with unknown remote sensor temperature](https://github.com/Einstein42/udi-ecobee-poly/issues/35)
  - [AttributeError: 'Controller' object has no attribute 'revData'](https://github.com/Einstein42/udi-ecobee-poly/issues/36)
  - [Thermostat connected not updated when service is down](https://github.com/Einstein42/udi-ecobee-poly/issues/37)
- 2.0.31: JimBo
  - Add Poll on controller to grab all current settings, and query to just report the currently known drivers values to the isy.
  - Fix another issue found when Ecobee servers are not responding.
- 2.0.30: JimBo
  - Fix for Hold Type names in Climate Control program action.  Although, they don't actually work yet in Polyglot, so you have to set Hold Type in another Action.
- 2.0.29: JimBo
  - Added back fix for checking sensors from 2.0.26 that git merge decided to get rid of.
- 2.0.28: JimBo
  - Added vacation mode tracking as a Climate Type for [Track Vacation along with Smart Home/Away](https://github.com/Einstein42/udi-ecobee-poly/issues/31)
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
