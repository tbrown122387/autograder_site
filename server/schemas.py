from pydantic import BaseModel


class DeleteID(BaseModel):
    id: int
