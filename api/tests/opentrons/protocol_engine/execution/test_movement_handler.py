"""Pipetting command handler."""
import pytest
from decoy import Decoy

from opentrons.types import MountType, Mount, Point
from opentrons.hardware_control.api import API as HardwareAPI
from opentrons.hardware_control.types import CriticalPoint
from opentrons.motion_planning import Waypoint

from opentrons.protocol_engine import WellLocation, WellOrigin
from opentrons.protocol_engine.state import StateStore, PipetteLocationData, CurrentWell
from opentrons.protocol_engine.execution.movement import MovementHandler


@pytest.fixture
def hardware_api(decoy: Decoy) -> HardwareAPI:
    """Get a mock in the shape of a HardwareAPI."""
    return decoy.mock(cls=HardwareAPI)


@pytest.fixture
def state_store(decoy: Decoy) -> StateStore:
    """Get a mock in the shape of a StateStore."""
    return decoy.mock(cls=StateStore)


@pytest.fixture
def handler(state_store: StateStore, hardware_api: HardwareAPI) -> MovementHandler:
    """Create a PipettingHandler with its dependencies mocked out."""
    return MovementHandler(state_store=state_store, hardware_api=hardware_api)


async def test_move_to_well(
    decoy: Decoy,
    state_store: StateStore,
    hardware_api: HardwareAPI,
    handler: MovementHandler,
) -> None:
    """Move requests should call hardware controller with movement data."""
    well_location = WellLocation(origin=WellOrigin.BOTTOM, offset=(0, 0, 1))

    decoy.when(
        state_store.motion.get_pipette_location(
            pipette_id="pipette-id",
            current_well=None,
        )
    ).then_return(
        PipetteLocationData(
            mount=MountType.LEFT,
            critical_point=CriticalPoint.FRONT_NOZZLE,
        )
    )

    decoy.when(
        await hardware_api.gantry_position(
            mount=Mount.LEFT,
            critical_point=CriticalPoint.FRONT_NOZZLE,
        )
    ).then_return(Point(1, 1, 1))

    decoy.when(hardware_api.get_instrument_max_height(mount=Mount.LEFT)).then_return(
        42.0
    )

    decoy.when(
        state_store.motion.get_movement_waypoints(
            origin=Point(1, 1, 1),
            origin_cp=CriticalPoint.FRONT_NOZZLE,
            max_travel_z=42.0,
            pipette_id="pipette-id",
            labware_id="labware-id",
            well_name="B2",
            well_location=well_location,
            current_well=None,
        )
    ).then_return(
        [Waypoint(Point(1, 2, 3), CriticalPoint.XY_CENTER), Waypoint(Point(4, 5, 6))]
    )

    await handler.move_to_well(
        pipette_id="pipette-id",
        labware_id="labware-id",
        well_name="B2",
        well_location=well_location,
    )

    decoy.verify(
        await hardware_api.move_to(
            mount=Mount.LEFT,
            abs_position=Point(1, 2, 3),
            critical_point=CriticalPoint.XY_CENTER,
        ),
        await hardware_api.move_to(
            mount=Mount.LEFT, abs_position=Point(4, 5, 6), critical_point=None
        ),
    )


async def test_move_to_well_from_starting_location(
    decoy: Decoy,
    state_store: StateStore,
    hardware_api: HardwareAPI,
    handler: MovementHandler,
) -> None:
    """It should be able to move to a well from a start location."""
    well_location = WellLocation(origin=WellOrigin.BOTTOM, offset=(0, 0, 1))

    current_well = CurrentWell(
        pipette_id="pipette-id",
        labware_id="labware-id",
        well_name="B2",
    )

    decoy.when(
        state_store.motion.get_pipette_location(
            pipette_id="pipette-id",
            current_well=current_well,
        )
    ).then_return(
        PipetteLocationData(
            mount=MountType.RIGHT,
            critical_point=CriticalPoint.XY_CENTER,
        )
    )

    decoy.when(
        await hardware_api.gantry_position(
            mount=Mount.RIGHT,
            critical_point=CriticalPoint.XY_CENTER,
        )
    ).then_return(Point(1, 2, 5))

    decoy.when(hardware_api.get_instrument_max_height(mount=Mount.RIGHT)).then_return(
        42.0
    )

    decoy.when(
        state_store.motion.get_movement_waypoints(
            current_well=current_well,
            origin=Point(1, 2, 5),
            origin_cp=CriticalPoint.XY_CENTER,
            max_travel_z=42.0,
            pipette_id="pipette-id",
            labware_id="labware-id",
            well_name="B2",
            well_location=well_location,
        )
    ).then_return([Waypoint(Point(1, 2, 3), CriticalPoint.XY_CENTER)])

    await handler.move_to_well(
        pipette_id="pipette-id",
        labware_id="labware-id",
        well_name="B2",
        well_location=well_location,
        current_well=current_well,
    )

    decoy.verify(
        await hardware_api.move_to(
            mount=Mount.RIGHT,
            abs_position=Point(1, 2, 3),
            critical_point=CriticalPoint.XY_CENTER,
        ),
    )
