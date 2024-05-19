import requests
import streamlit as st

def fetch_data(api_url):
    data = []
    page = 1

    while True:
        response = requests.get(api_url, params={'page': page})
        if response.status_code != 200:
            break

        try:
            page_data = response.json()
        except ValueError:
            break

        if not isinstance(page_data, list):
            break

        data.extend(page_data)
        page += 1

    return data

def extract_citations(data):
    citations = []

    for item in data:
        if not isinstance(item, dict):
            continue
        
        response_text = item.get('response', '')
        sources = item.get('sources', [])
        matched_sources = []

        for source in sources:
            if source['context'] in response_text:
                matched_sources.append({'id': source['id'], 'link': source.get('link', '')})

        citations.append(matched_sources)

    return citations

def main():
    st.title('API Data and Citations')

    api_url = 'https://devapi.beyondchats.com/api/get_message_with_sources'
    st.write('Fetching data from the API...')
    data = fetch_data(api_url)
    
    st.write('Fetched Data:')
    st.json(data)  # Display the raw data for debugging
    
    st.write('Data fetched successfully!')

    st.write('Extracting citations...')
    citations = extract_citations(data)
    st.write('Citations extracted successfully!')

    for i, citation in enumerate(citations):
        st.write(f'Response {i+1}:')
        st.json(citation)

if __name__ == '__main__':
    main()