# Filekit

A tiny Python library for finding and processing files.

![Filekit logo: a balloon that says 'filekit' on it](https://raw.githubusercontent.com/foundling/filekit/master/media/filekit.png?sanitize=false)

### Installation

For now, use `curl` or a similiar tool:

````bash
curl -O https://raw.githubusercontent.com/foundling/filekit/master/filekit.py
````

### What it Does

`filekit` handles opening, closing, reading and writing to files. You get to supply the functions that use the filehandle.  Partial application is a useful technique when using this library. It's explained in the examples.

**API**:

+ [find_files](#find_files)
+ [process_files](#process_files)

## find_files

````python
def find_files(
    root_dir=None, 
    subdir_pattern=None, 
    filename_pattern=None, 
    filename_filter=None
):
````

### Usage

+ `find_files` will match files in a specified directory using either a `filename_pattern` function or a `filename_filter` string, starting at the `root_dir`. 
+ If a `subdir_pattern` is provided, it is used to match against subdirectories of the `root_dir` argument. 
+ Passing a `subdir_pattern`  will group resulting files by their matching parent directory.


### Arguments

#### `root_dir`

Exact name of the base directory used in the file search. Defaults to current directory in which the script is run, i.e., `os.path.abspath(os.curdir)`.

#### `filename_pattern`

Pattern used for matching against result files.  Defaults to `'.*'`.

#### `subdir_pattern`

Pattern to match when searching for subdirectories.  Defaults to `'.*'`.

#### `filter_fn`

A function used as a predicate for filtering resulting filename matches.  Defaults to `None`.

### Returns

`find_files` returns a dictionary of arrays containing matched files whose keys are their parent directory. All filepaths in the keys and array values are absolute filepaths.

### Examples

#### Standard Usage

Given a current working directory tree that looks like this:
    
    test_data/
    ├── regular
    │   ├── subject_1.csv
    │   ├── subject_2.csv
    │   ├── subject_2.csv

We can run `find_files` in this way:

````python
from filekit import find_files
files = find_files(root_dir='test_data/regular', filename_pattern='subject')
````

This yields the following results:

````python
{ 
    '/Users/alex/filekit/test_data/regular': [
        '/Users/alex/filekit/test_data/regular/subject_1.csv',
        '/Users/alex/filekit/test_data/regular/subject_2.csv',
        '/Users/alex/filekit/test_data/regular/subject_3.csv'
    ]
}
````


#### Using the `subdir_pattern` option

Given a directory tree like this:

    └── test_data
		└── subdirs
			├── backupdata
			│   └── data.csv
			├── subject_1
			│   └── data.csv
			├── subject_10
			│   └── data.csv
			├── subject_2
			│   └── data.csv
			├── subject_3
			│   └── data.csv
			├── subject_4
			│   └── data.csv
			├── subject_5
			│   └── data.csv
			├── subject_6
			│   └── data.csv
			├── subject_7
			│   └── data.csv
			├── subject_8
			│   └── data.csv
			└── subject_9
				└── data.csv

We can run `find_files` with the `subdir_pattern` option in the following way:

    from filekit import find_files 
    files = find_files(dir='test_data/subdirs', subdir_pattern='subject_.*[0-9]')

This yeilds the following results:

````
 { 
    '/Users/alex/filekit/test_data/subdirs/subject_1': [ '/Users/alex/filekit/test_data/subdirs/subject_1/data.csv'],
    '/Users/alex/filekit/test_data/subdirs/subject_10': [ '/Users/alex/filekit/test_data/subdirs/subject_10/data.csv'],
    '/Users/alex/filekit/test_data/subdirs/subject_2': [ '/Users/alex/filekit/test_data/subdirs/subject_2/data.csv'],
    '/Users/alex/filekit/test_data/subdirs/subject_3': [ '/Users/alex/filekit/test_data/subdirs/subject_3/data.csv'],
    '/Users/alex/filekit/test_data/subdirs/subject_4': [ '/Users/alex/filekit/test_data/subdirs/subject_4/data.csv'],
    '/Users/alex/filekit/test_data/subdirs/subject_5': [ '/Users/alex/filekit/test_data/subdirs/subject_5/data.csv'],
    '/Users/alex/filekit/test_data/subdirs/subject_6': [ '/Users/alex/filekit/test_data/subdirs/subject_6/data.csv'],
    '/Users/alex/filekit/test_data/subdirs/subject_7': [ '/Users/alex/filekit/test_data/subdirs/subject_7/data.csv'],
    '/Users/alex/filekit/test_data/subdirs/subject_8': [ '/Users/alex/filekit/test_data/subdirs/subject_8/data.csv'],
    '/Users/alex/filekit/test_data/subdirs/subject_9': [ '/Users/alex/filekit/test_data/subdirs/subject_9/data.csv']
}   
````


## process_files

````python
def process_files(filepaths, callback, mode='r')
````

### Usage

`process_files` takes a sequence of `filepaths` and a `callback` function. It then opens each file in sequence, calls the provided callback on the open file handle, and then closes the filehandle.  `process_files` returns the values from each callback in an array.  Note that the filehandles are automatically closed, so it is not necessary to call the filehandle's `close` method in your callback.

### Arguments

#### `process_files`
An iterable.

#### `callback`
The function to run on each opened file in `filepaths`.

###### Arguments 
The `filehandle` for an opened file.

###### Returns
If the callback returns a value, `process_files` will return these values in an array. 

#### `mode`
The mode used for opening each filepath in `filepaths`. Defaults to `'r'`.


### Example

````python
results = find_files(
    root_dir='output', 
    subdir_pattern='sub', 
    filename_pattern='subject_[0-9].csv', 
    filename_filter=None
)

for dir, files in results.items():
    line_counts = process_files(files, callback=line_count)
        print(line_counts)
````
