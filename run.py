"""{...}."""

import uvicorn
import sthali_auth
import sthali_core

app = sthali_core.run_server(sthali_auth.Config, sthali_auth.AppSpecification, sthali_auth.SthaliAuth)


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
