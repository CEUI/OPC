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

import logging

from multiprocessing import Process, Value, Queue
from time import sleep

from opcua import Server, ua
from opc_wrapper.server import OpcServer
from opc_wrapper.config.config import ServerConfiguration
from opcua.common.callback import CallbackType


class FreeOpcUAServer(OpcServer):  # pylint: disable=too-many-instance-attributes
    """
    A wrapper class for an OPC-UA server based on the freeOpcUa framework.
    The server will start in a different process using the multiprocessing
    module.
    """

    def create_monitored_items(self, event, dispatcher):
        print("Monitored Item")

        for idx in range(len(event.response_params)):
            if (event.response_params[idx].StatusCode.is_good()):
                nodeId = event.request_params.ItemsToCreate[idx].ItemToMonitor.NodeId
                print("Node {0} was created".format(nodeId))


    def modify_monitored_items(self, event, dispatcher):
        print('modify_monitored_items')

    
    def delete_monitored_items(self, event, dispatcher):
        print('delete_monitored_items')
    

    @property
    def _logger(self) -> logging.Logger:
        """
        Get the logger for this class.

        :return:  The logger for this class.
        """
        logger = logging.getLogger("OPC." + self.__class__.__name__)
        return logger

    def __init__(self, configuration: ServerConfiguration) -> None:
        """
        Initialise the free OPC UA server.

        :param configuration:  The used OPC server configuration.
        """
        super().__init__(configuration)
        self._process = None
        self._stop = Value('i', False)
        self._started = Value('i', False)
        self._commands = Queue()  # commands to send from main process to server process
        self.pfGroup = None
        self._comThread = None

    def isRunning(self) -> bool:
        """
        Check, if the OPC server is running.

        :return:  True, if the OPC server is running.
        """
        if self._process is None:
            return False

        return self._started.value

    def start(self) -> None:
        """
        Start the OPC server.
        """
        if self.isRunning():
            self._logger.debug("Unable to start server because it is already running.")
            return

        self._logger.debug("Starting server with configuration %s", str(self.configuration))
        self._stop.value = False
        self._started.value = False
        self._process = Process(target=self._start)
        self._process.start()

    def _start(self) -> None:  # pylint: disable=too-many-statements
        """
        Working loop the OPC server.
        """
        try:
            sleep(1)
            server = Server()
            server.iserver.aspace.updateTimestamps = True
            server.subscribe_server_callback(CallbackType.ItemSubscriptionCreated, self.create_monitored_items)
            server.subscribe_server_callback(CallbackType.ItemSubscriptionModified, self.modify_monitored_items)
            server.subscribe_server_callback(CallbackType.ItemSubscriptionDeleted, self.delete_monitored_items)

            # TCP-ports usually used: 4840 (discovery server)  -  4846 (UA server)
            server.set_endpoint("%s://%s:%s/%s" % (self.configuration.protocol, self.configuration.serverUrl, str(self.configuration.port),
                                                   self.configuration.serverName))
            # Setup our own namespace, not really necessary
            uri = "http://testserver.freeopcua.io"
            idx = server.register_namespace(uri)
            server.start()
            objects = server.get_objects_node()
            self.pfGroup = objects.add_object(idx, "PF")
            for var in self.configuration.aliases:
                variant = None
                dataType = int(var.dataType)
                if dataType == 2:
                    variant = ua.Variant(0, ua.VariantType.Int16)
                else:
                    if dataType == 4:
                        variant = ua.Variant(0, ua.VariantType.Float)

                if variant is None:
                    raise RuntimeError("Unknown data type given " + var.dataType)

                pfVar = self.pfGroup.add_variable(idx, var.aliasName, variant)
                pfVar.set_writable(True)

                self._logger.debug("Adding variable " + var.aliasName + " to PF group")

            self._started.value = True
            oldValues = []
            for node in self.pfGroup.get_children():
                self._logger.debug("Value of %s is set to %.2f initially", node.get_browse_name(), node.get_value())
                oldValues.append(node.get_value())

            cmd = None
            while not self._stop.value:
                sleep(0.2)
                try:
                    cmd = None
                    try:
                        cmd = self._commands.get(False)
                    except Exception as ex:  # pylint: disable=broad-except
                        pass

                    if cmd is not None:
                        self._logger.debug("Found command to execute: %s.", cmd)
                        cmd.execute(self, server)
                        self._logger.debug("Finished execution.")

                    i = 0
                    for node in list(self.pfGroup.get_children()):
                        newValue = node.get_value()
                        if oldValues[i] != newValue:
                            self._logger.debug("Node %s has changed its value from %.2f to %.2f.", node.get_browse_name().to_string(),
                                               oldValues[i], newValue)

                            oldValues[i] = node.get_value()
                        i = i + 1
                except Exception as ex:  # pylint: disable=broad-except
                    self._logger.error("Failure occured %s.", str(ex))

            self._logger.debug("Stopping server (forked process).")
            server.stop()
            self._started.value = False
        except Exception as ex:  # pylint: disable=broad-except
            self._logger.error(str(ex))

    def changeVariableValue(self, varName: str, varValue: object) -> None:
        """
        Change the given variable to the given value.

        :param varName:   The name of the variable to change.
        :param varValue:  The value of the variable.
        """
        self._commands.put(ChangeValueCommand(varName, varValue))

    def deleteVariable(self, varName: str) -> None:
        """
        Delete the given variable.

        :param varName:   The name of the variable to delete.
        """
        self._commands.put(DeleteVariableCommand(varName))

    def stop(self) -> None:
        """
        Stop the OPC server.
        """
        if not self.isRunning():
            self._logger.debug("Server was already stopped")
            return

        self._stop.value = True
        self._logger.debug("Stopping server.")
        self._process.join(3)

        if self._process.is_alive():
            self._process.terminate()

        self._process = None
        self._comThread = None


