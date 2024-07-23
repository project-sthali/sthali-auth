import os

from spec_example import EXAMPLE_SPEC
from sthali_auth import AppSpecification, SthaliAuth, load_and_parse_spec_file


spec_file_path = os.getenv("SPEC_FILE_PATH")
app_spec_dict = load_and_parse_spec_file(spec_file_path) if spec_file_path else EXAMPLE_SPEC
client = SthaliAuth(AppSpecification(**app_spec_dict))
app = client.app
