from pydantic import BaseModel,Field
class PredictRequest(BaseModel): message:str=Field(min_length=1,max_length=2000)
class BatchPredictRequest(BaseModel): messages:list[str]=Field(min_length=1,max_length=128)
class Prediction(BaseModel):
    agent:str
    confidence:float
    needs_review:bool
    degraded_mode:bool=False
    provider:str='week14_distilbert'
class BatchPredictionResponse(BaseModel): predictions:list[Prediction]
