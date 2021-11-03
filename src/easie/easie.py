import api_easiedata
from src.utils import utils


class Easie():

    def __init__(self):
        settings = utils.get_settings()
        self.user = settings['easie']['user']
        self.developer_key = settings['easie']['developer_key']
        self.url_api = settings['easie']['url_api']
        self.easie_api = api_easiedata.easie_usertb.EasieUsertb(
            self.user, self.developer_key, self.url_api
        )

        return None

    def insert_in_easie(self, dfs_params):
        self.insertion_res = {}
        for k, v in dfs_params.items():
            self.insertion_res[k] = {}
            table_name = f'{k} @{self.user}'
            try:
                self.easie_api.post_easieusertb('insert_with_df', table_name, **v)
                self.insertion_res[k] = self.easie_api.res
            except Exception as e:
                self.insertion_res[k]['success'] = False
                self.insertion_res[k]['Exception'] = e.args
        
        return self

    def get_easie_tables(self, table_names):
        self.dfs = dict()
        for tb in table_names:
            table_name = f'{tb} @{self.user}'
            res_get = self.easie_api.get_easieusertb(table_name)
            self.dfs[tb] = res_get.df
            del res_get.df

        return self


        
        