import aiohttp
from imouapi.api import ImouAPIClient
import asyncio
import logging
from imouapi.api import ImouAPIClient
from imouapi.device_entity import ImouCamera
from imouapi.device import ImouDiscoverService
from imouapi.const import ONLINE_STATUS
from imouapi.exceptions import APIError

logging.basicConfig(level=logging.DEBUG)
_LOGGER = logging.getLogger(__name__)



async def get_online_devices():
    # Initialize the API client
    api_client = ImouAPIClient(app_id='', app_secret='', session=aiohttp.ClientSession())

    # Create the discover service
    discover_service = ImouDiscoverService(api_client)
    devices = await discover_service.async_discover_devices()
    for name, device in devices.items():
        cameras = device.get_sensors_by_platform('camera')
        for camera in cameras:
            print(await camera.async_get_stream_url())


    # Discover devices
    # devices = await discover_service.discover_devices()

    # for device_name, device in devices.items():
    #     # Refresh the status of the device
    #     await device.async_refresh_status()
    #
    #     # Check if the device is online
    #     if device.is_online():
    #         _LOGGER.info(f"Device {device_name} is online.")
    #
    #         # If the device is a camera, get the live stream URL
    #         if isinstance(device, ImouCamera):
    #             stream_url = await device.async_get_stream_url()
    #             _LOGGER.info(f"Live stream URL for {device_name}: {stream_url}")

# createDeviceRtmpLive
# Run the async function
asyncio.run(get_online_devices())
