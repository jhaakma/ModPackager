import pathlib, logger, yaml
#Fetches the configs from the specified file
def openConfigFile(configName):
    configPath = str(pathlib.Path(__file__).parent.resolve()) + '\\config\\' + configName + '.yaml'
    with open(configPath, 'r') as stream:
        try:
            config = yaml.safe_load(stream)
        except yaml.YAMLError as exception:
            logger.error(exception)
        return config
