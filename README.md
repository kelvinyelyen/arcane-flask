# Arcane

## Introduction

Arcane serves as a web-based solution as part of my Harvard's CS50x final project, designed with a minimalist approach to tackle the complexities of newsletter management. It provides an intuitive remedy for subscriber handling, enabling the creation of engaging newsletters using a comprehensive text editor, and ensuring the distribution of personalized content. Through seamless integration with an email service, it optimizes communication efficiency and fosters increased engagement among subscribers.

## Tech Stack

- [**Flask**](https://flask.palletsprojects.com/en/2.3.x/) - Framework
- [**Bootstrap**](https://getbootstrap.com/) - Responsive design
- [**SQLAlchemy**](https://www.sqlalchemy.org/) - Development database
- [**MongoDB**](https://www.mongodb.com/) - Production database
- [**Mailgun**](https://www.mailgun.com/) - Email Service
- [Resend](https://resend.com/) - Email Service 

## Getting Started

### Prerequisites

- Python 3.10+
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

   ```python
   DB_URI=your_mongodb_uri_here
   ```

2. Run the Flask app:

   ```bash
   python app.py
   ```

3. Access the app in your browser at `http://localhost:5000`.

## Configuration

- MongoDB URI: Update the `.env` file with your MongoDB URI.

## Found an issue or have a suggestion?

&lt;a href="https://github.com/kelvinyelyen/arcane/issues/new" target="\_blank"&gt;Create an issue&lt;/a&gt;