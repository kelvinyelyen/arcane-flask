# Arcane

## Introduction

Arcane serves as a web-based solution as part of my Harvard's CS50x final project, designed with a minimalist approach to tackle the complexities of newsletter management. It provides an intuitive remedy for subscriber handling, enabling the creation of engaging newsletters using a comprehensive text editor, and ensuring the distribution of personalized content. Through seamless integration with an email service, it optimizes communication efficiency and fosters increased engagement among subscribers.


## Getting Started

### Installation

Clone the repository:

```bash
git clone https://github.com/your-username/arcane.git
cd arcane
```

Create a virtual environment (optional but recommended):

```bash
python3 -m venv arcane_venv
source arcane_venv/bin/activate
```

Install the required packages:

```bash
pip install -r requirements.txt
```

## Usage

### Running the App

Configure your MongoDB URI in `.env`:

```python
DB_URI=your_mongodb_uri_here
```

Run the Flask app:

```bash
python app.py
```

Access the app in your browser at `http://localhost:5000`.

## Configuration

MongoDB URI: Update the `.env` file with your MongoDB URI.


## Built Using

- [**Flask**](https://flask.palletsprojects.com/en/2.3.x/) - Framework for backend development
- [**Bootstrap**](https://getbootstrap.com/) - Facilitating responsive design implementation
- [**SQLAlchemy**](https://www.sqlalchemy.org/) - Utilized as the development database engine
- [**MongoDB**](https://www.mongodb.com/) - Chosen as the production database solution
- [**Mailgun**](https://www.mailgun.com/) - Service provider for handling emails
- [**Resend**](https://resend.com/) - Additional email service integration for enhanced functionality\

  
## Found an issue or have a suggestion?

&lt;a href="https://github.com/kelvinyelyen/arcane/issues/new" target="\_blank"&gt;Create an issue&lt;/a&gt;
