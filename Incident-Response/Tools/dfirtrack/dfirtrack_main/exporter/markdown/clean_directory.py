from dfirtrack_config.models import SystemExporterMarkdownConfigModel
from dfirtrack_main.logger.default_logger import debug_logger, info_logger
import os
import shutil


def clean_directory(request_user):
    """ function to clean the system path within the markdown directory """

    # get config model
    model = SystemExporterMarkdownConfigModel.objects.get(system_exporter_markdown_config_name = 'SystemExporterMarkdownConfig')

    # clean or create markdown directory
    if os.path.exists(model.markdown_path + "/docs/systems/"):
        # remove markdown directory (recursivly)
        shutil.rmtree(model.markdown_path + "/docs/systems/")
        # recreate markdown directory
        os.mkdir(model.markdown_path + "/docs/systems/")
        # call logger
        debug_logger(request_user, " SYSTEM_MARKDOWN_ALL_SYSTEMS_DIRECTORY_CLEANED")
    else:
        # create markdown directory
        os.makedirs(model.markdown_path + "/docs/systems/")
        # call logger
        info_logger(request_user, " SYSTEM_MARKDOWN_FOLDER_CREATED")
