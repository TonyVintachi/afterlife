# Forensic Information Management System (FIMS)

This project is a web application designed to manage forensic pathology information, track processes within a forensic department, and utilize RFID tags (simulated for now) to track bodies within the system. This system is being developed with consideration for the South African market.

## Project Status

This project is currently in the initial setup phase. Basic Django structure, database models (Case, Body, RFIDTag), admin interface, and a placeholder homepage have been created.

## Getting Started

Follow these instructions to set up and run the project locally.

### Prerequisites

*   Python 3.8 or newer
*   `pip` (Python package installer)
*   `virtualenv` (optional, but recommended)

### Setup Instructions

1.  **Clone the repository (if you haven't already):**
    ```bash
    git clone <repository_url>
    cd forensic_system
    ```
    *(Note: If you are running this locally from the files I generate, you'll already be in the `forensic_system` directory or its parent.)*

2.  **Create and activate a virtual environment (recommended):**
    ```bash
    python -m venv venv
    # On Windows
    # venv\Scripts\activate
    # On macOS/Linux
    # source venv/bin/activate
    ```

3.  **Install dependencies:**
    (Ensure `requirements.txt` is in the project root)
    ```bash
    pip install -r requirements.txt
    ```

4.  **Database Setup:**
    Navigate to the directory containing `manage.py` (the `forensic_system` project root).

    *   **Apply database migrations:**
        ```bash
        python manage.py migrate
        ```
    *   **Create a superuser account (for accessing the admin panel):**
        ```bash
        python manage.py createsuperuser
        ```
        Follow the prompts to choose a username, email (optional), and password.

5.  **Running the Development Server:**
    Once the setup is complete, you can run the Django development server:
    ```bash
    python manage.py runserver
    ```
    By default, the server will be accessible at `http://127.0.0.1:8000/`.

    *   **Admin Interface:** `http://127.0.0.1:8000/admin/`
        (Log in with the superuser credentials you created)
    *   **Management App Homepage:** `http://127.0.0.1:8000/management/`

### Running Tests

To run the automated tests for the `management` app:
```bash
python manage.py test management
```
This command will discover and run tests within the `management` application.
