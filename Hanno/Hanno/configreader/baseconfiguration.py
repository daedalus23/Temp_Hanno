from collections.abc import Iterable


__all__ = ["BaseConfiguration"]


"""
BaseConfiguration module/class is base level attributes of both
shared types of configuration usage Single/Multiple. Adding
file extensions to BaseConfiguration attribute 'configFileTypes'
more file extensions can be loaded & read.
"""


class BaseConfiguration:

    sections = []
    content = {}
    configFileTypes = [
        "ini", "cnf", "conf"
    ]

    def _check_config_path(self, path):
        """Check for config file in path"""
        for fileType in self.configFileTypes:
            if fileType in path:
                return True
            else:
                return False

    @staticmethod
    def check_iterator(item):
        """Check if object is iterable"""
        excluded_types = str
        if isinstance(item, Iterable) and not isinstance(item, excluded_types):
            return True
        else:
            return False

    def parse_path(self, fullPath):
        """Separate file name & path"""
        tempPath = list(fullPath.split("\\"))
        for fileType in self.configFileTypes:
            if fileType in tempPath[-1].lower():
                fileNameLen = len(tempPath[-1])
                pathDiff = len(fullPath) - fileNameLen
                return fullPath[0:pathDiff], tempPath[-1]

    @staticmethod
    def prepare_content(newContent):
        """Parse Key from Dict to set Section name of config.ini"""
        sectionName = list(newContent.keys())[0]
        sectionContent = newContent[sectionName]
        return sectionName, sectionContent
