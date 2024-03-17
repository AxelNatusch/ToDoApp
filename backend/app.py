import os

import uvicorn

if __name__ == "__main__":
    if os.environ.get("ENV") == "development":
        uvicorn.run("src.main:app", host="0.0.0.0", port=8001, reload=True)
    else:
        uvicorn.run("src.main:app", host="0.0.0.0")
