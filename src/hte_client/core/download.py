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
import io
import logging
import zipfile
from pathlib import Path

import requests
from bs4 import BeautifulSoup

from hte_client._exceptions import InvalidDOIUrl

logger = logging.getLogger(__name__)


def download_doi(doi: str, path: Path) -> None:
    URL = f"https://doi.org/{doi}"
    page = requests.get(URL)
    soup = BeautifulSoup(page.content, "html.parser")
    title = soup.find('title')
    parsing_error = ValueError(f'Issue parsing DOI {doi}')
    if 'DOI Not Found' in title.string:
        raise InvalidDOIUrl(f'DOI does not exist: {doi}')

    section = soup.find(id='additional-description-1')
    if section is None:
        raise parsing_error
    links = section.find_all("a")
    if len(links) != 1:
        raise ValueError(f'Issue parsing the page found {len(links)} instead of 1')
    zip_file_url = links[0]['href']
    logger.info(f'Downloading link {zip_file_url} found for doi')
    r = requests.get(zip_file_url)
    z = zipfile.ZipFile(io.BytesIO(r.content))
    logger.info(f'Extracting to path {path}')
    z.extractall(path)
