import os


def get_api_url():
    host = os.environ.get("API_HOST", "localhost")
    port = 5005 if host == "localhost" else 80
    return f"http://{host}:{port}"


def get_my_uri():
    host = os.environ.get("DB_HOST", "localhost")
    port = 3306 if host == "localhost" else 33060
    password = os.environ.get("DB_PASSWORD", "abc123")
    user, db_name = "root", "root"
    return f"mysql://{user}:{password}@{host}:{port}/{db_name}"
