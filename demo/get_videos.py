from vaapi.client import Vaapi
import os


def get_logs():
    response = client.video.list()
    for video in response:
        print(video)


if __name__ == "__main__":
    client = Vaapi(
        base_url=os.environ.get("VAT_API_URL"),
        api_key=os.environ.get("VAT_API_TOKEN"),
    )

    get_logs()
