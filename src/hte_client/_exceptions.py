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


class DatabaseException(Exception):
    """Base Exception for errors encountered during interaction with the database."""


class DropMetadataException(DatabaseException):
    """Error occurred during metadata dropping."""


class CreateMetadataException(DatabaseException):
    """Error occurred during metadata create_all."""


class QueryResultsException(Exception):
    """Exception to raise when query results are not expected."""


class RequiredElementNotFoundInQuery(Exception):
    """Exception to raise when a required composition based query does not contain all the required elements."""
