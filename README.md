# Inventory Management System

A full-stack inventory management system built with Flask and MongoDB.

## Features

- RESTful API backend using Flask
- Frontend interface for inventory management
- User authentication and authorization
- MongoDB database integration
- API testing suite

## Project Structure

```
.
├── app.py              # Main Flask application
├── test_api.py         # API test suite
├── backend/            # Backend logic and routes
├── frontend/          # Frontend assets and templates
├── requirements.txt    # Python dependencies
└── users.json         # User configuration
```
## Screenshots
![Uploading Screenshot 2025-06-08 183644.png…]()


## Prerequisites

- Python 3.x
- MongoDB
- Virtual environment (recommended)

## Dependencies

- Flask 3.0.3 - Web framework
- PyMongo 4.6.3 - MongoDB driver
- python-dotenv 1.0.1 - Environment variable management
- requests 2.31.0 - HTTP library
- beautifulsoup4 4.12.2 - Web scraping library

## Installation

1. Clone the repository:
```bash
git clone https://github.com/Presktok/Inventory_management.git
cd Inventory_management
```

2. Create and activate a virtual environment:
```bash
python -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Set up environment variables:
Create a `.env` file with your configuration:
```
MONGODB_URI=your_mongodb_uri
SECRET_KEY=your_secret_key
```

## Running the Application

1. Start the Flask server:
```bash
python app.py
```

2. Access the application at `http://localhost:5000`

## Testing

Run the test suite:
```bash
python test_api.py
```

## Contributing

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Contact

Your Name - [@Presktok](https://github.com/Presktok)

Project Link: [https://github.com/Presktok/Inventory_management](https://github.com/Presktok/Inventory_management)
