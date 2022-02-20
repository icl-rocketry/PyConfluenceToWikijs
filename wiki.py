from pages import Page
import os

class Wiki:
    '''
    Class encompassing the actual wiki, with all its pages and images
    Will call page methods in order to build the wiki
    '''

    def __init__(self, input_folder, ext, wiki_name):
        self.input_folder = input_folder
        self.ext = ext # File extension of data files
        self.wiki_name = wiki_name # Name of the wiki, such as to remove it from HTML titles
        self.pages = self._import_pages(self.input_folder) # List containing all the pages within the wiki


    def _import_pages(self, input_folder):
        '''
        Import all the files from the input folder as pages
        Return list containing all the pages
        '''

        page_list = list()
        for file_in_dir in os.listdir(input_folder):
            # Store all html files but do not convert index.html, as it is not actuallly part of the wiki
            if file_in_dir.endswith(self.ext) and file_in_dir != "index.html":
                print("Importing " + file_in_dir + "...")
                page_list.append(Page(os.path.join(input_folder,file_in_dir), self.wiki_name))

        return page_list
