# Arcane

Arcane serves as a web-based solution as part of my Harvard's CS50x final project, designed with a minimalist approach to tackle the complexities of newsletter management. It provides an intuitive remedy for subscriber handling, enabling the creation of engaging newsletters using a comprehensive text editor, and ensuring the distribution of personalized content. Through seamless integration with an email service, it optimizes communication efficiency and fosters increased engagement among subscribers. 

## Features

- **User Registration:** Easily create accounts for newsletter creators.
- **Subscriber Management:** Effortlessly handle subscriber lists, including additions.
- **Rich Text Editor:** Powerful tool for visually stunning newsletter content.
- **Newsletter Sending:** Schedule or send newsletters instantly to your subscriber list.
- **Responsive Design:** Enjoy a seamless experience across desktop and mobile devices.

## Tech Stack

- **Backend:** Python with Flask framework and SQLAlchemy for database management.
- **Frontend:** HTML, CSS, and JavaScript with Bootstrap for responsive design.
- **Database:** SQLAlchemy for development, MongoDB for production.
- **Email Service:** Integrates with an email service (Mailgun) to send newsletters and welcome emails.

## Getting Started
### Prerequisites
- Python 3.7+
- `virtualenv` (optional but recommended)
- MongoDB

### Installation
1. Clone the repository:
    ```bash
    git clone https://github.com/your-username/arcane.git
    cd arcane
    ```

2. Create a virtual environment (optional but recommended):
    ```bash
    python3 -m venv arcane_venv
    source arcane_venv/bin/activate
    ```

3. Install the required packages:
    ```bash
    pip install -r requirements.txt
    ```

## Usage

### Running the App
1. Configure your MongoDB URI in `.env`:
    ```plaintext
    DB_URI=your_mongodb_uri_here
    ```

2. Run the Flask app:
    ```bash
    python app.py
    ```

3. Access the app in your browser at `http://localhost:5000`.

## Configuration
- MongoDB URI: Update the `.env` file with your MongoDB URI.

## Contributing
Contributions are welcome! If you find a bug or have suggestions for improvements, please open an issue or create a pull request.
