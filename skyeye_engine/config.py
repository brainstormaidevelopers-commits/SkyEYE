import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    # --- API CREDENTIALS (Load from .env on Windows) ---
    SCIHUB_USER = os.getenv("SCIHUB_USER", "guest")
    SCIHUB_PASS = os.getenv("SCIHUB_PASS", "guest")
    
    # --- DIRECTORY CONFIG ---
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))
    DOWNLOAD_CACHE = os.path.join(BASE_DIR, "output", "cache")
    RECONSTRUCTIONS_DIR = os.path.join(BASE_DIR, "output", "reconstructions")
    
    # --- SENSOR STACK & STAC CONFIG (Doctrine v1) ---
    STAC_ENDPOINTS = {
        "copernicus": "https://dataspace.copernicus.eu/apis/stac",
        "planetary_computer": "https://planetarycomputer.microsoft.com/api/stac/v1",
        "earth_search": "https://earth-search.aws.element84.com/v1"
    }

    TAXONOMY = {
        "visual.optical": ["sentinel-2-l2a", "landsat-c2-l2", "planet-scope"],
        "structure.radar": ["sentinel-1-grd"],
        "thermal.land_surface": ["landsat-8-tirs", "viirs-nrt", "modis-nrt"],
        "atmosphere.chemistry": ["sentinel-5p-l2"],
        "weather.clouds": ["goes-abi-l2"],
        "terrain.elevation": ["copernicus-dem", "srtm-30m"],
        "hazards.seismic": ["usgs-earthquake-v1"]
    }

    # Provider-Native Credentials extension
    USGS_M2M_API_KEY = os.getenv("USGS_M2M_API_KEY")
    PLANET_API_KEY = os.getenv("PLANET_API_KEY")

    
    # --- PLANETARY SCALE PARAMETERS (Doctrine v1) ---
    UNCERTAINTY_DECAY_RATE = 0.05  # Confidence loss per hour since last observation
    GEOSPATIAL_SHARD_SIZE = 100.0  # km per world chunk for TGH sharding
    VALIDATION_STRICTNESS = 0.8    # Threshold for Genesis to reject a delta
    TEMPORAL_GRANULARITY = 60      # Seconds between snapshot pulses
    
    # --- TRIGGER SETTINGS ---
    THERMAL_ANOMALY_THRESHOLD = 20.0  # Celsius above baseline
    EVENT_SCORE_MIN = 5.0  # Minimum score to trigger reconstruction


# Ensure cache directories exist
os.makedirs(Config.DOWNLOAD_CACHE, exist_ok=True)
os.makedirs(Config.RECONSTRUCTIONS_DIR, exist_ok=True)
