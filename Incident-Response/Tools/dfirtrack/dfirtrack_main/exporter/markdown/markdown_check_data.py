from django.contrib import messages
from dfirtrack_config.models import SystemExporterMarkdownConfigModel
from dfirtrack_main.logger.default_logger import warning_logger
import os

def check_config(request):
    """ check variables in config """

    # get config model
    model = SystemExporterMarkdownConfigModel.objects.get(system_exporter_markdown_config_name = 'SystemExporterMarkdownConfig')

    # reset stop condition
    stop_exporter_markdown = False

    # check MARKDOWN_PATH for empty string
    if not model.markdown_path:
        messages.error(request, "`MARKDOWN_PATH` contains an emtpy string. Check config!")
        # call logger
        warning_logger(str(request.user), " EXPORTER_MARKDOWN variable MARKDOWN_PATH empty string")
        stop_exporter_markdown = True

    # check MARKDOWN_PATH for existence in file system (check only if it actually is a non-empty string)
    if model.markdown_path:
        if not os.path.isdir(model.markdown_path):
            messages.error(request, "`MARKDOWN_PATH` does not exist in file system. Check config or filesystem!")
            # call logger
            warning_logger(str(request.user), " EXPORTER_MARKDOWN path MARKDOWN_PATH not existing")
            stop_exporter_markdown = True

    # check MARKDOWN_PATH for write permission (check only if it actually is a non-empty string)
    if model.markdown_path:
        if not os.access(model.markdown_path, os.W_OK):
            messages.error(request, "`MARKDOWN_PATH` is not writeable. Check config or filesystem!")
            # call logger
            warning_logger(str(request.user), " EXPORTER_MARKDOWN path MARKDOWN_PATH not writeable")
            stop_exporter_markdown = True

    return stop_exporter_markdown
