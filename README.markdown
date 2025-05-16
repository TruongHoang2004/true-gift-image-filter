# TrueGift RAG Indexer

A FastAPI-based application for applying various image filters to uploaded images. The application allows users to upload an image, apply a specified filter with customizable strength, and download the processed image. It also provides endpoints to list available filters and preview filter effects on a sample image.

## Features
- **Image Filtering**: Apply filters like grayscale, sepia, blur, and more to uploaded images.
- **Filter Preview**: Generate previews of filter effects on a sample image.
- **Filter List**: Retrieve a list of available filters with descriptions.
- **CORS Support**: Configured to allow cross-origin requests.
- **Streaming Response**: Efficiently stream processed images to clients.

## Prerequisites
Before setting up and running the application, ensure you have the following installed:
- **Python** 3.8 or higher
- **pip** (Python package manager)
- A working internet connection to download dependencies
- (Optional) **Git** for cloning the repository

## Installation

1. **Clone the Repository** (if applicable):
   ```bash
   git clone <repository-url>
   cd <repository-directory>
   ```

2. **Create a Virtual Environment** (recommended):
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install Dependencies**:
   Install the required Python packages using the provided `requirements.txt` (create this file if not already present) or manually install the packages.
   ```bash
   pip install fastapi uvicorn pillow python-multipart
   ```
   Alternatively, create a `requirements.txt` with the following content:
   ```
   fastapi==0.115.0
   uvicorn==0.30.6
   pillow==10.4.0
   python-multipart==0.0.9
   ```
   Then run:
   ```bash
   pip install -r requirements.txt
   ```

4. **Ensure the `filter.py` Module**:
   The application depends on a `filter.py` module that contains the `apply_image_filter` function and `FilterTypeLiteral`. Ensure this file is present in the same directory as `main.py` and correctly implemented. If you don't have this module, you may need to implement the image filtering logic using PIL or another library.

## Running the Application

1. **Start the FastAPI Server**:
   Run the application using Uvicorn, the ASGI server implementation for FastAPI.
   ```bash
   uvicorn main:app --host 0.0.0.0 --port 8000 --reload
   ```
   - `--host 0.0.0.0`: Makes the server accessible externally.
   - `--port 8000`: Specifies the port (change if needed).
   - `--reload`: Enables auto-reload for development (remove in production).

2. **Access the Application**:
   Once the server is running, the API will be available at:
   ```
   http://localhost:8000
   ```
   You can also access the interactive API documentation (Swagger UI) at:
   ```
   http://localhost:8000/docs
   ```

## API Endpoints

### 1. Apply Filter to an Image
- **Endpoint**: `POST /image/filter`
- **Description**: Upload an image, apply a filter, and receive the processed image.
- **Parameters**:
  - `file`: Image file (e.g., JPEG, PNG, GIF)
  - `filter_name`: Name of the filter (e.g., `grayscale`, `sepia`)
  - `strength`: Optional filter strength (0.0 to 2.0, default: 1.0)
- **Example Request** (using `curl`):
  ```bash
  curl -X POST "http://localhost:8000/image/filter" \
  -F "file=@/path/to/image.jpg" \
  -F "filter_name=grayscale" \
  -F "strength=1.0" \
  --output filtered_image.jpg
  ```
- **Response**: Streamed image file with the applied filter.

### 2. List Available Filters
- **Endpoint**: `GET /image/filters`
- **Description**: Retrieve a list of available filters with descriptions.
- **Example Request**:
  ```bash
  curl http://localhost:8000/image/filters
  ```
- **Response**:
  ```json
  {
    "available_filters": {
      "grayscale": "Convert image to grayscale",
      "sepia": "Apply classic sepia tone effect",
      ...
    }
  }
  ```

### 3. Preview Filter Effect
- **Endpoint**: `GET /image/filter/preview/{filter_name}`
- **Description**: Apply a filter to a sample image and return the result.
- **Parameters**:
  - `filter_name`: Name of the filter (e.g., `grayscale`, `sepia`)
  - `strength`: Optional filter strength (0.0 to 2.0, default: 1.0)
- **Example Request**:
  ```bash
  curl "http://localhost:8000/image/filter/preview/grayscale?strength=1.0" --output preview.jpg
  ```
- **Response**: Streamed JPEG image with the filter applied to a sample image.

## Usage Notes
- **Supported Image Formats**: The application supports JPEG, PNG, and GIF. Other formats may need conversion to RGB mode.
- **Filter Strength**: Adjust the `strength` parameter to control the intensity of the filter effect (0.0 to 2.0).
- **CORS Configuration**: The application allows all origins by default. For production, restrict `allow_origins` to specific domains.
- **Error Handling**: The API returns HTTP exceptions with detailed error messages for invalid inputs or processing errors.

## Troubleshooting
- **ModuleNotFoundError for `filter`**: Ensure the `filter.py` file exists and contains the required `apply_image_filter` function and `FilterTypeLiteral` type.
- **Pillow Errors**: Verify that the uploaded image is valid and supported. Ensure PIL is installed (`pip install pillow`).
- **Port Conflicts**: If port 8000 is in use, change the port using the `--port` option in the `uvicorn` command.
- **CORS Issues**: If requests are blocked, verify the `allow_origins` setting in the CORS middleware.

## Contributing
Contributions are welcome! Please submit a pull request or open an issue on the repository for bugs, feature requests, or improvements.

## License
This project is licensed under the MIT License. See the `LICENSE` file for details (if applicable).