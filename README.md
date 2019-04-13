# Home Assistant (Hass.io) Sonoff Server Integration

Current State => Tested and Working with Sonoff Duel.
Compatible with this Sonoff Private server: https://github.com/SideCodeIO/Sonoff-Server

This repo is about how to integrate Hass (Home Assistant) with Sonoff devices that are on a private Sonoff server) and define them as light switches (as a custom component).

There is no need to flash the sonoff devices, but you will need to control them via a private sonoff server.

This component is compatible and tested with this sonoff private server:
https://github.com/SideCodeIO/Sonoff-Server
Tested with Home Assistant running under docker.
Tested with Sonoff Dual devices.

Once integrated as a "light" inside Hass, you can fully control it with Hass.


A lot of this code is based on the findings and code from these sources:
* https://github.com/mdopp/simple-sonoff-server (mdopp)
* https://gist.github.com/gerswin/0cac4f8df4a947b0fec196b84a5e8d8b (gerswin)





# Configuration
- Create a custom_components under your /config folder.
- Copy the sonoff folder to your /config/custom_components folder.
- Copy the config.hs.json into your config folder.

- Add to configuration.yaml:
```yaml

light:
 - platform: sonoff
   host: "192.168.1.11"
   port: "8088"

``` 
host - is sonoff_server ip (localhost or under docker/diffrent device than the ip of the device/server).
port - is your sonof server http port.


- Add to your sonoff.ha.json file all of your sonoff devices with their device_id. 
  In my case it was a sonoff dual, each channel is a "device", with device_id-0 or device_id-1

 - you can check your device ids via sonof_server SERVER_IP:SERVER_HTTP_PORT/devices route. 
   In my case it was: http://192.168.1.11:8088/devices

- Restart Hass.

- Now you should see in the Panel under Configuration > Entity Registry
all your sonoff devices as lights of type sonoff.

