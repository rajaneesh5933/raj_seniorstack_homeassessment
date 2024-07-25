# Video Platform Project

## Overview

This project is a web-based video platform built with Flask and Tailwind CSS. It allows users to search for videos, create playlists, and manage these playlists. The application fetches video data from a mock API and provides features like pagination, search functionality, and playlist management.

## Features

- **Search Videos**: Users can search for videos using keywords in the title or description.
- **Pagination**: The video list is paginated, allowing users to navigate through multiple pages of videos.
- **Create Playlists**: Users can select videos and create playlists.
- **View Playlists**: Users can view their created playlists.
- **Delete Playlists**: Users can delete their playlists.
- **Remove Videos from Playlists**: Users can remove individual videos from a playlist.

## Getting Started

### Prerequisites

- Python 3.7+
- Flask
- Requests

### Installation

1. **Clone the repository**:
    ```bash
    git clone https://github.com/rajaneesh5933/raj_seniorstack_homeassessment 
    cd video-platform
    ```

2. **Create a virtual environment**:
    ```bash
    python -m venv venv
    ```

3. **Activate the virtual environment**:
    - On Windows:
      ```bash
      venv\Scriptsctivate
      ```
    - On macOS/Linux:
      ```bash
      source venv/bin/activate
      ```

4. **Install Flask and Requests**:
    ```bash
    pip install Flask requests
    ```

### Running the Application

1. **Start the Flask application**:
    ```bash
    python app.py
    ```

2. **Open the application in your browser**:
    Navigate to `http://127.0.0.1:5000` in your web browser.

### Folder Structure

- `app.py`: The main Flask application file.
- `playlists.json`: A JSON file used to store playlists data.

### API Endpoints

- **`/`**: Main route that serves the HTML template.
- **`/videos`**: Fetches videos from the mock API, with optional search query and pagination.
- **`/playlists`**: 
  - `GET`: Retrieves all playlists.
  - `POST`: Creates or updates a playlist with the given name and videos.
- **`/playlists/<name>`**:
  - `GET`: Retrieves a specific playlist by name.
  - `DELETE`: Deletes a specific playlist by name.
- **`/playlists/<name>/videos/<video_id>`**: 
  - `DELETE`: Removes a specific video from a specific playlist.

### HTML Template

The HTML template is built with Tailwind CSS and includes:
- A search bar for searching videos.
- Buttons for creating and viewing playlists.
- A modal for creating playlists.
- A modal for viewing playlists.

### JavaScript Functionality

The JavaScript in the template provides:
- Fetching and displaying videos.
- Handling pagination.
- Managing selected videos for playlist creation.
- Handling playlist creation and deletion.
- Handling modal display and interactions.

## Future Enhancements

- Fetching video comments and likes from the API.
- User authentication for personalized playlists.
- Enhancing the UI with more features and better styling.
