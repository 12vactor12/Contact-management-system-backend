# Contact Management System Backend Documentation

## Project Structure

The project is structured as follows:

```
└─ src
    │  myWeb.py          # Main backend application code
    │  requirements.txt   # Python package dependencies
```

## Overview

This document provides details on setting up and running the backend for the Contact Management System, which is built using Flask.

## Prerequisites

Before running the application, ensure that you have the following installed:

- Python 3.6 or higher
- pip (Python package installer)

## Setup

1. **Clone the Repository:**

   Clone the project repository to your local machine.

   ```bash
   git clone <repository_url>
   cd <repository_directory>/src
   ```

2. **Create a Virtual Environment (optional but recommended):**

   It’s a good practice to create a virtual environment for Python projects to manage dependencies separately.

   ```bash
   python -m venv venv
   source venv/bin/activate   # On Windows use `venv\Scripts\activate`
   ```

3. **Install Dependencies:**

   Use the `requirements.txt` file to install the necessary packages.

   ```bash
   pip install -r requirements.txt
   ```

## Running the Application

To start the backend server, execute the following command:

```bash
python myWeb.py
```

The server will start on the default port (5000). You can access it at:

```
http://127.0.0.1:5000
```

## API Endpoints

### 1. Get All Contacts

- **URL:** `/contacts`
- **Method:** `GET`
- **Description:** Retrieve a list of all contacts.

### 2. Get Contact by ID

- **URL:** `/contacts/<id>`
- **Method:** `GET`
- **Description:** Retrieve a specific contact by ID.

### 3. Create a New Contact

- **URL:** `/contacts`
- **Method:** `POST`
- **Description:** Create a new contact.
- **Request Body:** JSON object containing contact details.

### 4. Update a Contact

- **URL:** `/contacts/<id>`
- **Method:** `PUT`
- **Description:** Update an existing contact by ID.
- **Request Body:** JSON object containing updated contact details.

### 5. Delete a Contact

- **URL:** `/contacts/<id>`
- **Method:** `DELETE`
- **Description:** Delete a contact by ID.

## Testing

To ensure the application is working correctly, run the tests using your preferred testing framework (like `unittest` or `pytest`). The tests should be located in a separate directory.

## Conclusion

This document provides the necessary instructions for setting up and running the backend of the Contact Management System. For further details, refer to the source code and comments within the application files.
