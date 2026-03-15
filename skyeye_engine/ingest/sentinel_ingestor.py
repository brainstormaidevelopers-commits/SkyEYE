from sentinelsat import SentinelAPI, read_geojson, geojson_to_wkt
from datetime import date, datetime, timedelta
import os
from skyeye_engine.config import Config

class SentinelIngestor:
    def __init__(self):
        self.api = SentinelAPI(Config.SCIHUB_USER, Config.SCIHUB_PASS, 'https://scihub.copernicus.eu/dhus')
        
    def search_area(self, lat, lon, days_back=7, cloud_cover=(0, 20)):
        """
        Search for available Sentinel-2 imagery for a specific location.
        """
        # Create a tiny point buffer for the search
        footprint = f"POINT({lon} {lat})"
        
        start_date = date.today() - timedelta(days=days_back)
        
        products = self.api.query(footprint,
                                 date=(start_date, date.today()),
                                 platformname='Sentinel-2',
                                 processinglevel='Level-2A',
                                 cloudcoverpercentage=cloud_cover)
        
        # Convert result to a dataframe for easier handling
        products_df = self.api.to_dataframe(products)
        return products_df

    def download_product(self, product_id):
        """
        Download a specific product to the local cache.
        """
        print(f"[INGEST] Downloading Sentinel-2 product: {product_id}")
        download_path = Config.DOWNLOAD_CACHE
        self.api.download(product_id, directory_path=download_path)
        return os.path.join(download_path, product_id + ".zip")

if __name__ == "__main__":
    # Test for a specific city block (Example: Central Park, NYC)
    ingestor = SentinelIngestor()
    results = ingestor.search_area(40.7829, -73.9654)
    print(f"[INGEST] Found {len(results)} potential products.")
    if not results.empty:
        print(results[['title', 'cloudcoverpercentage', 'beginposition']].head())
