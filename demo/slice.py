from vaapi.client import Vaapi
import os

if __name__ == "__main__":
    client = Vaapi(
        base_url=os.environ.get("VAT_API_URL"),
        api_key=os.environ.get("VAT_API_TOKEN"),
    )
    client.video.slice(path="/mnt/repl/2025-03-12-GO25/2025-03-15_17-15-00_Berlin United_vs_HULKs_half2/videos/2025-03-15_17-15-00_BerlinUnited_vs_Hulks_half2_Field-B_PiCam.mp4", start=10, end=20)
