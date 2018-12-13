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

## Release Notes

- 2.0.7: JimBo
  - [Changing setpoint when program running changes the actual "comfort setting"](https://github.com/Einstein42/udi-ecobee-poly/issues/6)
    - See Notes above in Settings for "Schedule Mode"
- 2.0.6: JimBo
  - [Fix lookup for setting Mode](https://github.com/Einstein42/udi-ecobee-poly/issues/4)
  - [Fix crash when changing schedule mode](https://github.com/Einstein42/udi-ecobee-poly/issues/5)
  - Fix "Climate Type" initialization when there is a manual change
  - Automatically upload new profile when it is out of date.
  - Change current temp for F to include one signficant digit, since that's what is sent.
