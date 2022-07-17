from typing import List, Dict

from fastapi import Depends, FastAPI
from sqlmodel.ext.asyncio.session import AsyncSession

from app.db import get_session
from app.models import Results
from app.service import get_results as get_r, read_data_input

app = FastAPI()


@app.on_event("startup")
async def startup_event():
    read_data_input()


@app.get("/results", response_model=Dict[str, List[Results]])
async def get_results(session: AsyncSession = Depends(get_session)):
    results = await get_r(session)
    curr_results = [i for i in results if i.new is True]
    history = [i for i in results if i.new is not True]
    return {
        'current_results': curr_results,
        'history': history
    }


@app.get("/history/{event_result_id}", response_model=Dict[str, List[Results]])
async def get_history(event_result_id: int,
                      session: AsyncSession = Depends(get_session)):
    results = await get_r(session, event_result_id)
    curr_results = [i for i in results if i.new is True]
    history = [i for i in results if i.new is not True]
    return {
        'current_results': curr_results,
        'history': history
    }
