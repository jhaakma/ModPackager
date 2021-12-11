import os
import shutil
import pathlib
import yaml
import py7zr
import errno
import logger
from git import Repo

#Fetches the configs from the specified file
def openConfigFile(configName):
    configPath = str(pathlib.Path(__file__).parent.resolve()) + '\\config\\' + configName + '.yaml'
    with open(configPath, 'r') as stream:
        try:
            config = yaml.safe_load(stream)
        except yaml.YAMLError as exception:
            logger.error(exception)
        return config

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

#Commit changes to git, set release tag and push to remote
def createRelease(config, version):
    logger.header(f"Creating Release for Version {version}")
    logger.info("Checking out master branch")
    try:
        repo = Repo(config['repo_path'])
    except:
        logger.warn("No repo configured, skipping release")
    repo.heads.master.checkout()
    logger.info("Pull from origin")
    repo.remotes.origin.pull()
    logger.info("Add local changes")
    repo.git.add('.')
    logger.info("Commit local changes")
    repo.index.commit(version)
    logger.info("Set release version tag")
    try:
        repo.create_tag(version)
    except Exception as e:
        logger.warn(f"Version {version} already exists, skipping tag creation")
    logger.info("Push to origin")
    origin = repo.remote(name='origin')
    origin.push(tags=True)
    origin.push()
    logger.success("Release created successfully")

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