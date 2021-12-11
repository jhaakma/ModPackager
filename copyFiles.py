import os
import shutil
import errno
import logger

#Copies file or folder from src to dst
def copyFileOrFolder(src, dest):
    try:
        shutil.copytree(src, dest)
        logger.info(f"Copied folder from '{src}' to '{dest}")
    except OSError as exc: # python >2.5
        if exc.errno in (errno.ENOTDIR, errno.EINVAL):
            shutil.copy(src, dest)
            logger.info(f"Copied file from '{src}' to '{dest}")
        else: raise

def removeExistingFileOrFolder(filePath):
    try:
        shutil.rmtree(filePath)
        logger.info(f"Removed folder at {filePath}")

    except:
        try:
            os.remove(filePath)
            logger.info(f"Removed file at {filePath}")
        except:
            logger.info(f"{filePath} does not exist, skipping remove")

#Copy files from Morrowind install folder into build folder
def copyFiles(config):
    if not "contents" in config:
        logger.info("No files to copy")
        return

    logger.info("Copying files from Morrowind to repo")
    for contentPath in config["contents"]:
        src = f'{config["morrowind_path"]}/Data Files/{contentPath}'
        dest = f'{config["repo_path"]}/Data Files/{contentPath}'

        removeExistingFileOrFolder(dest)
        try:
            copyFileOrFolder(src, dest)
        except Exception as e:
            logger.error(f"Failed to copy file from {contentPath}. Exception: {e}")
    logger.success("Copy successful")