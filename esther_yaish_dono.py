import re
import requests
import json
import random

BASE_URL = "https://recording.seminoleclerk.org/DuProcessWebInquiry/Home"
ASCII_OFFSET = 64

# The conversion of GIN to an access_key is a critical step, as it is required to retrieve the extended instrument data. 
# Without it, we cannot access the full details of the record.
def gin_to_access_key(gin: str) -> str:
    # Each digit is converted to a character according to ASCII
    return ''.join([chr(ASCII_OFFSET + int(c)) for c in gin])

def search_records(first_name: str, last_name: str, from_date: str, thru_date: str)-> list[dict]:
    url = f"{BASE_URL}/CriteriaSearch"
    params = {
        "criteria_array": json.dumps([{
            "full_name": f"{last_name} {first_name}",
            "file_date_start": from_date,
            "file_date_end": thru_date
        }])
    }
    res = requests.get(url, params=params)
    if res.status_code == 200:
        return res.json()
    else:
        print("Request failed with status:", res.status_code)
        return []
    
def get_instrument_details(access_key: str)-> dict:
    # The values of x and y in the access_key do not affect the returned data.
    x = random.randint(1, 99)
    y = random.randint(1, 99)
    url = f"{BASE_URL}/LoadInstrument/?access_key={access_key}!0-{x}-{y}"
    res = requests.get(url)
    return res.json() if res.status_code == 200 else {}

def get_image_links(access_key: str) -> list:
    url = f"{BASE_URL}/GetNumberOfDocumentPages?id={access_key}"
    res = requests.get(url)
    if res.status_code != 200:
        return []
    else:
        num_pages = res.json() if isinstance(res.json(), int) else 0
        return [
            f"{BASE_URL}/GetDocumentPage/undefined,{access_key},{i}"
            for i in range(num_pages)
        ]
    
# Extracts the timestamp number from a wrapped date string ("/Date(…)").
def extract_timestamp(date_str: str) -> int:
    match = re.search(r'\d+', date_str)
    return int(match.group()) if match else 0    

# Builds a complete record object containing all required fields for the final output
def build_record(item: dict, inst_data: dict, access_key: str) -> dict:
    party_collection = inst_data.get("PartyCollection", [])
    record = {
        "instrument_number": int(item.get("inst_num")),
        "from": [p["PartyName"] for p in party_collection if p.get("Direction") == 1],
        "to": [p["PartyName"] for p in party_collection if p.get("Direction") == 0],
        "record_date": extract_timestamp(inst_data.get("FileDate")),
        "doc_type": item.get("instrument_type"),
        "image_links": get_image_links(access_key)
    }
    return record

def get_records(first_name: str, last_name: str, from_date: str, thru_date: str)-> list[dict]:
    results = []
    search_data = search_records(first_name, last_name, from_date, thru_date)

    for item in search_data:
        gin = item.get("gin")
        # Our access to the extended instrument data relies on converting the GIN to an access_key.
        # If the GIN is missing, we cannot proceed with this item, so we skip it.
        if not gin:
            continue
        access_key = gin_to_access_key(str(gin))
        inst_data = get_instrument_details(access_key)
        if inst_data:
            record = build_record(item, inst_data, access_key)
            results.append(record)
    return results

def runner():
    first_name = input("Enter first name: ").strip()
    last_name = input("Enter last name: ").strip()
    from_date = input("Enter from_date: ").strip()
    thru_date = input("Enter thru date: ").strip()

    # Call the get_records function
    output = get_records(first_name, last_name, from_date, thru_date)

    # Print the output
    print(json.dumps(output, indent=2))


if __name__ == "__main__":
    runner()

