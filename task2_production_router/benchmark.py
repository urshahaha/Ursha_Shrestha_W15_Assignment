import argparse,statistics,time
from concurrent.futures import ThreadPoolExecutor
import requests
SAMPLES=['I need to change the address on my order.','My card payment keeps failing.','Where can I download my invoice?','I want to cancel my order.','How do I delete my account?','Where is my refund?','I want to leave a complaint.','What delivery options do you offer?']
def one(url,msg):
    t=time.perf_counter(); r=requests.post(f'{url}/predict',json={'message':msg},timeout=30); r.raise_for_status(); return (time.perf_counter()-t)*1000
def pct(v,p):
    s=sorted(v); return s[int(round((len(s)-1)*p))]
def main():
    ap=argparse.ArgumentParser(); ap.add_argument('--url',default='http://localhost:8002'); ap.add_argument('--requests',type=int,default=50); ap.add_argument('--workers',type=int,default=4); a=ap.parse_args()
    msgs=[SAMPLES[i%len(SAMPLES)] for i in range(a.requests)]; start=time.perf_counter()
    with ThreadPoolExecutor(max_workers=a.workers) as pool: lat=list(pool.map(lambda m:one(a.url,m),msgs))
    wall=time.perf_counter()-start
    print('Requests:',len(lat)); print('Workers:',a.workers); print('Mean latency (ms):',round(statistics.mean(lat),2)); print('Median latency (ms):',round(statistics.median(lat),2)); print('p95 latency (ms):',round(pct(lat,.95),2)); print('Throughput (requests/sec):',round(len(lat)/wall,2))
if __name__=='__main__': main()
