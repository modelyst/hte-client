#   Copyright 2022 Modelyst LLC
#
#   Licensed under the Apache License, Version 2.0 (the "License");
#   you may not use this file except in compliance with the License.
#   You may obtain a copy of the License at
#
#       http://www.apache.org/licenses/LICENSE-2.0
#
#   Unless required by applicable law or agreed to in writing, software
#   distributed under the License is distributed on an "AS IS" BASIS,
#   WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#   See the License for the specific language governing permissions and
#   limitations under the License.
from typing import Optional


class HTEClientException(Exception):
    """Base Exception for hte-client."""


class DatabaseException(Exception):
    """Base Exception for errors encountered during interaction with the database."""


class DOINotFound(HTEClientException):
    """Raised when a DOI url cannot be found at https://doi.org."""


class CaltechJsonNotFound(HTEClientException):
    """Raised when a caltech json cannot be found at https://data.caltech.edu/records/{id}/export/json"""


class RequestLimitation(HTEClientException):
    """Raised when a caltech limits the number of requests."""


class UrlConnectionError(HTEClientException):
    """Raised when a caltech limits the number of requests."""


class DOIParsingError(HTEClientException):
    """Raised when a zip link cannot be parsed the DOI's webpage."""


class ConnectionTimeoutError(HTEClientException):
    """Raised when an http connection request times out."""


class DeadUrlError(HTEClientException):
    """Raised when a link redirects to a dead url."""

    dead_url: Optional[str]

    def __init__(self, dead_url: str = None) -> None:
        super().__init__()
        self.dead_url = dead_url
