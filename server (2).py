#! python3
# -*- coding: utf-8 -*-

"""
:copyright:    2017 DIgSILENT GmbH. All rights reserved.
:author:       Marcus Walther (M.Walther@digsilent.de)
:organization: DIgSILENT GmbH
:date:         2016-02-05
:short:        A module describing the functionality of OPC servers.
:todo:         -
"""

from .config import ServerConfiguration


class OpcServer(object):
    """
    An abstract class of a OPC server.
    """

    def __init__(self, configuration: ServerConfiguration) -> None:
        """
        Initialise the OPC server.

        :param configuration:  The used OPC server configuration.
        """
        self.configuration = configuration

    def start(self) -> None:
        """
        Start the OPC server.
        """
        pass

    def stop(self) -> None:
        """
        Stop the OPC server.
        """
        pass

    def isRunning(self) -> bool:
        """
        Check if the server is running.
        """
        pass
