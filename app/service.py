import asyncio
import json
from typing import Optional

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlmodel import Session

from app.db import sync_engine
from app.models import Results


async def get_results(session: AsyncSession,
                      event_result_id: Optional[int] = None):
    query = select(Results)
    if event_result_id is not None:
        query = query.where(Results.event_result_id == event_result_id)
    results = await session.execute(query)
    results = results.scalars().all()
    results = transform_to_model(results)
    return results


def add_record(record: Results):
    with Session(sync_engine) as session:
        query = select(Results).where(
            Results.event_result_id == record.event_result_id).where(
            Results.score_index == record.score_index).where(
            Results.new == True)
        result = session.execute(query)
        result = result.scalar()
        if not result:
            session.add(record)
            session.commit()
        else:
            result.new = False
            session.add(result)
            session.commit()
            session.refresh(result)
            session.add(record)
            session.commit()


def read_data_input():
    path = 'data/input'
    needed_class = 'Fon.Notification.EventResultNotification'
    score_body_class = 'Fon.Ora.ScoreBody'
    with open(path, 'r') as f:
        for row in f:
            row = json.loads(row)
            for el in row:
                if el.get('class') == needed_class:
                    curr_event_result_id = el['object']['eventResultId']
                    scores = el['object']['eventResultInstance']['object'][
                        'scores']
                    scores = [score['object'] for score in scores if
                              score['class'] == score_body_class]
                    curr_results = [
                        Results(
                            event_result_id=curr_event_result_id,
                            score_index=int(score['scoreIndex']),
                            score1=int(score['score1']),
                            score2=int(score['score2']),
                            flags=score['flags']
                        )
                        for score in scores
                    ]
                    for result in curr_results:
                        add_record(result)


def transform_to_model(records):
    return [Results(event_result_id=record.event_result_id,
                    score_index=record.score_index,
                    score1=record.score1,
                    score2=record.score2,
                    flags=record.flags,
                    new=record.new) for record in records]


if __name__ == '__main__':
    asyncio.run(read_data_input())
