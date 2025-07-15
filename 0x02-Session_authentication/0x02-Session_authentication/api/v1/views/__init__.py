#!/usr/bin/env python3
"""
DocAPI views
"""
from os import getenv
from flask import Blueprint

app_views = Blueprint("app_views", __name__, url_prefix="/api/v1")

from api.v1.views.index import *
from api.v1.views.users import *

# Import session_auth views at the end to avoid circular imports
from api.v1.views.session_auth import *
