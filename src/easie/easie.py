import api_easiedata


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
        self.insertion_res = {}

    @classmethod
    def from_settings(cls, settings):
        return cls(**settings['easie'])

    def insert_in_easie(self, dfs_params):
        """
            Method to insert data in easiedata

            Parameters
            ----------

            dfs_params: list
                list of with object with parameters for data insertion in easie
                {
                    "table_name": str
                        easie table name
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
            self.insertion_res[data['table_name']] = {}
            try:
                self.easie_api.post_easieusertb('insert_with_df', **data)
                self.insertion_res[data['table_name']] = self.easie_api.res
            except Exception as e:
                self.insertion_res[data['table_name']]['success'] = False
                self.insertion_res[data['table_name']]['Exception'] = e.args

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
            dfs[tb] = res_get.df
            del res_get.df

        return dfs
