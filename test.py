import requests
import urllib
from bs4 import BeautifulSoup
import json

def make_url(base_url , comp):
    
    url = base_url
    
    # add each component to the base url
    for r in comp:
        url = '{}/{}'.format(url, r)
        
    return url

# define a base url, this would be the EDGAR data Archives
base_url = r"https://www.sec.gov/Archives/edgar/data"

# define a company to search (GOLDMAN SACHS), this requires a CIK number that is defined by the SEC.
cik_num = '886982'

# let's get all the filings for Goldman Sachs in a json format.
# Alternative is .html & .xml
filings_url = make_url(base_url, [cik_num, 'index.json'])
print(filings_url)

headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:120.0) Gecko/20100101 Firefox/120.0", 'Accept': 'application/json'}
# Get the filings and then decode it into a dictionary object.
content = requests.get(filings_url, headers=headers)
decoded_content = json.loads(content.text)

# Get a filing number, this way we can request all the documents that were submitted.
# HERE I AM JUST GRABBING CERTAIN FILINGS FOR READABILITY REMOVE [3:5] TO GRAB THEM ALL.
for filing_number in decoded_content['directory']['item']:    
    
    filing_num = filing_number['name']
    print('-'*100)
    print('Grabbing filing : {}'.format(filing_num))
    
    # define the filing url, again I want all the data back as JSON.
    filing_url = make_url(base_url, [cik_num, filing_num, 'index.json'])

    # Get the documents submitted for that filing.
    content = requests.get(filing_url, headers=headers)
    document_content = json.loads(content.text)

    # get a document name
    for document in document_content['directory']['item']:
        document_name = document['name']
        filing_url = make_url(base_url, [cik_num, filing_num, document_name])
        print(filing_url)