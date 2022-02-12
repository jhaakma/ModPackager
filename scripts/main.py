#!/usr/bin/python
import logger
import argparse
from resetTimestamp import resetTimestamps
from createArchive import createArchive
from createRelease import createRelease
from syncTimestamp import syncTimestampOverrideFile
from copyFiles import copyFiles
from openConfigFile import openConfigFile
from versionFile import updateVersionFile, appendVersionPrefix

# Parse the arguments
parser = argparse.ArgumentParser(description = "Create a release of the project")

subparser = parser.add_subparsers(dest = "command")
sync = subparser.add_parser("sync", help = "sync files from source")
build = subparser.add_parser("build", help = "build the project")
release = subparser.add_parser("release", help = "create a release")

parser.add_argument("name", help="name of the mod to package")
release.add_argument("version", help = "the version to release")

args = parser.parse_args()

def sync(config):
    logger.header(f"Syncing files for {config['mod_name']}")
    copyFiles(config)

def build(config):
    logger.header(f"Building {config['mod_name']}")
    resetTimestamps(config)
    syncTimestampOverrideFile(config)
    createArchive(config)

def release(config, version):
    logger.header(f"Creating release {args.version} for {config['mod_name']}")
    createRelease(config, version)


config = openConfigFile(args.name)
if args.command == 'sync':
    sync(config)

if args.command == 'build':
    sync(config)
    build(config)

if args.command == 'release':
    appendVersionPrefix(args.version)
    updateVersionFile(config, args.version)
    sync(config)
    build(config)
    release(config, args.version)