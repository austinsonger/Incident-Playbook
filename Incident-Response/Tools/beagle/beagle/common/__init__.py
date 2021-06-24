from __future__ import absolute_import

from typing import Dict, List, Tuple

from beagle.common.logging import logger  # noqa:F401
from beagle.nodes import Node


def split_path(path: str) -> Tuple[str, str]:
    """Parse a full file path into a file name + extension, and directory
    at once.
    For example::

        >>> split_path('c:\\ProgramData\\app.exe')
        (app.exe', 'c:\\ProgramData')

    By default, if it can't split, it'll return \\ as the directory, and None
    as the image.

    Parameters
    ----------
    path : str
        The path to parse

    Returns
    -------
    Tuple[str, str]
        A tuple of file name + extension, and directory at once.
    """
    image_only = path.split("\\")[-1]
    directory = "\\".join(path.split("\\")[:-1])

    if directory == "":
        directory = "\\"
    if image_only == "":
        image_only = "None"

    return image_only, directory


def split_reg_path(reg_path: str) -> Tuple[str, str, str]:
    """Splits a full registry path into hive, key, and path.

    Examples
    ----------

        >>> split_reg_path(\\REGISTRY\\MACHINE\\SYSTEM\\ControlSet001\\Control\\ComputerName)
        (REGISTRY, ComputerName, MACHINE\\SYSTEM\\ControlSet001\\Control)


    Parameters
    ----------
    regpath : str
        The full registry key

    Returns
    -------
    Tuple[str, str, str]
        Hive, registry key, and registry key path
    """
    # RegistryKey Node Creation
    hive = reg_path.split("\\")[0]
    reg_key_path = "\\".join(reg_path.split("\\")[1:-1])
    reg_key = reg_path.split("\\")[-1]

    return (hive, reg_key, reg_key_path)


def dedup_nodes(nodes: List[Node]) -> List[Node]:
    """Deduplicates a list of nodes.

    Parameters
    ----------
    nodes : List[Node]
        [description]

    Returns
    -------
    List[Node]
        [description]
    """

    def _merge_batch(nodes: List[Node]) -> List[Node]:
        """Merge a single batch of nodes"""
        output: Dict[int, Node] = {}

        logger.debug(f"Merging batch of size {len(nodes)}")

        for node in nodes:
            node_key = hash(node)

            # First time seeing node.
            if node_key not in output:
                output[node_key] = node
                continue

            # Otherwise, update the node

            current = output[node_key]

            current.merge_with(node)

            output[node_key] = current

        logger.debug(f"Merged down to size {len(output)}")

        return list(output.values())

    return _merge_batch(nodes)
