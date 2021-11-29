import api_easiedata
import json
from src.error import MissingDataFrame


class Easie():
    """
        A class that is used to comunicate with easiedata api for loading and
        extracting data

        Parameters
        ----------

        user : str
            easiedata username
        developer_key : str
            easiedata generated developer key
        url_api : str
            url from easiedata api chosen to comunicate
    """

    def __init__(self, user, developer_key, url_api):
        self.user = user
        self.developer_key = developer_key
        self.url_api = url_api
        self.easie_api = api_easiedata.easie_usertb.EasieUsertb(
            self.user, self.developer_key, self.url_api
        )

        self.post_res = []
        self.get_res = []

    @classmethod
    def from_settings(cls, settings):
        return cls(**settings['easie'])

    def post_in_easie(self, dfs_params):
        """
            Method to insert data in easiedata

            Parameters
            ----------

            dfs_params: list
                list of with object with parameters for data insertion in easie
                {
                    "table_name": str
                        easie table name,
                    "action": str
                        action to be performed,
                    "df": pd.DataFrame
                        Data to be inserted
                    "params": {
                        not_exists_create: bool
                            If table doesnt exists it creates it
                        replace: bool
                            Replaces the data in table in easie with data
                            being sent
                    }

                }
        """

        for data in dfs_params:
            data['table_name'] = f"{data['table_name']} @{self.user}"
            post_res = {
                'table_name': data['table_name'],
                'res': {}
            }
            try:
                self.easie_api.post_easieusertb(**data)
                post_res['res'] = json.loads(str(self.easie_api))
                self.post_res.append(post_res)
            except Exception as e:
                post_res["res"]['success'] = False
                post_res["res"]['Exception'] = json.dumps(e.args)
                self.post_res.append(post_res)

        return self

    def get_easie_tables(self, table_names):
        """
            Method to retrieve data from tables in easie

            Parameters
            ----------
            table_names: list
                Names of tables in easie
        """

        dfs = {}
        for tb in table_names:
            table_name = f'{tb} @{self.user}'
            res_get = self.easie_api.get_easieusertb(table_name)

            if not hasattr(res_get, 'df'):
                self.get_res.append(json.loads(str(res_get)))
                raise MissingDataFrame(tb)
                
            dfs[tb] = res_get.df
            del res_get.df
        return dfs
