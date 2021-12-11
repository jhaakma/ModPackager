#!/usr/bin/python
import sys
import impl
import logger

try:
    CONFIG_NAME = sys.argv[1]
except:
    logger.info("Usage: buildmod.py <config name>")
    sys.exit(1)
config = impl.openConfigFile(CONFIG_NAME)

hasVersion = len(sys.argv) > 2
if hasVersion:
    version = sys.argv[2]
    logger.info(f"Version: {version}")

if hasVersion:
    impl.updateVersionFile(config, version)

logger.header(f"Starting Build for {config['mod_name']}")
impl.copyFiles(config)

if hasVersion:
    impl.createRelease(config, version)
impl.createArchive(config)