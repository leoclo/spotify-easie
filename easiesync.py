import api_easiedata
import sys
from src.easie import Easie
from src.spotify import spotify
from src.utils import utils



class EasieSync(Easie):

    def __getitem__(self, k):
        return getattr(self, k)


    def spotify_artists(self):
        return spotify.get_artists(self.settings, self.easie)







if __name__ == '__main__':
    easie_sync = EasieSync()[sys.argv[2]]()

    print('Done')
