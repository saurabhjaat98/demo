    # Unit Test cases

## Instructions
 - Install requirements.txt.
 - Install test-requirements.txt for **test case dependencies only**.
 - All UTs to go under this directory.
 - A separate file to be created for each source .py file. Example, for ```utils.py```, the UT file name will be ```test_utils.py```. For ```general.py```, the UT file name will be ```test_general.py``` and so on.
 - Each ```test_*.py``` will import the method/class that needs to be tested.
    If you are writing test cases for a class called class XYZ, the UT test class will be defined as ```class TestXYZ(unittest.TestCase)```.
    Each test case should have a docstring describing the test case.
    Preferably **define ```main()``` in each UT file** so that any particular file can be executed individually to help other developers in saving time.
    Example:
    ```python
    if __name__ == '__main__':
        unittest.main(verbosity=2)
    ```
 - Write UTs in a way that you mock external API calls. Example, mock Keycloak, OpenStack API calls.
 - UTs to follow Behavior-driven development (BDD) and should be written using Given-When-Then (GWT) approach.
 - To run all tests, ```python runner.py```
 - To run a single file tests, ```python test_aggregate.py```
