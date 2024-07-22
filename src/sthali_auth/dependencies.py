"""This module provides the dependencies for sthali-backend usage."""
from typing import Annotated

from fastapi import Depends
from fastapi.security import HTTPBasic, HTTPBasicCredentials

http_basic: Annotated[HTTPBasicCredentials, Depends(HTTPBasic())]
