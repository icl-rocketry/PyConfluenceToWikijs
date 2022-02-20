from pages import Page

class Wiki:
    '''
    Class encompassing the actual wiki, with all its pages and images
    Will call page methods in order to build the wiki
    '''

    def __init__(self, input_folder):
        self.input_folder = input_folder
        self.pages = self._import_pages(self.input_folder) # List containing all the pages within the wiki

    def _import_pages(input_folder):
        '''
        Import all the files from the input folder as pages
        Return list containing all the pages
        '''

        # some sort of loop required, for every file name
        page_list = Page("")

        return page_list

