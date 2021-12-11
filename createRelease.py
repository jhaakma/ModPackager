import logger
from git import Repo
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