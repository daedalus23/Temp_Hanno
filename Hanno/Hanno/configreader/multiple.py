from configparser import SafeConfigParser
from configparser import ConfigParser
from .baseconfiguration import BaseConfiguration

import os


__all__ = ["Multiple"]


# TODO:
#   Multiple module/class add_multi_content not working
#       multiple.py line 36: add_multi_content
#           baseconfiguration.py line 48: prepare_content
#       AttributeError: 'list' object has no attribute 'keys'


"""
Multiple module/class parses & loads configuration file sections,
content from a given directory. Takes file directory & will load
dict format data into 'multiContent' attribute named as file name
in directory.
"""


class Multiple(BaseConfiguration):

    _ConfigObj = None
    multiContent = {}
    _multiDirectory = None
    _fileObject = None
    _dirList = []
    _numConfigs = 0

    def add_multi_content(self, newContent, fileName):
        """Adds new section & content to configObj"""
        for configFile in self._dirList:
            if fileName == configFile["fileName"]:
                self._fileObject = configFile
                self._multi_load_content()
        sectionName, sectionContent = self.prepare_content(newContent)
        self._ConfigObj[f"{sectionName.lower()}"] = sectionContent
        self._multi_write_file()

    def clear_multi_cache(self):
        """Clear & reset cache for next configuration file to be loaded"""
        self._ConfigObj = ConfigParser()
        self.sections = []
        self.content = {}

    @staticmethod
    def create_config_dict(file, path):
        """Create config file structure of file information"""
        tempfileName, tempfileExt = file.split(".")
        tempFile = {
            "fileName": tempfileName,
            "fileExt": tempfileExt,
            "fullFileName": file,
            "filePath": rf"{path}\{file}"
        }
        return tempFile

    def _check_multi_config(self):
        """Check if path is directory of configuration files"""
        for file in os.listdir(self._multiDirectory):
            for fileType in Multiple.configFileTypes:
                if fileType in file.split(".")[1]:
                    self._numConfigs += 1
                    self._dirList.append(
                        self.create_config_dict(file, self._multiDirectory)
                    )

    def load_multi(self, path):
        """Load directory of config files"""
        self._multiDirectory = path
        self._check_multi_config()
        os.chdir(self._multiDirectory)
        for configFile in self._dirList:
            self._fileObject = configFile
            self._multi_load_content()
            self.clear_multi_cache()

    def _multi_load_content(self):
        """Load content from config file & return dict."""
        self._multi_load_sections()
        parser = SafeConfigParser()
        parser.optionxform = str
        found = parser.read(self._fileObject["fullFileName"])
        if not found:
            raise ValueError('No config file found!')
        for name in self.sections:
            self.content[f"{name}"] = dict(parser.items(name))
        self.multiContent[self._fileObject["fileName"]] = self.content

    def _multi_load_sections(self):
        """Load all sections of ini file into class sections list."""
        self._multi_read_file()
        self.sections = self._ConfigObj.sections()

    def _multi_read_file(self):
        """Read file from path and return content."""
        with open(self._fileObject["fullFileName"], "r") as file:
            self._ConfigObj.read_file(file)

    def _multi_write_file(self):
        """Writes ConfigObj to class INI file"""
        with open(self._fileObject["fullFileName"], "w") as file:
            self._ConfigObj.write(file)
