# Backend Task 

This project is a solution to a backend assignment.  
The goal of the task is to integrate a new data source (Seminole County, Florida) by scraping real estate document records and returning structured information in JSON format.

---

##  Task Overview

The company aims to simplify access to billions of real estate documents.  
In this task, we were asked to build a Python script that:

- Accepts a person's full name and a date range
- Searches Seminole County's public records site
- Retrieves metadata about the matching records
- Converts GIN numbers to `access_key`s (required for deeper access)
- Fetches document details and image links
- Returns a list of record dictionaries in a defined format

Target site:  
 [https://recording.seminoleclerk.org/DuProcessWebInquiry](https://recording.seminoleclerk.org/DuProcessWebInquiry)

---

##  Technologies Used

- Python 3.8+
- `requests` for HTTP requests
- `re` and `json` (standard libraries)
- Random module to simulate request variations

---

##  Install dependencies

pip install -r requirements.txt 

---

##  Example Input

- First name: ben
- Last name: smith
- From date: 01/10/2023
- Thru date: 01/06/2024

---

###  Example Output

```json
[
  {
    "instrument_number": 2023004567,
    "from": [
      "MOVEMENT MORTGAGE LLC",
      "MORTGAGE ELECTRONIC REGISTRATION SYSTEMS INC"
    ],
    "to": [
      "SMITH BENJAMIN F II",
      "SMITH GRETA R"
    ],
    "record_date": 1674018000000,
    "doc_type": "SATISFACTION",
    "image_links": [
      "https://recording.seminoleclerk.org/DuProcessWebInquiry/Home/GetDocumentPage/undefined,GEHBIII,0"
    ]
  }
]
