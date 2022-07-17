from sqlmodel import SQLModel, Field


class Results(SQLModel, table=True):
    id: int = Field(default=None, primary_key=True)
    event_result_id: int
    score_index: int
    score1: int
    score2: int
    flags: str
    new: bool = True
