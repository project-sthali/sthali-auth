"""{...}."""

import os

import uvicorn
import sthali_auth


dependency = sthali_auth.dependencies.APIKeyAuth(sthali_auth.clients)

app_specification_file_path = os.getenv("APP_SPECIFICATION_FILE_PATH") or "volume/app_specification_sample.json"
config = sthali_auth.Config(app_specification_file_path)
app_specification_dict = config.app_specification
client = sthali_auth.SthaliAuth(sthali_auth.AppSpecification(**app_specification_dict, dependencies=[dependency]))
app = client.app


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
