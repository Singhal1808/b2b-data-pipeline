def clean_data(data):

    cleaned_data = []

    seen = set()

    for record in data:

        name = record.get("name")

        if not name:
            continue

        name = name.strip()

        if name in seen:
            continue

        seen.add(name)

        cleaned_record = {

            "name": name,

            "description":
                record.get("description")
                or "Not available",

            "long_description":
                record.get("long_description"),

            "location":
                record.get("location")
                or "Unknown",

            "industry":
                record.get("industry")
                or "Unknown",

            "tags":
                record.get("tags"),

            "team_size":
                record.get("team_size"),

            "website":
                record.get("website"),

            "batch":
                record.get("batch"),

            "status":
                record.get("status"),

            "scraped_at":
                record.get("scraped_at")

        }

        cleaned_data.append(cleaned_record)

    print("Cleaned records:", len(cleaned_data))

    return cleaned_data