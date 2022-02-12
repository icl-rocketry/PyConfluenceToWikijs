def confluence2wikijs(inputFolder, outputFolder):
    '''
    Function that creates a new folder containing the converted files
    '''
    '''
    Need to extract:
    - Title
    - location within hierarchy
    - content
    - links (and what they refer to)

    Processing:
    - Need to work out what the new path of each file is (dictionary?)
    - Need to yeet away empty files (with no content)
    - Need to flag up any attachments (that cant be auto converted)

    Needs to create in the output folder, a html file with:
    - Placed in the correct sub-folder so that it reflects the hierarchy
    - HTML header correct so that wikijs doesn't freak out
    - title, content etc within the page
    - All links modified to relfect the modified paths
    - A footer saying that this file was auto-converted, and ideally what the last edit was and the creation when it was auto-converted
    '''
