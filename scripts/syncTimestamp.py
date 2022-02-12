import logger
import yaml

def syncTimestampOverrideFile(config):
    repoPath = config.get("repo_path")
    if not repoPath:
        logger.info("No repo path specified, skipping timestamp override")
        return
    timestamps = config.get("timestamps")
    if not timestamps:
        logger.info("No timestamp override specified, skipping timestamp sync")
        return
    logger.info("Creating timestamp override file")
    try:
        with open(repoPath + "/timestampOverrides.yaml", "w") as f:
            f.write(yaml.dump(timestamps))
            logger.success(f"Timestamp override file created successfully at '{repoPath}/timestampOverrides.yaml'")
    except Exception as e:
        logger.error(f"Failed to write timestamp override file. Exception: {e}")
