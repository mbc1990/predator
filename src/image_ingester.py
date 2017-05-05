from ingester import Ingester
import hashlib

class ImageIngester(Ingester):
    """
    This is an ingester for a single image URL.
    This is typically created by another ingester
    that polls a web page or API for images
    """

    IMAGE_DIR = 'images/'

    def __init__(self, image_url):
        self.image_url = image_url

    @property 
    def source_name(self):
        return "Image Ingester"
    
    def should_run(self):
        return True

    def get_url(self):
        return self.image_url
     
    def parse_callback(self, result):
        """
        Handles the deduplication and saving step of an image.
        Right now this only saves to disk, but it should be
        writing to S3 or using EMR to do the deduplication+S3
        """
        fname = hashlib.md5(result).hexdigest()
        extension = self.image_url.split('.')[-1]
        with open(self.IMAGE_DIR+fname+'.'+extension, 'wb') as f:
            f.write(result)

        self.is_blocking = False
    
    def parse_error(self, error):
        """
        TODO: Logging
        """
        print error
        self.is_blocking = False

    def should_destroy(self):
        """
        Each ImageIngester should only ever run once
        """
        return not self.is_blocking 