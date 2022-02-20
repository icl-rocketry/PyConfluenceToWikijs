class Page:
    """
    Class to store and process a single wiki page.

    Contains all its data, and operations on the page.
    This includes reading a page to the instance, and exporting it to the
    correct files.
    """
    
    def __init__(self, file_name):
        self.file_name = file_name
        self._import_from_file(self.file_name)

    def _import_from_file(self, file_name):
        '''
        Function that imports the data from the given file into the class, by parsing the html
        '''
        self.title = ""
        self.location = "" # Location within the hierarchy
        self._content = "" # The actual content of the page
        self._update_text = ""
        self.image_folder = ""