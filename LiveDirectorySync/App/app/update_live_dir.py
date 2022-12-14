import logging
import os
import re
from typing import List
from sql_connectors import connect_single
from yaml_parser import get_yaml


def get_folders(logger: logging.Logger, src: str, fmt: str):
    """Gets list of directories from src """
    command = f'ls {src} | grep {fmt}'
    logger.debug(f'command as : {command}')
    try:
        text = os.popen(command).read().split()
        logging.debug(f'{text[0:5]}')
        logging.info(f'got {len(text)} folders from dir listing')

        return text

    except Exception as e:
        logger.critical(f'failed to get live directory listing')


def sql_ise(text):
    return f"('{text}')"


def push_folders_to_db(logger: logging.Logger, folders: List[str], fmt: str):
    """pushes list of directories into postgres db"""

    logger.debug(f"{', '.join([sql_ise(f) for f in folders[0:6] if re.match(fmt,f)])}")

    query = f"""
    INSERT INTO pipeline.tmp_live(file_name)
    VALUES {', '.join([sql_ise(f) for f in folders if re.match(fmt,f)])};
    """
    try:
        connect_single(logger, query)
    except Exception as e:
        logger.critical(f'failed to push folders to postgres')


def push_new_folders(logger):
    """Add new directories to live directory table  """

    query = """
    INSERT INTO pipeline.live_directory(file_name)
    (SELECT tmp.file_name
     FROM pipeline.tmp_live as tmp
     LEFT JOIN pipeline.live_directory as live
     ON tmp.file_name = live.file_name
     WHERE live.file_name IS NULL
    ) 
    """

    query_reset = """
        DELETE FROM pipeline.tmp_live
        """

    try:
        connect_single(logger, query)
        connect_single(logger, query_reset)
    except Exception as e:
        logger.critical(f'failed to move folders to live directory table')


def update_live_db(logger: logging.Logger, src: str):
    """Updates live directory DB"""

    fmts = get_yaml()['Extensions']

    for regex_value in fmts:
        fmt = str(regex_value).encode().decode('unicode_escape')
        logger.info(f'searching for {fmt}')
        folders = get_folders(logger, src, fmt)
        logging.info(f'got {len(folders)} folders from dir listing')
        push_folders_to_db(logger, folders, fmt)
        logger.info(f'pushed folders to tmp db')
        push_new_folders(logger)
        logger.info(f'pushed new folders')
