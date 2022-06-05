"""
This module collects pytest fixtures needed for unit testing.
"""

from unittest import mock

import pytest


@pytest.fixture(scope="function")
def async_repository_mock():
    """Create asynchronous repository mock."""
    return mock.AsyncMock(name="async_repository_mock")


@pytest.fixture(scope="function")
def async_session_mock():
    """Create mock of asynchronous session."""
    session_mock = mock.AsyncMock(name="AsyncSession mock")
    session_mock.add = mock.Mock(name="AsyncSession.add mock")
    session_mock.commit = mock.AsyncMock(name="AsyncSession.commit mock")
    return session_mock
