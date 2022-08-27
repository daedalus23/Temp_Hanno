from .single import Single
from .multiple import Multiple


"""
Configuration class determines single or multiple configuration
files to be loaded. Single configuration file has more ConfigObject
flexibility, due to multiple purely loads configuration file content
into class object & then clearing cache 'ConfigObject'. Acceptable
configuration files that can be loaded must contain file extensions:
                    ('ini', 'cnf', 'conf')
"""


class Configuration(Single, Multiple, object):

    singleFile = None

    def __init__(self, path):
        """
        Load single configuration file  or Load directory of config files;
        :param path: --> str: Path given of config file or directory
        """
        self.path = path
        self._check_single_config()
        if self.singleFile:
            self.load_single(self.path)
        else:
            self.load_multi(path)

    def _check_single_config(self):
        """
        Check if path is single configuration file or directory.
        :return: singleFile --> bool: Determining file path given is directory or absolute file path
        """
        while self.singleFile is None:
            for fileType in Single.configFileTypes:
                if self.path.split(".")[-1] in fileType:
                    self.singleFile = True
            if self.singleFile is None:
                break
