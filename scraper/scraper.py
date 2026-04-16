import requests
from datetime import datetime
import time

BASE_URL = "https://api.ycombinator.com/v0.1/companies"


def scrape_data():

    print("Fetching startup data...")

    data = []

    url = BASE_URL

    try:

        while url:

            print("Fetching:", url)

            response = requests.get(
                url,
                timeout=30
            )

            if response.status_code != 200:

                print("Failed to fetch data")

                break

            response_data = response.json()

            companies = response_data.get(
                "companies",
                []
            )

            for company in companies:

                name = company.get("name")

                if not name:
                    continue

                record = {

                    "name": name,

                    "description":
                        company.get("oneLiner"),

                    "long_description":
                        company.get(
                            "longDescription"
                        ),

                    "industry":
                        company.get(
                            "industries"
                        )[0]
                        if company.get(
                            "industries"
                        )
                        else "Unknown",

                    "tags":
                        company.get("tags"),

                    "team_size":
                        company.get(
                            "teamSize"
                        ),

                    "location":
                        company.get(
                            "locations"
                        )[0]
                        if company.get(
                            "locations"
                        )
                        else "Unknown",

                    "website":
                        company.get("website"),

                    "batch":
                        company.get("batch"),

                    "status":
                        company.get("status"),

                    "scraped_at":
                        datetime.utcnow()

                }

                data.append(record)

            url = response_data.get(
                "nextPage"
            )

            time.sleep(1)

        print(
            "Total companies fetched:",
            len(data)
        )

        return data

    except Exception as e:

        print(
            "Error during scraping:",
            e
        )

        return []
    
if __name__ == "__main__":

    data = scrape_data()

    print("\nSample record:")

    if data:
        print(data[0])