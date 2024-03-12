#!/usr/bin/env python3

import logging

import backend.constants


def logger() -> logging.Logger:
    """Gets the main logger for scripts"""
    return logging.getLogger(backend.constants.SCRIPT_LOGGER_NAME)
