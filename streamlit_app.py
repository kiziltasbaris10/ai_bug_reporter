import streamlit as st
import requests

st.set_page_config(page_title='AI Bug Reporter', layout='centered')

st.title('🐞 AI Bug Reporter')

st.markdown("Enter the details of the bug below:")

title = st.text_input('Bug Title')
description = st.text_area('Bug Description')
log = st.text_area('Log Output')

if st.button('Submit Bug Report'):
    if not title or not description or not log:
        st.warning('Please fill in all fields.')
    else:
        with st.spinner('Submitting...'):
            try:
                response = requests.post(
                    'http://localhost:8010/report-bug',
                    json={
                        'title': title,
                        'description': description,
                        'log': log
                    }
                )
                if response.status_code == 200:
                    data = response.json()
                    st.success('✅ Bug report submitted successfully!')
                    st.subheader('📊 Log Analysis')
                    st.json(data['analysis'])
                else:
                    st.error(f'Server error: {response.status_code}')
            except Exception as e:
                st.error(f'An error occurred: {str(e)}')
