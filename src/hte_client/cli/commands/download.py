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
from typing import Optional,List

import typer
from rich.table import Table

import hte_client.cli.styles as styles

download_app = typer.Typer(name='download', no_args_is_help=True,help="Download Zip files from sample and process information.")

@download_app.command(name="run")
def download_run(
    sql_file: Optional[Path] = typer.Option(None,'--file', help='Path to sql file to run download from'),
    raw_sql: Optional[str] = typer.Option(None, '--raw',help='Raw sql to run.'),
    number_of_rows: int = typer.Option(10, '-n',help='Number of rows to print to the screen.'),
    fields: Optional[List[str]] = typer.Option(None, '--field',help='Number of rows to print to the screen.')
):
    """
    Test connections to the database
    """
    if sql_file:
        command = sql_file.read_text()
    elif raw_sql:
        command = raw_sql
    else:
        raise typer.BadParameter('Need to provide --file or --raw.')

    with styles.console.status('Running download...'):
        result = run_raw_download(command)
    if result:
        table = Table(title=sql_file or command)
        if fields:
            if len(fields) != len(result[0]):
                raise typer.BadParameter(f'Incorrect number of fields provided for download output. Expected {len(result[0])} but given {len(fields)}',param_hint='fields')
            for field in fields:
                table.add_column(field)
        else:
            for i in range(len(result[0])):
                table.add_column(f'Column {i}')

        styles.console.print(f'download finished. It returned {len(result)} row(s). Showing first {number_of_rows} rows')
        styles.delimiter()
        for row in result[:number_of_rows]:
            table.add_row(*row)
        styles.console.print(table)
    else:
        styles.bad_typer_print('No data returned.')
