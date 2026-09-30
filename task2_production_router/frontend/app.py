import os,requests,streamlit as st
API_URL=os.getenv('ROUTER_API_URL','http://localhost:8002')
st.set_page_config(page_title='ShopAssist Router',page_icon='🧭')
st.title('ShopAssist AI — Support Router')
st.caption('Productionized Week 14 customer-support routing model')
message=st.text_area('Customer message',placeholder='Example: My card was charged twice and I need a refund.',height=140)
if st.button('Route message',type='primary'):
    if not message.strip(): st.warning('Please enter a customer message.')
    else:
        try:
            response=requests.post(f'{API_URL}/predict',json={'message':message},timeout=30); response.raise_for_status(); r=response.json()
            st.success(f"Route: {r['agent']}"); st.metric('Confidence',f"{r['confidence']:.1%}"); st.write('Provider:',r['provider'])
            if r['degraded_mode']: st.warning('Primary Week 14 model unavailable; fallback provider was used.')
            if r['needs_review']: st.warning('Low confidence or fallback mode: send for human review.')
        except Exception as exc: st.error(f'Routing service error: {exc}')