class DeleteVariableCommand(object):  # pylint: disable=too-few-public-methods
    """
    The class for a delete variable command.
    """

    def __init__(self, varName: str) -> None:
        """
        Initialise the delete variable command.

        :parm varName:  The variable name to delete.
        """
        self.varName = varName

    def execute(self, server: FreeOpcUAServer, internalServer: Server) -> None:
        """
        Execute the delete variable command.

        :param server:          The used OPC server.
        :param internalServer:  The used internal OPC server.
        """
        child = server.pfGroup.get_child(self.varName)
        # internalServer.iserver.isession.delete_subscriptions(child)
        internalServer.delete_nodes([child])

    def __str__(self) -> str:
        """
        Get the delete variable command as string.

        :return:  The delete variable command as string.
        """
        return "DeleteVariableCommand::Variable=%s" % self.varName


class ChangeValueCommand(object):  # pylint: disable=too-few-public-methods
    """
    The class for a change value command.
    """

    def __init__(self, varName: str, varValue: object) -> None:
        """
        Initialise the change value command.

        :parm varName:   The variable name to change.
        :parm varValue:  The variable value to change.
        """
        self.varName = varName
        self.varValue = varValue

    def execute(self, server: FreeOpcUAServer, internalServer: Server) -> None:  # @UnusedVariable pylint: disable=unused-argument
        """
        Execute the change value command.

        :param server:          The used OPC server.
        :param internalServer:  The used internal OPC server.
        """
        child = server.pfGroup.get_child(self.varName)
        if child.get_data_value().Value.VariantType == ua.VariantType.Int16:
            child.set_value(ua.Variant(int(self.varValue), ua.VariantType.Int16))
        else:
            child.set_value(ua.Variant(float(self.varValue), ua.VariantType.Float))

    def __str__(self) -> str:
        """
        Get the change value command as string.

        :return:  The change value command as string.
        """
        return "ChangeValueCommand::Variable=%s::value=%0.2f" % (self.varName, self.varValue)
