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

import logging
from typing import Optional, Union
from uuid import UUID

from sqlalchemy.dialects.postgresql import aggregate_order_by
from sqlmodel import Session, func, select, text

from hte_client._enums import EntityType
from hte_client.database.session import get_engine
from hte_client.schema.esamp import Collection, Process, ProcessDetail, Sample, SampleProcess
from hte_client.schema.jcap import JcapAnalysis, JcapRun

logger = logging.getLogger(__name__)
engine = get_engine()


def run_raw_query(query: str):
    with Session(engine) as session:
        result = session.exec(text(query)).all()
    return result


def get_process_history(sample_id: UUID, sample_label: str):
    with Session(engine) as session:
        stmt = (
            select(
                func.ARRAY_AGG(aggregate_order_by(ProcessDetail.type, Process.timestamp, Process.ordering)),
                func.ARRAY_AGG(
                    aggregate_order_by(ProcessDetail.technique, Process.timestamp, Process.ordering)
                ),
            )
            .select_from(Sample)
            .join(SampleProcess)
            .join(Process)
            .join(ProcessDetail)
        )
        if sample_id:
            stmt = stmt.where(Sample.id == sample_id)
        elif sample_label:
            stmt = stmt.where(Sample.label == sample_label)
        stmt = stmt.group_by(Sample.id)
        result = session.exec(stmt).one_or_none()
    return result


def get_doi(entity_type: EntityType, entity_id: Optional[UUID], entity_label: Optional[str]) -> Optional[str]:
    table: Union[Collection, JcapRun, JcapAnalysis]
    if entity_type == EntityType.PLATE:
        table = Collection
    elif entity_type == EntityType.RUN:
        table = JcapRun
    elif entity_type == EntityType.ANALYSIS:
        table = JcapAnalysis
    else:
        raise ValueError(f'Unknown entity_type: {entity_type}')

    # Ensure we have at least an id or label
    if not (entity_label or entity_id):
        raise ValueError('Must provide at least an id or label.')
    # Check that we provided label for the right entity type
    if entity_label and entity_type not in EntityType.PLATE:
        raise ValueError(f'Cannot provide a label for entity: {entity_type}')

    stmt = select(table.doi)
    if entity_id:
        stmt = stmt.where(table.id == entity_id)
    elif entity_label:
        stmt = stmt.where(table.label == entity_label)

    with Session(engine) as session:
        result = session.exec(stmt).one_or_none()
    return result
