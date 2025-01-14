"""Tests for the ProtocolAnalyzer."""
import pytest
from decoy import Decoy
from datetime import datetime

from opentrons.protocol_engine import commands as pe_commands
from opentrons.protocol_runner import ProtocolRunner

from robot_server.protocols import ProtocolFileType
from robot_server.protocols.analysis_store import AnalysisStore
from robot_server.protocols.protocol_store import ProtocolResource
from robot_server.protocols.protocol_analyzer import ProtocolAnalyzer


@pytest.fixture
def protocol_runner(decoy: Decoy) -> ProtocolRunner:
    """Get a mocked out ProtocolRunner."""
    return decoy.mock(cls=ProtocolRunner)


@pytest.fixture
def analysis_store(decoy: Decoy) -> AnalysisStore:
    """Get a mocked out AnalysisStore."""
    return decoy.mock(cls=AnalysisStore)


@pytest.fixture
def subject(
    protocol_runner: ProtocolRunner,
    analysis_store: AnalysisStore,
) -> ProtocolAnalyzer:
    """Get a ProtocolAnalyzer test subject."""
    return ProtocolAnalyzer(
        protocol_runner=protocol_runner,
        analysis_store=analysis_store,
    )


async def test_analyze(
    decoy: Decoy,
    protocol_runner: ProtocolRunner,
    analysis_store: AnalysisStore,
    subject: ProtocolAnalyzer,
) -> None:
    """It should be able to analyize a protocol."""
    protocol_resource = ProtocolResource(
        protocol_id="protocol-id",
        protocol_type=ProtocolFileType.JSON,
        created_at=datetime(year=2021, month=1, day=1),
        files=[],
    )

    analysis_commands = [
        pe_commands.Pause(
            id="command-id",
            status=pe_commands.CommandStatus.SUCCEEDED,
            createdAt=datetime(year=2022, month=2, day=2),
            data=pe_commands.PauseData(message="hello world"),
        )
    ]

    decoy.when(await protocol_runner.run(protocol_resource)).then_return(
        analysis_commands
    )

    await subject.analyze(
        protocol_resource=protocol_resource,
        analysis_id="analysis-id",
    )

    decoy.verify(
        analysis_store.update(
            analysis_id="analysis-id",
            commands=analysis_commands,
            errors=[],
        ),
    )


async def test_analyze_error(
    decoy: Decoy,
    protocol_runner: ProtocolRunner,
    analysis_store: AnalysisStore,
    subject: ProtocolAnalyzer,
) -> None:
    """It should handle errors raised by the runner."""
    protocol_resource = ProtocolResource(
        protocol_id="protocol-id",
        protocol_type=ProtocolFileType.JSON,
        created_at=datetime(year=2021, month=1, day=1),
        files=[],
    )

    error = RuntimeError("oh no")

    decoy.when(await protocol_runner.run(protocol_resource)).then_raise(error)

    await subject.analyze(
        protocol_resource=protocol_resource,
        analysis_id="analysis-id",
    )

    decoy.verify(
        analysis_store.update(analysis_id="analysis-id", commands=[], errors=[error]),
    )
