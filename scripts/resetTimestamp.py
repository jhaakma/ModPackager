from datetime import datetime
import time
import logger
import os
from pathlib import Path

def setTimeStamp(filepath, timestamp):
    os.utime(filepath, (timestamp, timestamp))

def resetTimestamps(config):
    logger.info("Resetting timestamps")
    timestamps = config.get("timestamps")
    if not timestamps:
        logger.warn("No timestamps found, skipping reset")
        return
    masterpath = config.get("repo_path")
    if not masterpath:
        logger.warn("No master path found, skipping reset")
        return
    for fileData in timestamps:
        filepath = fileData.get("path")
        timestamp = fileData.get("timestamp")
        if not filepath or not timestamp:
            logger.warn("Invalid timestamp data, skipping")
            continue

        fullpath = Path(os.path.join(masterpath, "Data Files", filepath))
        setTimeStamp(fullpath, timestamp)
        logger.success(f"Successfully Reset timestamp for {filepath} to {timestamp}")