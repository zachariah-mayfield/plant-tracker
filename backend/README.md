# Plant Tracker API

This project is a gardening/plant tracking web application built with FastAPI.
It provides an API to manage plants using a YAML file as the database.

## How to Run in a Python Virtua Environment.

1. Create and activate a virtual environment.
    ```bash
    python -m venv venv
    source venv/Scripts/activate
    ```
2. Install dependencies:
    ```bash
    pip install -r requirements.txt
    ```
3. Run the application:
    ```bash
    uvicorn main:app --reload
    ```

## How to Build and Run the Docker Container

1. Open a terminal in the plant-tracker/backend/ folder:

### Build the image
    ```bash
    docker build -t plant-tracker-backend .
    ```
### Run the container and to make Data Persistent (Optional for Now). This mounts your local data/ folder into the container.
    ```bash
    docker run -d -p 8000:8000 --name plant-tracker-api \ 
    -v "$(pwd)/data:/app/data" \ 
    plant-tracker-backend
    ```

### Then visit:
http://localhost:8000/docs


## Endpoints

- **GET /plants**: Returns a list of all plants from the database.
- **GET /plants/{id}**: Fetches a single plant by its id. Returns a 404 if not found.
- **POST /plants**: Creates a new plant. Requires a name, type, and notes (optional).
- **PUT /plants/{id}**: Updates an existing plant by id. If the plant doesn't exist, returns 404.
- **DELETE /plants/{id}**: Deletes the plant by id. If it doesn't exist, returns 404.