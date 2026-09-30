import asyncio
from cachetools import TTLCache
from .config import settings
from .fallback import cloud_fallback
from .schemas import Prediction

class RouterService:
    def __init__(self,model):
        self.model=model; self.semaphore=asyncio.Semaphore(settings.max_concurrent_inference); self.cache=TTLCache(maxsize=2048,ttl=settings.cache_ttl_seconds)
    async def _primary_predict(self,messages):
        async with self.semaphore: return await asyncio.to_thread(self.model.predict_batch,messages)
    async def predict_one(self,message):
        key=message.strip()
        if key in self.cache: return self.cache[key]
        try:
            r=(await self._primary_predict([key]))[0]
            p=Prediction(agent=r['agent'],confidence=r['confidence'],needs_review=r['needs_review'],degraded_mode=False,provider='week14_distilbert')
        except Exception:
            r=await asyncio.to_thread(cloud_fallback,key)
            p=Prediction(agent=r['agent'],confidence=float(r['confidence']),needs_review=True,degraded_mode=True,provider='openai_fallback')
        self.cache[key]=p; return p
    async def predict_batch(self,messages):
        clean=[m.strip() for m in messages]
        try:
            rows=await self._primary_predict(clean)
            return [Prediction(agent=r['agent'],confidence=r['confidence'],needs_review=r['needs_review'],degraded_mode=False,provider='week14_distilbert') for r in rows]
        except Exception:
            return await asyncio.gather(*[self.predict_one(m) for m in clean])
