import os
from pages import Page

class Wiki:
    '''
    Class encompassing the actual wiki, with all its pages and images
    Will call page methods in order to build the wiki
    '''

    # Variables to store the relationship between the old and new paths
    filename_dict = {}
    path_dict = {}

    def __init__(self, input_folder, wiki_name, ext = ".html"):
        self.input_folder = input_folder
        self.ext = ext # File extension of data files
        self.wiki_name = wiki_name # Name of the wiki, such as to remove it from HTML titles
        # List containing all the pages within the wiki
        self.pages = self._import_pages(self.input_folder)

    def convert_pages(self):
        '''
        Generate the conversion dictionaries for all the pages,
        such as the new file name and location
        '''
        for page in self.pages:
            self.filename_dict[os.path.splitext(page.filename)[0]] = page.convert_filename()

        for page in self.pages:
            self.path_dict[page.filename] = os.path.join(*page.convert_location(self.filename_dict),
                                            self.filename_dict[os.path.splitext(page.filename)[0]]
                                            + self.ext)


    def export_pages(self, output_dir):
        '''
        Export all the pages to the provided directory
        '''
        for page in self.pages:
            page.export(self.path_dict[page.filename], output_dir, self.path_dict)


    def _import_pages(self, input_folder):
        '''
        Import all the files from the input folder as pages
        Return list containing all the pages
        '''

        page_list = []
        for file_in_dir in os.listdir(input_folder):
            # Store all html files but do not convert index.html,
            # as it is not actuallly part of the wiki
            if file_in_dir.endswith(self.ext) and file_in_dir != "index.html":
                print("Importing " + file_in_dir + "...")
                page_list.append(Page(os.path.join(input_folder,file_in_dir), self.wiki_name))

        return page_list
