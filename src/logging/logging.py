import json
import pandas as pd
import sys
from datetime import datetime
from functools import wraps
from src.core import core
from src.easie import Easie
from src.spotify import Spotify
from src.utils import utils


def logging(func):
    """ Decorator to build the insertion log and insert in easiedata """
    @wraps(func)
    def log_method(*args, **kwargs):
        easiesync, e = func(*args, **kwargs)
        return Logging(utils.get_settings()).build_log(easiesync, e)

    return log_method


class Logging():
    """
        A class that is used to build and insert the log of the easiedata api 
        requests

        Parameters
        ----------
        settings: dict
        
    """
    def __init__(self, settings):
        self.easie = Easie(**settings['easie'])
        self.logging = settings['logging']

    def __getitem__(self, k):
        return getattr(self, k)

    def find_easie_errors(self, res):
        """
            Method to find only unsuccessful api requests  

            Parameters
            ----------
            res: list
                list of all res of the easiedata api requests
        """
        return [r for r in res if not r['res']['success']]

    def build_log(self, easiesync, e):
        """
            Method to mount and select necessary information to build log 

            Parameters
            ----------
            easiesync: Easiesync object 
                easiesync object used in the insertion in easiedata,
            e: exception object
                exception object that contains any exception that occurred 
                during insertion in easiedata
        """
        if not self.logging['easie_error_tb'] and not self.logging['easie_error_file']:
            return None

        post_res = None
        get_res = None
        if easiesync is not None:
            post_res = easiesync.easie.post_res 
            get_res = easiesync.easie.get_res

            if not self.logging['save_success'] and len(post_res) > 0:
                post_res = self.find_easie_errors(post_res)

            if len(post_res) == 0:
                if e is None: 
                    return None

                post_res = None

            if len(get_res) == 0:
                get_res = None

        return self.insert_log(post_res=post_res, get_res=get_res, e=e)
 
    def insert_log(self, post_res=None, get_res=None, e=None):
        """
            Method to build dataframe with log information and insert in easiedata 

            Parameters
            ----------
            post_res: list
                list of res of the api post requests,
            get_res: list
                list of res of the api get requests,
            e: exception object
                exception object that contains any exception that occurred 
                during insertion in easiedata
        """
        if e is not None:
            e = str(e)

        if post_res is not None:
            post_res = json.dumps(post_res)

        if get_res is not None:
            get_res = json.dumps(get_res)

        columns = ['timestamp', 'post_res', 'get_res', 'exception']
        data = [[datetime.now(), post_res, get_res, e]]

        df = pd.DataFrame(data,columns=columns)
        
        if self.logging['easie_error_file']:
            with open(self.logging['easie_error_filename'], 'a') as f:
                f.write(str(data) + '\n')
        
        if self.logging['easie_error_tb']:
            params = {
                'not_exists_create': True,
                'replace': False
            }

            df_params = [{
                'table_name': self.logging['easie_error_tb_name'], 
                'action': 'insert_with_df',
                'df': df,
                'params': params
            }]

            self.easie.post_in_easie(df_params)



        return None
