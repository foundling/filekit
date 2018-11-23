import os
import pytest
from filekit import find_files, process_files
import shutil

test_data = '''
'id','avg_hr_min','avg_hr_hour','pk_hr','low_hr'
1,60.7,360,78,71
2,70.0,330,80,58
3,72.2,350,82,78
6,61.8,300,70,63
'''


@pytest.fixture(scope="module", autouse=True)
def build_test_dir():

    # setup before each test
    if 'test' in os.listdir('.'):
        shutil.rmtree('test')

    os.mkdir('test')
    os.mkdir('test/subjects')
    os.mkdir('test/subjects/heart_data')
    os.mkdir('test/subjects/sleep_data')

    with open('test/subjects/heart_data/123_heart.csv','w+') as fh:
        fh.write(test_data)

    with open('test/subjects/sleep_data/123_sleep.csv','w+') as fh:
        fh.write(test_data)

    # test is run
    yield 

    if 'test' in os.listdir('.'):
        shutil.rmtree('test')

def test_find_files_defaults():

    os.chdir('test')
    base_path = os.path.abspath(os.curdir)

    test_filepaths = [ 
        os.path.join(base_path,'subjects/heart_data/123_heart.csv'),
        os.path.join(base_path,'subjects/sleep_data/123_sleep.csv')
    ]
    results = find_files()
    assert str(sorted(results['results'])) == str(sorted(test_filepaths))
