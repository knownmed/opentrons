from typing import Optional, Dict

from opentrons.drivers.temp_deck.abstract import AbstractTempDeckDriver, Temperature

TEMP_DECK_MODELS = {
    "temperatureModuleV1": "temp_deck_v1.1",
    "temperatureModuleV2": "temp_deck_v20",
}


class SimulatingDriver(AbstractTempDeckDriver):
    def __init__(self, sim_model: str = None):
        self._temp = Temperature(target=None, current=0)
        self._port: Optional[str] = None
        self._model = TEMP_DECK_MODELS[sim_model] if sim_model else "temp_deck_v1.1"

    async def set_temperature(self, celsius: float):
        self._temp.target = celsius
        self._temp.current = self._temp.target

    async def get_temperature(self) -> Temperature:
        return self._temp

    async def deactivate(self):
        self._temp = Temperature(target=None, current=23)

    async def connect(self):
        pass

    async def is_connected(self) -> bool:
        return True

    async def disconnect(self):
        pass

    async def enter_programming_mode(self):
        pass

    async def get_device_info(self) -> Dict[str, str]:
        return {
            "serial": "dummySerialTD",
            "model": self._model,
            "version": "dummyVersionTD",
        }
