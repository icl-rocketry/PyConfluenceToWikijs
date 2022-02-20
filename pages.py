from bs4 import BeautifulSoup

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

        file = open(file_name, 'r')
        file_data = file.read()
        file.close()

        html_data = BeautifulSoup(file_data, 'html.parser')

        self.title = html_data.title

        # Location within the hierarchy stored as list of names, going from root down
        self.location = list() 

        # Parse the breadcumbs section for the correct hierarchy
        hierarchy_section = html_data.find("ol", id="breadcrumbs")
        for item in hierarchy_section.find_all("li"):
            link_text = item.find("a").get("href")
            self.location.append(link_text[:-5]) # Strip the .html extension

        self._content = html_data.find("div", class_="wiki-content group",id="main-content")

        self._update_text = html_data.find("div", class_ = "page-metadata")

        self.id = file_name[-14:-5] # Get only the 9 digit ID at the end of the filename before the extension
