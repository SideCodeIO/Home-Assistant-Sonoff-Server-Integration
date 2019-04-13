# how to use
#light:
#  - platform: sonoff
#    host: "192.168.1.11"
#    port: "8089"

import logging

import voluptuous as vol

# Import the device class from the component that you want to support
from homeassistant.components.light import ATTR_BRIGHTNESS, Light, PLATFORM_SCHEMA
from homeassistant.const import CONF_HOST, CONF_PORT, CONF_USERNAME, CONF_PASSWORD
import homeassistant.helpers.config_validation as cv

# Home Assistant depends on 3rd party packages for API specific code.

_LOGGER = logging.getLogger(__name__)

# Validation of the user's configuration
PLATFORM_SCHEMA = PLATFORM_SCHEMA.extend({
    vol.Required(CONF_HOST): cv.string,
    vol.Required(CONF_PORT): cv.string,
    vol.Optional(CONF_USERNAME, default='admin'): cv.string,
    vol.Optional(CONF_PASSWORD): cv.string,
})

from urllib.request import urlopen
import urllib.parse
import json


UPDATE_INTERVAL_SECONDS = 1
_LOGGER = logging.getLogger(__name__)


def setup_platform(hass, config, add_devices, discovery_info=None):
    host = config.get(CONF_HOST)
    port = config.get(CONF_PORT)
    url = "http://" + host + ":" + port
    """Set up the demo light platform."""

    with open('/config/sonoff.ha.json') as f:
        for device in json.loads(f.read()):
            if (device['service'] == "Lightbulb"):
                add_devices([
                    SonoffLights(device['uid'], device['name'],
                                 device['name'], url, True)
                ])


class SonoffLights(Light):
    """Representation of a demo light."""

    def __init__(self, unique_id, name, state, url, available=False):
        """Initialize the light."""
        self._unique_id = unique_id
        self._name = name
        self._state = state
        self._available = available
        self._url = url

    @property
    def name(self):
        """Return the display name of this light."""
        return self._name

    @property
    def is_on(self):
        """Return true if light is on."""
        return self._state

    @property
    def available(self) -> bool:
        """Return availability."""
        # This demo light is always available, but well-behaving components
        # should implement this to inform Home Assistant accordingly.
        return self._available

    @property
    def unique_id(self):
        """Return unique ID for light."""
        return self._unique_id

    @property
    def should_poll(self) -> bool:
        """No polling needed for a demo light."""
        return True

    def turn_on(self, **kwargs):
        """Instruct the light to turn on.

        You can skip the brightness part if your light does not support
        brightness control.
        """
        self._state = True

        _LOGGER.info("on luz")
        # http://192.168.0.14:1081/status/1a19dc9729bd/on
        #fixed to
        # http://192.168.1.11:8088/status/1a19dc9729bd/on

        url = self._url + "/devices/" + self._unique_id + "/on"

        #url = "http://" + self._hub._ip + ":" + str(self._hub._port) + "/homekit"

        f = urllib.request.urlopen(url)
        self.schedule_update_ha_state()

    def turn_off(self, **kwargs):
        """Instruct the light to turn off."""
        self._state = False

        _LOGGER.info("off luz")

        url = self._url + "/devices/" + self._unique_id + "/off"

        #url = "http://" + self._hub._ip + ":" + str(self._hub._port) + "/homekit"

        f = urllib.request.urlopen(url)
        self.schedule_update_ha_state()

    def update(self):
        """Fetch new state data for this light.

        This is the only method that should fetch new data for Home Assistant.
        """
        urlDevices = self._url + "/devices/" + self.unique_id + "/status"
        f = urllib.request.urlopen(urlDevices)
        status = json.loads(f.read().decode('utf-8'))
        self._state = bool(status)