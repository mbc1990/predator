from image_ingester import ImageIngester
from twisted.internet import reactor, task
from twisted.web.client import getPage

class Predator():

    def __init__(self):

        self.ingesters = self.initialize_ingesters()

    def initialize_ingesters(self):
        """
        Returns a list of instantiated ingesters
        """
        return [
        ]

    def add_ingester(self, ingester):
        """
        Adds an Ingester subclass. Typically 
        called by another ingester.
        """
        self.ingesters.append(ingester)

    def manage_ingesters(self):
        """
        Called in a loop, checks on ingesters and manages
        their output
        """
        while self.ingesters:
            for ingester in self.ingesters:
                
                # First, check if we can remove this ingester
                if ingester.should_destroy():
                    self.ingesters.remove(ingester)                    

                # Currently waiting for a callback from this
                # ingester
                if ingester.is_blocking:
                    continue
                
                if ingester.should_run():
                    ingester.is_blocking = True
                    d = getPage(ingester.get_url())
                    d.addCallback(ingester.parse_callback, self.add_ingester)
                    d.addErrback(ingester.parse_error)


def main():
    predator = Predator()

    manage = task.LoopingCall(predator.manage_ingesters)
    manage.start(1)

    reactor.run()


if __name__ == "__main__":
    main()
