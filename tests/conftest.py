import os

# https://stackoverflow.com/questions/5137497/find-current-directory-and-files-directory
dir_path = os.path.dirname(os.path.realpath(__file__))


# https://stackoverflow.com/questions/36141024/how-to-pass-environment-variables-to-pytest
def pytest_generate_tests(metafunc):
    # Let us replace system commands with our own versions for testing purposes
    os.environ['PATH'] = f"{dir_path}/binmocks:{os.environ['PATH']}"
