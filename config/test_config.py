
from dotenv import load_dotenv
import os

def test_env():
    load_dotenv()
    test_string = os.getenv('TEST')
    # breakpoint()
    assert test_string == 'test-string'
