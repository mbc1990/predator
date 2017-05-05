from twisted.internet import reactor, task
from twisted.web.client import getPage

class Predator():

    def __init__(self):

        self.ingesters = self.initialize_ingesters()

    def initialize_ingesters(self):
        """
        Returns a list of instantiated ingesters
        """
        return []

    def manage_ingesters(self):
        """
        Called in a loop, checks on ingesters and manages
        their output
        """
        while True:
            for ingester in self.ingesters:
                # Currently waiting for a callback from this
                # ingester
                if ingester.is_blocking:
                    continue
                
                if ingester.should_run():
                    ingester.is_blocking = True
                    d = getPage(ingester.get_url())
                    d.addCallback(ingester.parse_callback)
                    d.addErrback(ingester.parse_error)


def main():
    predator = Predator()
    manage = task.LoopingCall(predator.manage_ingesters)
    manage.start(1)
    reactor.run()


if __name__ == "__main__":
    main()
