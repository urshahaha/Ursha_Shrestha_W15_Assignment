from contextlib import asynccontextmanager
import asyncio
from fastapi import FastAPI,HTTPException,Request
from slowapi import Limiter
from slowapi.errors import RateLimitExceeded
from slowapi.util import get_remote_address
from slowapi.extension import _rate_limit_exceeded_handler
from .model_loader import Week14Router
from .schemas import BatchPredictRequest,BatchPredictionResponse,PredictRequest,Prediction
from .service import RouterService
from .fallback import cloud_fallback

limiter=Limiter(key_func=get_remote_address)
@asynccontextmanager
async def lifespan(app:FastAPI):
    try:
        app.state.router_service=RouterService(Week14Router()); app.state.model_error=None
    except Exception as exc:
        app.state.router_service=None; app.state.model_error=str(exc)
    yield
app=FastAPI(title='Week 14 ShopAssist Router — Production API',version='1.0.0',lifespan=lifespan)
app.state.limiter=limiter; app.add_exception_handler(RateLimitExceeded,_rate_limit_exceeded_handler)

@app.get('/health')
async def health(): return {'status':'ok' if app.state.router_service else 'degraded','primary_model_loaded':bool(app.state.router_service),'model_error':app.state.model_error}

@app.post('/predict',response_model=Prediction)
@limiter.limit('300/minute')
async def predict(request:Request,payload:PredictRequest):
    service=app.state.router_service
    if service is None:
        try:
            r=await asyncio.to_thread(cloud_fallback,payload.message)
            return Prediction(agent=r['agent'],confidence=float(r['confidence']),needs_review=True,degraded_mode=True,provider='openai_fallback')
        except Exception as exc: raise HTTPException(503,f'Both primary and fallback routing are unavailable: {exc}') from exc
    try: return await service.predict_one(payload.message)
    except Exception as exc: raise HTTPException(503,f'Routing failed: {exc}') from exc

@app.post('/predict/batch',response_model=BatchPredictionResponse)
@limiter.limit('10/minute')
async def predict_batch(request:Request,payload:BatchPredictRequest):
    service=app.state.router_service
    if service is None: raise HTTPException(503,'Primary model unavailable. Use /predict for fallback routing.')
    try: return BatchPredictionResponse(predictions=await service.predict_batch(payload.messages))
    except Exception as exc: raise HTTPException(503,f'Batch routing failed: {exc}') from exc
