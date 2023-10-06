# 2023-10-06 Initiated a py file

# import
import configparser

# import - Own utils
from utility import SFUtil

# read configs
config = configparser.ConfigParser()        # instance
configFile = SFUtil.initiate_env_var('ConfigFile')
config.read(configFile)

print(configFile)