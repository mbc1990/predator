class Ingester():
    """
    Base class for ingesters of different sources.

    Ingesters should be thought of as short lived scrapers
    and API readers that are frequently run and maintain
    their own in-memory state regarding timing limitations 
    of APIs.

    Ingesters do not worry about deduplication or storage,
    they simply parse a particular webpage or API into images
    and return them.
    """
    def __init__(self):
        pass
    
    # set True while waiting for a callback
    is_blocking = False

    def source_name(self):
        """
        Returns a human readable source name e.g. "r/cute front page"
        """
        raise NotImplementedError()
    
    def should_run(self):
        """
        Returns True or False, determining if the ingester should run
        """
        raise NotImplementedError()

    def get_headers(self):
        """
        Returns header parameters, use for authenticating API requests
        in ingesters
        """
        return {}

    def get_url(self):
        """
        Returns the URL to be queried
        """
        raise NotImplementedError()
     
    def parse_callback(self, result, add_ingester=None):
        """
        result - return value of getPage
        add_ingester - method on Predator that adds an
        ingester to the event list

        Returns an array of image URLs to download

        Must set is_blocking to False 
        """
        raise NotImplementedError()
    
    def parse_error(self, error):
        """
        Parses the error case callback. Use for logging.

        Must set is_blocking to False 
        """
        raise NotImplementedError()

    def should_destroy(self):
        """
        Returns true if the ingester is no longer needed and
        can be removed from the event loop
        """
        raise NotImplementedError()
