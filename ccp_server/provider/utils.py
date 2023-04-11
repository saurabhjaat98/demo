###############################################################################
# Copyright (c) 2023-present CorEdge India Pvt. Ltd - All Rights Reserved     #
# Unauthorized copying of this file, via any medium is strictly prohibited    #
# Proprietary and confidential                                                #
# Written by Bhaskar Tank <bhaskar@coredge.io>, Feb 2023                      #
###############################################################################
import re
from datetime import datetime

# Regular expression pattern that extract filename from the given path.
FILE_NAME_EXTRACTOR_REGEX = r"/([^/]+)$"
TIMESTAMP_FORMAT: str = "%Y-%m-%d %H:%M:%S"


async def get_file_name(file_path):
    # Search for the pattern in the file path
    match = re.search(FILE_NAME_EXTRACTOR_REGEX, file_path)
    # Extract the filename from the match object
    return match.group(1)


def format_datetime(date: str, source_format: str, destination_format: str = TIMESTAMP_FORMAT) -> str:
    """
    Formats a datetime object given source and destination format and returns a UTC datetime object.
    :param date: str: string representing datetime in the source format.
    :param source_format: str: The format used in the str parameter.
    :param destination_format: str: The destination format to convert to.
    :return: UTCDatetime.
    """
    dt_obj = datetime.strptime(date, source_format)
    dt_obj = dt_obj.astimezone(datetime.timezone.utc)
    return datetime.strftime(dt_obj, destination_format)
