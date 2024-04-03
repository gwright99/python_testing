Links:
- https://pypi.org/project/moto/
- https://medium.com/@seifeddinerajhi/unit-testing-aws-lambda-with-python-and-mock-aws-services-using-moto-80e1855c16e1


! `from moto import mock_s3` not working.
    - Replaced in v5 with `mock_aws`: https://github.com/getmoto/moto/blob/master/CHANGELOG.md
    - Breaking change: All decorators have been replaced with a single decorator: mock_aws


```bash
# Fixture not found
~/python_testing/moto$ pytest -v --disable-socket -s test/test_main.py

# works but errors
:~/python_testing/moto$ pytest -v --disable-socket

# Works with both tests
$ ~/python_testing/moto/pytest -v -s --disable-socket
```