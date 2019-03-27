# -*- coding: utf-8 -*-
"""
This module contains auxiliary functions for the application, including wrappers for various Flask functions.

------

"""

from flask import jsonify

def convert_json(arg_dict):
    """Wrapper for Flask's ``jsonify()`` function.

    Args:
        arg_dict (dict): dictionary of key-value pairs to be converted into JSON-format.

    Returns:
        JSON-formatted *arg_dict* using Flask's ``jsonify()`` function.
    """
    return jsonify(arg_dict)










