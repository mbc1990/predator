import json
import sys
from image_ingester import ImageIngester
from twitter_ingester import TwitterIngester
from twisted.internet import reactor, task
from twisted.web.client import getPage

class Predator():
    """
    Event based consumer of cute animal photos
    """
    MAX_CONCURRENT_CONNECTIONS = 5

    def __init__(self, config):
        self.ingesters = self.initialize_ingesters(config['bearer_token'], config['twitter_ingesters'])

    def initialize_ingesters(self, twitter_bearer_token, twitter_ingesters):
        """
        Returns a list of instantiated ingesters
        """
        ingesters = []
        for ing in twitter_ingesters:
            screen_name = ing['screen_name']
            source_name = ing['source_name']
            ti = TwitterIngester(screen_name, source_name,
                                 twitter_bearer_token,
                                 self.add_image_ingester)
            ingesters.append(ti)

        return ingesters

    def add_image_ingester(self, url, source_name):
        """
        Adds a new image ingester, usually passed to a 
        different ingester that finds image URLs
        """
        image_ingester = ImageIngester(url, source_name)
        self.ingesters.append(image_ingester)

    def manage_ingesters(self):
        """
        Called in a loop, checks on ingesters and manages
        their output
        """
        concurrent = 0
        for ingester in self.ingesters:
            
            # First, check if we can remove this ingester
            if ingester.should_destroy():
                self.ingesters.remove(ingester)                    

            # Currently waiting for a callback from this
            # ingester
            if ingester.is_blocking:
                concurrent += 1
                continue
            
            if ingester.should_run() and concurrent < self.MAX_CONCURRENT_CONNECTIONS:
                ingester.is_blocking = True
                url = ingester.get_url()
                d = getPage(ingester.get_url(), timeout=3,
                            headers=ingester.get_headers())
                d.addCallback(ingester.parse_callback)
                d.addErrback(ingester.parse_error)


def main():
    config_path = sys.argv[1]

    with open(config_path) as config_file:    
        config = json.load(config_file)

    predator = Predator(config)

    manage = task.LoopingCall(predator.manage_ingesters)
    manage.start(1)

    reactor.run()


if __name__ == "__main__":
    main()
