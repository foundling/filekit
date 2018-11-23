import os
import re
import pprint

def make_filter(pattern):

    def filter(s): 
        return re.compile(pattern).search(s)

    return filter

def find_files(
    root_dir=None, 
    filename_pattern=None, 
    filename_filter=None, 
    dirname_pattern=None, 
    dirname_filter=None ):

    if root_dir is None:
        root_dir = os.path.abspath(os.curdir)

    results = { 
        'filename_pattern': filename_pattern, 
        'dirname_pattern': dirname_pattern, 
        'results': []
    }

    if not filename_filter:
        filename_filter = make_filter(filename_pattern or  '.*')

    if not dirname_filter:
        dirname_filter = make_filter(dirname_pattern or '.*')

    for dirpath, dirnames, filenames in os.walk(root_dir):

        path_key = os.path.abspath(dirpath)
        if dirname_filter(path_key):

            matches = [ os.path.abspath(os.path.join(dirpath, filename))
                        for filename in filenames 
                        if filename_filter(filename) and dirname_filter(path_key) ]

            if len(matches): 
                results['results'].extend(matches)


    return results

def process_files(files=[], callback=lambda x: x):
    ''' 
        Takes an array of relative filepaths, opens them and calls callback on each open file handle.
    '''  

    results = []

    for file in files:
        with open(file,'r') as fh:
            results.append(callback(fh))

    return results
