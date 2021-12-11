import logger
import py7zr
#Add data files to archive
def createArchive(config):
    logger.header("Creating 7z file")
    try:
        archivePath = config["archive_path"]
    except:
        logger.info("No archive path specified, skipping archive creation")
        return
    try:
        repoPath = config["repo_path"]
    except:
        raise Exception("No master home specified")
    try:
        with py7zr.SevenZipFile(archivePath, 'w') as archive:
            archive.writeall(f"{repoPath}/Data Files", "Data Files")
        logger.success(f"Archive created successfully at '{archivePath}'")
    except Exception as e:
        logger.error(f"Failed to create archive. Exception: {e}")