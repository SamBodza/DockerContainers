import logging
import os
import time

from sql_connectors import connect_single
from config_parser import get_config
from yaml_parser import get_yaml


def get_folders_to_sync(logger):
    """Get ordered list of folders to sync """

    try:
        query = """
        SELECT file_name
        FROM pipeline.live_directory
        WHERE up_to_date = False
        """
        fldrs = connect_single(logger, query, get=True)
        logging.info(f'found {len(fldrs)} folders to sync')

        if not fldrs:
            logging.info('All folders up to date, resetting')
            query_reset = """
            UPDATE pipeline.live_directory
            SET up_to_date = False
            """
            connect_single(logger, query_reset)
            get_folders_to_sync(logger)

    except Exception as e:
        logging.critical(f'unable to get folders to sync')

    return fldrs


def rsync_folder(fldr: str):
    """Sync a single patient folder across to working dir"""

    paths = get_config()['PATHS']
    try:
        src = os.path.join(paths['src_dir'], fldr[0])
        dst = os.path.join(paths['dst_dir'], fldr[0])
        logging.debug(f'{src} : {dst}')
        if os.path.exists(src):
            command = f'rsync -avi {src} {dst}'
            logging.debug(f'found folder {fldr}')
            text = os.popen(command).read().split()

            return text
        else:
            logging.error(f'could nto find {fldr}')
    except Exception as e:
        logging.error(f'failed to rsync {fldr} : {e}')


def add_file_to_db(logger, fldr):
    """Adds new file to db"""

    logging.debug(f'adding {fldr}, into working files')
    try:
        query = f"""
                INSERT INTO pipeline.working_files
                    (file_name)
                SELECT 
                    '{fldr[0]}'
                WHERE
                    NOT EXISTS (
                        SELECT file_name 
                        FROM pipeline.working_files 
                        WHERE file_name = '{fldr[0]}');
                """

        connect_single(logger, query)

    except Exception as e:
        logging.critical(f'unable to get folders to sync')


def update_dbs(logger, fldr: str):
    """Update working dir db with new folder
    and live dir with new value"""

    query = f"""
    UPDATE pipeline.live_directory
    SET up_to_date = True
    WHERE file_name = '{fldr[0]}'
    """
    connect_single(logger, query)


def get_time_to_run(logger):
    """Get time to run from yaml file"""
    yaml = get_yaml(logger)
    added_time = int(yaml['Runtime']['Hours']) * 3600 + int(yaml['Runtime']['Minutes']) * 60 + int(
        yaml['Runtime']['Seconds'])
    return time.time() + added_time


def rsync_folders_for_time(logger):
    """rsync as many folders as possible in set time"""

    time_out = get_time_to_run(logger)
    logger.info(f'set time out for {time_out}')
    fldrs = sorted(get_folders_to_sync(logger))
    logger.info(f'got {len(fldrs)} folders to sync')
    for fldr in fldrs:
        logger.debug(f'syncing {fldr}')
        if time_out > time.time():
            try:
                text = rsync_folder(fldr)
                logger.debug(f'syncing {fldr}')
                add_file_to_db(logger, fldr)
                logger.debug(f'added {fldr} to working dir')
                update_dbs(logger, fldr)
                logger.debug(f'updating liv dir for {fldr}')
            except Exception as e:
                logging.error(f'unable to sync {fldr}: {e}')
        else:
            break
