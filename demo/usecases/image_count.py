import os
from vaapi.client import Vaapi


if __name__ == "__main__":
    client = Vaapi(
        base_url=os.environ.get("VAT_API_URL"),
        api_key=os.environ.get("VAT_API_TOKEN"),
    )   
    count = client.image.get_image_count()
    print(count)
