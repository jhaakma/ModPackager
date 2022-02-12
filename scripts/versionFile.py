import logger

#Updates the configured version.text file
def updateVersionFile(config, version):
    try:
        versionFile = config['morrowind_path'] + "/"  + config["version_path"]
    except:
        print("No version file specified, skipping version update")
        return
    try:
        with open(versionFile, "w") as f:
            f.write(version)
        logger.success(f"Updated version file to {version}")
    except Exception as e:
        logger.error(f"Failed to update version file. Exception: {e}")

#Ensures that the version number starts with a 'v', which is required to trigger the release workflow opn Github
def appendVersionPrefix(version):
    if not version.startswith("v"):
        version = "v" + version
