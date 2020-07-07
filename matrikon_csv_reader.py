#! python3
# -*- coding: utf-8 -*-

"""
:copyright:    2017 DIgSILENT GmbH. All rights reserved.
:author:       Marcus Walther (M.Walther@digsilent.de)
:organization: DIgSILENT GmbH
:date:         2016-01-29
:short:        A module containing a class that is able to read the CSV alias definition exported by Matrikon Server.
:todo:         -
"""

import csv

from .config import AliasConfiguration
from typing import List


class MatrikonCsvReader(object):  # pylint: disable=too-few-public-methods
    """
    A class to read the Matrikon CSV file.
    """

    def __init__(self, filePath: str) -> None:
        """
        Initialise a new alias configuration.

        :param filePath:  The path of the used CSV file.
        """
        self.__filePath = filePath

    def readAliasVars(self) -> List[AliasConfiguration]:
        """
        Read all alias variables from the Matrikon CSV file.

        :return:  The list of all read aliases
        """
        result = []
        with open(self.__filePath, 'r') as csvfile:
            fileReader = csv.reader(csvfile, delimiter=',', quotechar='"')
            for row in fileReader:
                if row and row[0].startswith('#'):  # skip comments
                    continue
                if len(row) != 8:
                    raise RuntimeError("Wrong number of entries in row given. Expected 8, got %s." % str(len(row)))
                result.append(AliasConfiguration(row[0], row[1], row[2], row[3], row[4], row[5], row[6], row[7]))

        return result
