"""
    Simple package for maintaining config file
    By Anang Faturrohman <anang42429@gmail.com>
"""

from configobj import ConfigObj
from dataclasses import dataclass

import os

resource_path = os.path.join(os.path.dirname(__file__), '..', 'resource')

if os.path.exists(os.path.join(resource_path, 'config.conf')):
    config = ConfigObj(os.path.join(resource_path, 'config.conf'))

@dataclass
class DatabaseSettings:

    __main = config.get('DATABASE', {})    #type: ignore

    srv = bool(__main.get('srv', 0))

    user = __main.get('username', 'guest')
    passw = __main.get('password', 'guest123')
    database = __main.get('db_name', 'transfer')

    if not srv:
        host = __main.get('host', '127.0.0.1')
        port = int(__main.get('port', 27017))
    else:
        cluster = __main.get('cluster', None)
        host = f"mongodb+srv://{user}:{passw}@{cluster}/{database}?retryWrites=true&w=majority"


    # Records Collection Name
    record_collection_name = __main.get('main_collection', 'transfer_log')
    history_collection_name = __main.get('history_collection', 'history')
    dev_collection_name = __main.get('development', 'test_data')


@dataclass
class TelegramSetting:
    __main = config.get('TELEGRAM', {})
    token = __main.get('token', 'NOTOKEN')
