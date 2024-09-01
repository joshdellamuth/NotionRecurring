'''
pip installs copy paste: 
1. pip install requests 
2. pip install pytz
3. pip install json
'''

import requests
import json
from datetime import datetime, timedelta
import pytz

# Replace with your integration token
NOTION_TOKEN = ""

# Get this from the URL when your navigate to that database (dont highlight after the ?)
DATABASE_ID = ""

# Define the headers
headers = {
    "Authorization": f"Bearer {NOTION_TOKEN}",
    "Content-Type": "application/json",
    "Notion-Version": "2022-06-28"
}

def get_database_properties():
    url = f"https://api.notion.com/v1/databases/{DATABASE_ID}"
    headers = {
        "Authorization": f"Bearer {NOTION_TOKEN}",
        "Notion-Version": "2022-06-28"
    }
    
    response = requests.get(url, headers=headers)
    
    if response.status_code == 200:
        database_info = response.json()
        properties = database_info.get("properties", {})
        print(json.dumps(properties, indent=4))
    else:
        print(f"Failed to retrieve database properties. Status code: {response.status_code}")
        print(response.text)


# Function to create a task with custom properties including emojis
def create_task(task_data):
    url = f"https://api.notion.com/v1/pages"
    payload = {
        "parent": {"database_id": DATABASE_ID},
        # define icon for the task
        "icon": {
            "type": "emoji",
            "emoji": task_data["emoji_icon"]
        },
        "properties": {
            "Title": {
                "title": [
                    {
                        "text": {
                            "content": task_data["name"]
                        }
                    }
                ]
            },
            "Date": {
                "date": {
                    "start": task_data["start_datetime"],
                    "end": task_data["end_datetime"]
                }
            },
            "Status": {
                "status": {
                    "name": task_data["status"]
                }
            },
            # automatically added the fixed
            "Tags": {
                "multi_select": [
                    {
                        "id": "834c0b72-8620-406d-8a41-a6a87243e632",
                        "name": "Fixed",
                        "color": "yellow",
                    }
                ]
            }
        }
    }
    # json.dumps converts a Python object into a JSON formatted string
    response = requests.post(url, headers=headers, data=json.dumps(payload))
    return response.json()

# get all of the dates based on the user inputted range and days pattern specified
def get_dates_between(start_date, end_date, days_of_week):
    current_date = start_date
    dates = []
    while current_date <= end_date:
        if current_date.strftime('%A') in days_of_week:
            dates.append(current_date)
        current_date += timedelta(days=1)
    return dates

def print_notion_recurring():
    print(r"""
 
 Thank you for using:
  _   _       _   _                            
 | \ | | ___ | |_(_) ___  _ __                 
 |  \| |/ _ \| __| |/ _ \| '_ \                
 | |\  | (_) | |_| | (_) | | | |               
 |_| \_|\___/ \__|_|\___/|_| |_|               
  ____                           _             
 |  _ \ ___  ___ _   _ _ __ _ __(_)_ __   __ _ 
 | |_) / _ \/ __| | | | '__| '__| | '_ \ / _` |
 |  _ <  __/ (__| |_| | |  | |  | | | | | (_| |
 |_| \_\___|\___|\__,_|_|  |_|  |_|_| |_|\__, |
                                         |___/ 
                                                                             
    """)

'''
Emojis I use to copy and paste: 
🔨 📊 ✅ 👍 🦥 🚛 🎯 🛏️ 🏠 👨‍💻 ➖ 🚘
'''

def main():
    print_notion_recurring()
    get_database_properties()
    # Input dates and days of the week
    inputted_name = input("Enter the name/title of the task: ")
    emoji_icon = input("Enter the emoji icon you would like to use for the task (must be an emoji and must be set): ")
    begin_time_str = input("Enter the start time each task will have on that date (HH:MM) (24 hr format): ")
    end_time_str = input("Enter the end time each task will have on that date (HH:MM) (24 hr format): ")
    start_date_range_str = input("Enter the date you want to start repeating the task (YYYY-MM-DD): ")
    end_date_range_str = input("Enter the date you want to stop repeating the task (YYYY-MM-DD): ")
    days_of_week = input("Enter the days of the week you would like the task to occur (comma-separated, e.g., Monday,Wednesday): ").split(',')

    # format the date range dates into date times 
    start_date_range = datetime.strptime(start_date_range_str, '%Y-%m-%d')
    end_date_range = datetime.strptime(end_date_range_str, '%Y-%m-%d')
    print(start_date_range)
    print(end_date_range)

    # get the date range with the inputted days of the week
    dates = get_dates_between(start_date_range, end_date_range, days_of_week)

    # Set the time zone to your local time zone
    local_tz = pytz.timezone('America/Chicago')

    for date in dates:
        # for every date in the list, add the time inputted by the user before making it in Notion
        start_datetime = datetime.combine(date, datetime.strptime(begin_time_str, '%H:%M').time())
        end_datetime = datetime.combine(date, datetime.strptime(end_time_str, '%H:%M').time())

        # Localize the datetime objects to the local time zone
        start_datetime = local_tz.localize(start_datetime)
        end_datetime = local_tz.localize(end_datetime)

        # dictionary 
        task_data = {
            "name": inputted_name,
            "emoji_icon": emoji_icon,
            "start_datetime": start_datetime.isoformat(),
            "end_datetime": end_datetime.isoformat(),
            "status": "➖"
        }
        response = create_task(task_data)
        print(response)  # Print the response to see the output

if __name__ == "__main__":
    main()
