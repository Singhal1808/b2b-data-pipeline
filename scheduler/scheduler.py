import time
import schedule
from datetime import datetime
import os
from dotenv import load_dotenv

from scraper.scraper import scrape_data
from cleaner.cleaner import clean_data
from database.db import save_to_database

load_dotenv()

INTERVAL_MINUTES = int(
    os.getenv("INTERVAL_MINUTES", 60)
)


def run_pipeline():

    try:

        print(
            "\nStarting scheduled pipeline at:",
            datetime.now()
        )

        raw_data = scrape_data()

        cleaned_data = clean_data(raw_data)

        save_to_database(cleaned_data)

        print("Pipeline completed.")

    except Exception as e:

        print("Pipeline error:", e)


if __name__ == "__main__":

    run_pipeline()

    schedule.every(
        INTERVAL_MINUTES
    ).minutes.do(run_pipeline)

    print("Scheduler started...")

    last_next_run = None

    while True:

        next_run = schedule.next_run()

        if next_run != last_next_run:

            print(
                "Next run at:",
                next_run
            )

            last_next_run = next_run

        schedule.run_pending()

        time.sleep(10)