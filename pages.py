import string
import os
from datetime import datetime
from shutil import copytree
from bs4 import BeautifulSoup

class Page:
    """
    Class to store and process a single wiki page.

    Contains all its data, and operations on the page.
    This includes reading a page to the instance, and exporting it to the
    correct files.
    """

    def __init__(self, path, wiki_name):
        self.path = os.path.split(path)[0]
        self.filename = os.path.split(path)[1]
        self._import_from_file(path, wiki_name)

    def convert_filename(self):
        '''
        Function used to generate the new file name used for export

        Returns the new filename
        '''

        # Generate a nice file name from the title
        new_filename = self._format_filename(str(self.title))

        return new_filename


    def convert_location(self, filename_dict):
        '''
        Convert the folder names within the location list to the new names, to keep it consistent
        '''
        new_location = []

        for folder in self.location[1:]: # We dont care about the first item, as it is the root
            # Convert the folder name if the corresponding name has also been converted,
            # otherwise just add the old one
            if folder in filename_dict:
                new_location.append(filename_dict[folder])
            else:
                new_location.append(folder)
        return new_location


    def export(self, new_location, destination_folder, path_dict):
        '''
        Function to get the content of the page, and export it in the correct form and location
        within the destination folder.

        Takes a three arguments; the local path within the hierarchy, the destination folder,
        and the dictionary containing the mapping between old and new files.
        The latter is used to update links.
        Creates folders as neccessary within that folder such as to emulate the previous hierarchy.
        '''
        page_path = os.path.join(destination_folder, new_location)
        new_dir = os.path.split(page_path)[0]

        # Create all necessary folders
        os.makedirs(new_dir, exist_ok=True)

        # Open the file for writing
        page_file = open(page_path, 'w', encoding="utf-8")

        # Write header
        # Current date and time in the right format
        dt_str = datetime.now().strftime("%Y-%m-%dT%H:%M:%S.000Z")
        page_file.write("<!--\n")
        page_file.write(f"title: {self.title}\n")
        page_file.write("description: \npublished: true\n")
        page_file.write(f"date: {dt_str}\n")
        page_file.write("tags: \neditor: ckeditor\n")
        page_file.write(f"dateCreated: {dt_str}\n")
        page_file.write("-->\n\n")

        # Write title
        page_file.write(f"<h1><strong>{self.title}</strong></h1>\n\n")

        # Write content, correcting links for the new placement.
        page_file.write(self._replace_links(str(self._content),
                        path_dict, os.path.split(new_location)[0]+"\n"))

        # Write footer
        page_file.write("<p><span class=\"text-tiny\"><i>Autogenerated using <a href=\"https://github.com/icl-rocketry/PyConfluenceToWikijs\">1337 h4xx0r 5k111z</a>, from ye olde Confluence Wiki</i></span></p>\n")
        page_file.write(f"<p><span class=\"text-tiny\"><i>Old Metadata: {self._metadata}</i></span></p>\n")
        page_file.write(f"<p><span class=\"text-tiny\"><i>ID: {self.id}</i></span></p>\n")

        # Write footer
        page_file.close()

        # Move media files to a new media folder
        media_origin = os.path.join(self.path, "attachments", self.id)
        if os.path.isdir(media_origin): # Check if there are any attachments
            media_folder = os.path.join(new_dir, "attachments", self.id)
            copytree(media_origin, media_folder, dirs_exist_ok=True)


    def _import_from_file(self, filename, wiki_name):
        '''
        Function that imports the data from the classes file into the class, by parsing the html
        '''

        file = open(filename, 'r', encoding="utf-8")
        file_data = file.read()
        file.close()

        html_data = BeautifulSoup(file_data, 'html.parser')

        # Title is prepended with the name of the wiki, plus a " : "; need to strip it
        title_chars_to_strip = len(wiki_name)+3
        self.title = html_data.title.string[title_chars_to_strip:]

        # Location within the hierarchy stored as list of names, going from root down
        self.location = []

        # Parse the breadcumbs section for the correct hierarchy
        hierarchy_section = html_data.find("ol", id="breadcrumbs")
        for item in hierarchy_section.find_all("li"):
            link_text = item.find("a").get("href")
            self.location.append(os.path.splitext(link_text)[0]) # Strip the .html extension

        self._content = html_data.find("div", class_="wiki-content group",id="main-content")

        self._metadata = html_data.find("div", class_ = "page-metadata").get_text().strip()

        # Get only the 9 digit ID at the end of the filename before the extension
        self.id = os.path.splitext(filename)[0][-9:]


    @staticmethod
    def _format_filename(unformatted_filename):
        '''
        Take a string and return a valid filename constructed from the string.
        Uses a whitelist approach: any characters not present in valid_chars are
        removed. Also spaces are replaced with underscores.

        Blatantly stolen from this gist: https://gist.github.com/seanh/93666
        '''
        valid_chars = f"-_() {string.ascii_letters}{string.digits}"
        filename = ''.join(c for c in unformatted_filename if c in valid_chars)
        filename = filename.replace(' ','_') # I don't like spaces in filenames.
        return filename

    @staticmethod
    def _replace_links(original_text, link_dictionary, curr_dir):
        '''
        Uses the dictionary to replace all occurences of links in the file
        with one updated using the dictionary
        '''
        # Create new copy of the string
        rep_s = original_text[:]
        for key in link_dictionary:
            rep_s = rep_s.replace(key, os.path.relpath(link_dictionary[key], curr_dir))

        return rep_s
