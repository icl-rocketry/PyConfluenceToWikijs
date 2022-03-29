# PyConfluenceToWikijs
Python scripts used to convert the Confluence based wiki to a format that is usable with Wiki.js.

Based loosely on [this tool by gkpln3](https://github.com/gkpln3/ConfluenceToWikiJS), though ported to python, and with enhanced capability.

Features:

 - Preserved page hierarchy, converted to use folders
 - Files renamed to their title rather than just their ID
 - Working links between pages
 - Working images
 - Working non-image attachments (though no previews)
 - HTML not formatted as a single line (which is what confluence does by default)
 - Metadata (page edit times) preserved, and saved to the footer of each page

[Documented here](https://wiki.imperial.ac.uk/display/IRW/Confluence+to+Wiki.js+Conversion) (on old wiki for now!)