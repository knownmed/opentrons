import typing
from datetime import datetime, timezone
from typing_extensions import Literal
from uuid import uuid4
from fastapi import Depends, Header, Request, status

from opentrons.hardware_control import ThreadManager, ThreadedAsyncLock

from robot_server import constants, util, errors
from robot_server.hardware import get_hardware
from robot_server.service.session.manager import SessionManager
from robot_server.service.protocol.manager import ProtocolManager


class OutdatedApiVersionResponse(errors.ErrorDetails):
    """An error returned when you request an outdated HTTP API version."""

    id: Literal["OutdatedAPIVersion"] = "OutdatedAPIVersion"
    title: str = "Requested HTTP API version no longer supported"
    detail: str = (
        f"HTTP API version {constants.MIN_API_VERSION - 1} is "
        "no longer supported. Please upgrade your Opentrons "
        "App or other HTTP API client."
    )


@util.call_once
async def get_motion_lock() -> ThreadedAsyncLock:
    """
    Get the single motion lock.

    :return: a threaded async lock
    """
    return ThreadedAsyncLock()


@util.call_once
async def get_protocol_manager() -> ProtocolManager:
    """The single protocol manager instance"""
    return ProtocolManager()


@util.call_once
async def get_session_manager(
    hardware: ThreadManager = Depends(get_hardware),
    motion_lock: ThreadedAsyncLock = Depends(get_motion_lock),
    protocol_manager: ProtocolManager = Depends(get_protocol_manager),
) -> SessionManager:
    """The single session manager instance"""
    return SessionManager(
        hardware=hardware,
        motion_lock=motion_lock,
        protocol_manager=protocol_manager,
    )


async def check_version_header(
    request: Request,
    opentrons_version: typing.Union[int, constants.API_VERSION_LATEST_TYPE] = Header(
        ...,
        description=(
            f"The requested HTTP API version must be at least "
            f"'{constants.MIN_API_VERSION}' or higher. To use the latest "
            f"version unconditionally, specify '{constants.API_VERSION_LATEST}'"
        ),
    ),
) -> None:
    """Dependency that will check that Opentrons-Version header meets
    requirements."""
    # Get the maximum version accepted by client
    requested_version = (
        int(opentrons_version)
        if opentrons_version != constants.API_VERSION_LATEST
        else constants.API_VERSION
    )

    if requested_version < constants.MIN_API_VERSION:
        raise OutdatedApiVersionResponse().as_error(status.HTTP_400_BAD_REQUEST)
    else:
        # Attach the api version to request's state dict
        request.state.api_version = min(requested_version, constants.API_VERSION)


async def get_unique_id() -> str:
    """Get a unique ID string to use as a resource identifier."""
    return str(uuid4())


async def get_current_time() -> datetime:
    """Get the current time in UTC to use as a resource timestamp."""
    return datetime.now(tz=timezone.utc)
