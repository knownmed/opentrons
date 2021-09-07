"""Test load labware commands."""
from decoy import Decoy

from opentrons.types import DeckSlotName
from opentrons.protocols.models import LabwareDefinition
from opentrons.protocol_engine.types import DeckSlotLocation
from opentrons.protocol_engine.execution import (
    LoadedLabwareData,
    EquipmentHandler,
    MovementHandler,
    PipettingHandler,
    RunControlHandler,
)
from opentrons.protocol_engine.commands.load_labware import (
    LoadLabwareData,
    LoadLabwareResult,
    LoadLabwareImplementation,
)


async def test_load_labware_implementation(
    decoy: Decoy,
    well_plate_def: LabwareDefinition,
    equipment: EquipmentHandler,
    movement: MovementHandler,
    pipetting: PipettingHandler,
    run_control: RunControlHandler,
) -> None:
    """A LoadLabware command should have an execution implementation."""
    subject = LoadLabwareImplementation(
        equipment=equipment,
        movement=movement,
        pipetting=pipetting,
        run_control=run_control,
    )

    data = LoadLabwareData(
        location=DeckSlotLocation(slot=DeckSlotName.SLOT_3),
        loadName="some-load-name",
        namespace="opentrons-test",
        version=1,
    )

    decoy.when(
        await equipment.load_labware(
            location=DeckSlotLocation(slot=DeckSlotName.SLOT_3),
            load_name="some-load-name",
            namespace="opentrons-test",
            version=1,
            labware_id=None,
        )
    ).then_return(
        LoadedLabwareData(
            labware_id="labware-id",
            definition=well_plate_def,
            calibration=(1, 2, 3),
        )
    )

    result = await subject.execute(data)

    assert result == LoadLabwareResult(
        labwareId="labware-id",
        definition=well_plate_def,
        calibration=(1, 2, 3),
    )
