#!/usr/bin/python
import sys
import logger
from resetTimestamp import resetTimestamps
from createArchive import createArchive
from createRelease import createRelease
from syncTimestamp import syncTimestampOverrideFile
from copyFiles import copyFiles
from config import openConfigFile
from versionFile import updateVersionFile

try:
    CONFIG_NAME = sys.argv[1]
except:
    logger.info("Usage: buildmod.py <config name>")
    sys.exit(1)
config = openConfigFile(CONFIG_NAME)

hasVersion = len(sys.argv) > 2
if hasVersion:
    version = sys.argv[2]
    logger.info(f"Version: {version}")

if hasVersion:
    updateVersionFile(config, version)

logger.header(f"Starting Build for {config['mod_name']}")
copyFiles(config)
resetTimestamps(config)
syncTimestampOverrideFile(config)

if hasVersion:
    createRelease(config, version)

createArchive(config)