"""Workspace (group) configuration for Qtile."""

from typing import Any, List

WORKSPACE_NAMES = "12345"


def create_groups(group_class: Any) -> List:
    """Create workspace groups.

    Args:
        group_class: Qtile Group class

    Returns:
        List of Group objects
    """
    return [group_class(name) for name in WORKSPACE_NAMES]
