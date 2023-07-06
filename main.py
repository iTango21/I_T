import requests
import json
import os
import xml.etree.ElementTree as ET
import re

# File name
filename = "Questel-2000-07-06-sample.xml"

# Extract directory name from the file name
directory_name = os.path.splitext(filename)[0]

# Create directory if it doesn't exist
if not os.path.exists(directory_name):
    os.makedirs(directory_name)
    print(f"Created directory: {directory_name}")

# Path to the "PDF" directory
pdf_directory = os.path.join(directory_name, "PDF")

# Create "PDF" directory if it doesn't exist
if not os.path.exists(pdf_directory):
    os.makedirs(pdf_directory)
    print(f"Created directory: {pdf_directory}")

# Open XML file and parse it
tree = ET.parse(filename)
root = tree.getroot()

url_elements = root.findall('.//url')

for i in url_elements:
    # Find the "url" tag and get its value
    url_element = i.find('.//style')

    pdf_link = url_element.text if url_element is not None else None

    if pdf_link is not None:
        # Print the obtained value
        print(pdf_link)

        # Define the regular expression
        regex = r"XPN=([^&]+)"

        # Search for matches using the regular expression
        matches = re.findall(regex, pdf_link)

        # Extract the found matches
        if len(matches) > 0:
            result = matches[0]
            print(result)
        else:
            print("No matches found.")

        headers = {
            'authority': 'rest.orbit.com',
            'accept': '*/*',
            'accept-language': 'ru-RU,ru;q=0.9,en-US;q=0.8,en;q=0.7,uk;q=0.6,vi;q=0.5,pt;q=0.4,ka;q=0.3',
            'application': 'Express',
            'content-type': 'application/json',
            'origin': 'https://permalink.orbit.com',
            'referer': 'https://permalink.orbit.com/',
            'sec-ch-ua': '"Not.A/Brand";v="8", "Chromium";v="114", "Google Chrome";v="114"',
            'sec-ch-ua-mobile': '?0',
            'sec-ch-ua-platform': '"Windows"',
            'sec-fetch-dest': 'empty',
            'sec-fetch-mode': 'cors',
            'sec-fetch-site': 'same-site',
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36',
        }

        response = requests.get(
            f'https://rest.orbit.com/rest/iorbit/user/permalink/fampat/{result}&id=0&base=;fields=AB%20ACT%20APID%20CLMS%20CTN%20CTGN%20DESC%20EPRD%20PRD%20FPN%20IC%20ICLM%20IMG%20IN%20NOTE%20PA%20PDF%20PN%20REP%20STAR%20STG%20TI%20UFLD%20V_APL%20V_FACT%20V_PTCC%20REGISTER',
            headers=headers,
        )

        data_ = json.loads(response.text)
        # print(data_['data']['documents'][0]['APID'])

        item_directory = os.path.join(pdf_directory, data_['data']['documents'][0]['APID'])
        if not os.path.exists(item_directory):
            os.makedirs(item_directory)
            print(f"Created directory: {item_directory}")

        url_pdf = data_['data']['documents'][0]['PDF']
        filename = f"{item_directory}/{data_['data']['documents'][0]['ID']}.pdf"

        response = requests.get(url_pdf)

        if response.status_code == 200:
            with open(filename, 'wb') as file:
                file.write(response.content)
            print(f'File {filename} successfully downloaded.')
        else:
            print('Failed to download the file.')
