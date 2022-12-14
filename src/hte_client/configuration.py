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

import os
from textwrap import dedent
from typing import Any, Dict, Optional, Union

from pydantic import BaseSettings, PostgresDsn, SecretStr, parse_obj_as, validator

from hte_client._enums import LogLevel


class PostgresqlDsn(PostgresDsn):
    allowed_schemes = {"postgresql"}
    path: str


class Settings(BaseSettings):
    LOG_LEVEL: LogLevel = LogLevel.INFO

    # Database credentials
    POSTGRES_SERVER: str = "localhost"
    POSTGRES_USER: str = "postgres"
    POSTGRES_PASSWORD: SecretStr = parse_obj_as(SecretStr, "")
    POSTGRES_DB: str = ""
    POSTGRES_PORT: str = "5432"
    POSTGRES_SCHEMA: str = "production"
    POSTGRES_DSN: Optional[PostgresDsn]

    _always_set = {"POSTGRES_DSN"}
    _simple_params = {
        "POSTGRES_DSN",
        "POSTGRES_SERVER",
        "POSTGRES_USER",
        "POSTGRES_PASSWORD",
        "POSTGRES_DB",
        "POSTGRES_PORT",
        "POSTGRES_SCHEMA",
        "POSTGRES_DSN",
    }

    @validator("POSTGRES_DSN", pre=True)
    def assemble_db_connection(cls, v: Optional[str], values: Dict[str, Any]) -> Union[PostgresDsn, str]:
        if v is not None:
            return v
        password = values["POSTGRES_PASSWORD"].get_secret_value() if values["POSTGRES_PASSWORD"] else ""
        return PostgresDsn.build(
            scheme="postgresql",
            user=values["POSTGRES_USER"],
            password=password,
            host=values["POSTGRES_SERVER"],
            port=values["POSTGRES_PORT"],
            path=f"/{values['POSTGRES_DB']}",
        )

    class Config:
        case_sensitive = True
        env_file = os.environ.get('HTE_ENV_FILE', '.env')
        env_prefix = 'HTE_'
        secrets_dir = os.environ.get("SECRETS_DIR", None)

    def display(self, show_defaults: bool = False, show_passwords: bool = False, simple: bool = False):
        params = []
        for key, val in self.dict().items():
            if simple and key not in self._simple_params:
                continue
            if val is not None:
                str_val = f"{val.get_secret_value()}" if show_passwords and "PASSWORD" in key else val
                if show_defaults or key in self.__fields_set__ or key not in self._always_set:
                    params.append(f"{key} = {str_val}")
                else:
                    params.append(f"# {key} = {str_val}")

        params_str = "\n".join(params)
        output = f"""# HTE Client Settings\n{params_str}"""
        return dedent(output)

    def __str__(self) -> str:
        return self.display()


settings = Settings()
