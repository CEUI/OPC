#! python3
# -*- coding: utf-8 -*-

"""
:copyright:    2017 DIgSILENT GmbH. All rights reserved.
:author:       Marcus Walther (M.Walther@digsilent.de)
:organization: DIgSILENT GmbH
:date:         2016-02-05
:short:        A module containing configuration classes that can be used to set up a server and transmit settings
               from a configuration file to the server configuration.
:todo:         -
"""
import socket
from typing import List


def getFreePort() -> int:
    """
    Get the number of one free port.

    :return:  The number of one free port.
    """
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.bind(('', 0))
        s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        return int(s.getsockname()[1])
    finally:
        s.close()


class AliasConfiguration:  # pylint: disable=too-few-public-methods, too-many-instance-attributes
    """
    Configuration class for an alias definition (inspired by the Matrikon CSV alias definition).
    """

    # pylint: disable=too-many-arguments
    def __init__(self, aliasGroup: str, aliasName: str, itemPath: str, dataType: str, readOnly: str, pollAlways: str, updateRate: str,
                 scaling: str) -> None:
        """
        Initialise a new alias configuration.

        :param aliasGroup:  The alias group.
        :param aliasName:   The alias name.
        :param itemPath:    The item path.
        :param dataType:    The data type.
        :param readOnly:    The read-only flag.
        :param pollAlways:  The poll always flag.
        :param updateRate:  The update rate.
        :param scaling:     The scaling.
        """
        self.aliasGroup = aliasGroup
        self.aliasName = aliasName
        self.itemPath = itemPath
        self.dataType = dataType
        self.readOnly = readOnly
        self.pollAlways = pollAlways
        self.updateRate = updateRate
        self.scaling = scaling


class ServerConfiguration:  # pylint: disable=too-few-public-methods
    """
    Configuration class for a server definition.
    """

    # pylint: disable=too-many-arguments
    def __init__(self, protocol: str = "opc.tcp", serverUrl: str = "localhost", serverName: str = "", port: int = None,
                 aliases: List[AliasConfiguration] = None, rootPath: str = "") -> None:
        """
        Initialise a new alias configuration.

        :param protocol:    The used protocol.
        :param serverUrl:   The URL of the OPC server.
        :param serverName:  The name of the OPC server.
        :param port:        The port of the OPC server.
        :param aliases:     The list of all aliases.
        :param rootPath:    The root path of OPC tags.
        """
        self.protocol = protocol
        self.serverUrl = serverUrl
        self.serverName = serverName
        self.port = port or getFreePort()
        self.aliases = aliases or []
        self.rootPath = rootPath

    def __str__(self):
        """
        Get the OPC server configuration as string.

        :return:  The OPC server configuration as string.
        """
        return ("Protocol: %s - ServerUrl: %s - ServerName: %s - Port: %i - Aliases: %i - RootPath: %s" %
                (self.protocol, self.serverUrl, self.serverName, self.port, len(self.aliases), self.rootPath))
