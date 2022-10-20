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
from pathlib import Path
from typing import Optional
from uuid import UUID

import typer

import hte_client.cli.styles as styles
from hte_client._enums import EntityType
from hte_client._exceptions import InvalidDOIUrl
from hte_client.core.download import download_doi
from hte_client.core.queries import get_doi

download_app = typer.Typer(
    name='download', no_args_is_help=True, help="Download Zip files from sample and process information."
)


@download_app.command(name="doi")
def download_doi_command(
    doi: str = typer.Option(..., '--doi', help='Doi to download'),
    path: Path = typer.Option(..., '--path', help='Path to download the doi to'),
):
    """
    Download a doi from Caltech Data.
    """
    with styles.console.status('Downloading DOI zip...'):
        try:
            download_doi(doi, path)
        except InvalidDOIUrl:
            styles.bad_typer_print(f'DOI provided is invalid, see https://doi.org/{doi} for details')
            raise typer.Exit(code=1)
    styles.delimiter()
    styles.console.print(f'Finished downloading, files extracted to {str(path)!r}')


@download_app.command(name="entity")
def download_entity(
    entity_type: EntityType = typer.Option(..., '--entity', help='Path to sql file to run query from'),
    entity_id: Optional[UUID] = typer.Option(None, '--id', help='Path to sql file to run query from'),
    entity_label: Optional[str] = typer.Option(None, '--label', help='Path to sql file to run query from'),
    path: Path = typer.Option(..., '--path', help='Path to download the doi to'),
):
    """
    Download a doi from Caltech Data using an entity type and label/uuid.
    """
    with styles.console.status('Getting doi...'):
        doi = get_doi(entity_type=entity_type, entity_id=entity_id, entity_label=entity_label)
        lable_str = f'id={entity_id}' if entity_id else f'label={entity_label}'
        if doi is None:
            styles.bad_typer_print(f'No doi found for entity {entity_type}({lable_str})')
            raise typer.Exit(code=1)
    with styles.console.status('Downloading DOI zip...'):
        try:
            download_doi(doi, path)
        except InvalidDOIUrl:
            styles.bad_typer_print(
                f'DOI found for entity {entity_type}({lable_str}) is invalid, see https://doi.org/{doi} for details'
            )
            raise typer.Exit(code=1)

    styles.delimiter()
    styles.console.print(f'Finished downloading, files extracted to {str(path)!r}')
