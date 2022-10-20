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

"""A CLI Tool for Querying and client data within a High Throughput Experimentation Database"""

__author__ = "Michael Statt"
__email__ = "michael.statt@modelyst.io"
__maintainer__ = "Michael Statt"
__maintainer_email__ = "michael.statt@modelyst.io"
__version__ = "0.1.0"


from hte_client.core.queries import run_raw_query