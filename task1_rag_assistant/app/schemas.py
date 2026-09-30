from pydantic import BaseModel, Field

class AskRequest(BaseModel):
    question: str = Field(min_length=1, max_length=4000)

class SourceItem(BaseModel):
    filename: str
    chunk_id: int

class AssistantAnswer(BaseModel):
    answer: str
    sources: list[SourceItem]
    used_tool: str | None = None
    grounded: bool

class IngestResponse(BaseModel):
    filename: str
    chunks_indexed: int
