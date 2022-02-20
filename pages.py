from bs4 import BeautifulSoup
import string
import os

class Page:
    """
    Class to store and process a single wiki page.

    Contains all its data, and operations on the page.
    This includes reading a page to the instance, and exporting it to the
    correct files.
    """
    
    def __init__(self, file_name, wiki_name):
        self.file_name = file_name
        self._import_from_file(wiki_name)

    def convert_file_name(self, file_name_dict):
        '''
        Function used to generate the new file name used for export

        Adds a new key to the provided dictionary, such that the change can be kept track of
        '''

        # Generate a nice file name from the title
        self.new_file_name = self._format_filename(str(self.title))

        # Add conversion to dictionary so that it can be kept track of
        file_name_dict[self.file_name] = self.new_file_name


    def export_to_folder(self, destination_folder):
        '''
        Function to get the content of the page, and export it in the correct form and location
        within the destination folder.

        Takes a single argument, the destination folder. Creates folders as neccessary within that
        folder such as to emulate the previous hierarchy.
        '''



    def _import_from_file(self, wiki_name):
        '''
        Function that imports the data from the classes file into the class, by parsing the html
        '''

        file = open(self.file_name, 'r')
        file_data = file.read()
        file.close()

        html_data = BeautifulSoup(file_data, 'html.parser')

        # Title is prepended with the name of the wiki, plus a " : "; need to strip it
        title_chars_to_strip = len(wiki_name)+3
        self.title = html_data.title.string[title_chars_to_strip:]

        # Location within the hierarchy stored as list of names, going from root down
        self.location = list() 

        # Parse the breadcumbs section for the correct hierarchy
        hierarchy_section = html_data.find("ol", id="breadcrumbs")
        for item in hierarchy_section.find_all("li"):
            link_text = item.find("a").get("href")
            self.location.append(os.path.splitext(link_text)[0]) # Strip the .html extension

        self._content = html_data.find("div", class_="wiki-content group",id="main-content")

        self._update_text = html_data.find("div", class_ = "page-metadata").string

        self.id = os.path.splitext(file_name)[0][-9:] # Get only the 9 digit ID at the end of the filename before the extension


    @staticmethod
    def _format_filename(s):
        '''
        Take a string and return a valid filename constructed from the string.
        Uses a whitelist approach: any characters not present in valid_chars are
        removed. Also spaces are replaced with underscores.

        Blatantly stolen from this gist: https://gist.github.com/seanh/93666
        '''
        valid_chars = "-_() %s%s" % (string.ascii_letters, string.digits)
        filename = ''.join(c for c in s if c in valid_chars)
        filename = filename.replace(' ','_') # I don't like spaces in filenames.
        return filename
