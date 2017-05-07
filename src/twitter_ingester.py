from ingester import Ingester
from image_ingester import ImageIngester

class TwitterIngester(Ingester):
    """
    Ingests images from a particular twitter account
    Dead simple web scraper, doesn't even touch the API
    """
    ENDPOINT = 'https://api.twitter.com/1.1/statuses/user_timeline.json'


    def __init__(self, screen_name, source_name, bearer_token):
        # TODO: Construct twitter API call
        self.url = self.ENDPOINT + '?screen_name='+screen_name
        self.source = source_name
        self.bearer_token = bearer_token
    
    def source_name(self):
        return self.source
    
    def should_run(self):
        # TODO: This should only run ever x minutes
        return True

    def get_headers(self):
        return {'Authorization':'Bearer %s' % self.bearer_token}

    def get_url(self):
        """
        Returns the URL to be queried
        """
        return self.url
     
    def parse_callback(self, result, add_ingester=None):
        self.is_blocking = False
        # TODO: Parse webpage
        # TODO: Collect images
        # TODO: Add image ingesters
    
    def parse_error(self, error):
        # TODO: Logging
        print error

    def should_destroy(self):
        return False
