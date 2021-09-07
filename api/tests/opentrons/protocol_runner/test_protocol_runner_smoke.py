"""Smoke tests for the ProtocolRunner and ProtocolEngine classes.

These tests construct a ProtocolRunner with a real ProtocolEngine
hooked to a simulating HardwareAPI.

Minimal, but valid and complete, protocol files are then loaded from
disk into the runner, and the protocols are run to completion. From
there, the ProtocolEngine state is inspected to everything was loaded
and ran as expected.
"""
from pathlib import Path
from datetime import datetime
from decoy import matchers

from opentrons_shared_data.pipette.dev_types import LabwareUri
from opentrons.types import MountType
from opentrons.protocol_api_experimental import DeckSlotName

from opentrons.protocol_engine import (
    DeckSlotLocation,
    LoadedLabware,
    LoadedPipette,
    PipetteName,
    commands,
)
from opentrons.protocol_runner import (
    ProtocolFile,
    ProtocolFileType,
    create_simulating_runner,
)


async def test_protocol_runner_with_python(python_protocol_file: Path) -> None:
    """It should run a Python protocol on the ProtocolRunner."""
    protocol_file = ProtocolFile(
        protocol_type=ProtocolFileType.PYTHON,
        files=[python_protocol_file],
    )

    subject = await create_simulating_runner()
    commands_result = await subject.run(protocol_file)
    pipettes_result = subject.engine.state_view.pipettes.get_all()
    labware_result = subject.engine.state_view.labware.get_all_labware()

    pipette_id_captor = matchers.Captor()
    labware_id_captor = matchers.Captor()

    expected_pipette = LoadedPipette(
        id=pipette_id_captor,
        pipetteName=PipetteName.P300_SINGLE,
        mount=MountType.LEFT,
    )

    expected_labware = LoadedLabware(
        id=labware_id_captor,
        location=DeckSlotLocation(slot=DeckSlotName.SLOT_1),
        loadName="opentrons_96_tiprack_300ul",
        definitionUri=LabwareUri("opentrons/opentrons_96_tiprack_300ul/1"),
    )

    assert expected_pipette in pipettes_result
    assert expected_labware in labware_result

    expected_command = commands.PickUpTip.construct(
        id=matchers.IsA(str),
        status=commands.CommandStatus.SUCCEEDED,
        createdAt=matchers.IsA(datetime),
        startedAt=matchers.IsA(datetime),
        completedAt=matchers.IsA(datetime),
        data=commands.PickUpTipData(
            pipetteId=pipette_id_captor.value,
            labwareId=labware_id_captor.value,
            wellName="A1",
        ),
        result=commands.PickUpTipResult(),
    )

    assert expected_command in commands_result


async def test_protocol_runner_with_json(json_protocol_file: Path) -> None:
    """It should run a JSON protocol on the ProtocolRunner."""
    protocol_file = ProtocolFile(
        protocol_type=ProtocolFileType.JSON,
        files=[json_protocol_file],
    )

    subject = await create_simulating_runner()
    commands_result = await subject.run(protocol_file)
    pipettes_result = subject.engine.state_view.pipettes.get_all()
    labware_result = subject.engine.state_view.labware.get_all()

    expected_pipette = LoadedPipette(
        id="pipette-id",
        pipetteName=PipetteName.P300_SINGLE,
        mount=MountType.LEFT,
    )

    expected_labware = LoadedLabware(
        id="labware-id",
        location=DeckSlotLocation(slot=DeckSlotName.SLOT_1),
        loadName="opentrons_96_tiprack_300ul",
        definitionUri=LabwareUri("opentrons/opentrons_96_tiprack_300ul/1"),
    )

    assert expected_pipette in pipettes_result
    assert expected_labware in labware_result

    expected_command = commands.PickUpTip.construct(
        id=matchers.IsA(str),
        status=commands.CommandStatus.SUCCEEDED,
        createdAt=matchers.IsA(datetime),
        startedAt=matchers.IsA(datetime),
        completedAt=matchers.IsA(datetime),
        data=commands.PickUpTipData(
            pipetteId="pipette-id",
            labwareId="labware-id",
            wellName="A1",
        ),
        result=commands.PickUpTipResult(),
    )

    assert expected_command in commands_result
