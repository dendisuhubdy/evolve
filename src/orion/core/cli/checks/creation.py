#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
:mod:`orion.core.cli.checks.creation` -- Creation stage for database checks
===========================================================================

.. module:: creation
    :platform: Unix
    :synopsis: Checks for the creation of a `Database` object.

"""

from orion.core.io.database import Database
from orion.core.utils.decorators import register_check
from orion.core.utils.exceptions import CheckError


class _Checks:
    checks = []


class CreationStage:
    """The creation stage of the checks."""

    def __init__(self, presence_stage):
        """Create an intance of the stage.

        Parameters
        ----------
        presence_stage: `PresenceStage`
            An instance of the previous stage.

        """
        self.p_stage = presence_stage

    @staticmethod
    def checks():
        return _Checks.checks

    @register_check(_Checks.checks, "Check if database of specified type can be created... ")
    def check_database_creation(self):
        database = self.p_stage.db_config
        db_type = database.pop('type')

        try:
            db = Database(of_type=db_type, **database)
        except ValueError as ex:
            raise CheckError(str(ex))

        if not db.is_connected:
            raise CheckError("Database failed to connect after creation.")

        self.instance = db

        return "Success", ""

    def post_stage(self):
        """Print the created database."""
        print(self.instance)
