# KütüpOS

A comprehensive full-stack library management application that demonstrates the progressive implementation of Object-Oriented Programming, External API Integration, and FastAPI web service development. This project evolves from a simple command-line interface to a complete web application with interactive visualization and real-time features.

## Project Architecture

This project implements a three-stage development approach:

- **Stage 1**: Object-oriented terminal application with persistent JSON storage
- **Stage 2**: Enhanced with Open Library API integration for automatic book data retrieval
- **Stage 3**: Full-stack web application with FastAPI backend and React frontend

## Features

### Core Functionality
- **Book Management**: Add, remove, update, and search books with comprehensive metadata
- **ISBN Integration**: Automatic book data retrieval from Open Library API
- **Interactive Library Map**: Multi-floor visualization with genre-based organization
- **Real-time Search**: Instant search with dropdown suggestions and highlighting
- **Statistics Dashboard**: Comprehensive library analytics and author rankings
- **Genre Categorization**: Automatic and manual book categorization system

### Technical Features
- **RESTful API**: Complete FastAPI backend with automatic documentation
- **Modern Frontend**: React application with smooth animations and responsive design
- **Data Persistence**: JSON-based storage with backup functionality
- **Error Handling**: Comprehensive exception management and user feedback
- **Testing Suite**: Extensive pytest coverage for all components
- **Type Safety**: Full type hints and Pydantic models for data validation

## Installation

### Prerequisites

- Python 3.8 or higher
- Node.js 16 or higher
- npm or yarn package manager

### Backend Setup

1. Clone the repository:
```bash
git clone <repository-url>
cd library-management-system
```

2. Create and activate a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install Python dependencies:
```bash
pip install -r requirements.txt
```

4. Initialize the data directory:
```bash
mkdir -p data
```

### Frontend Setup

1. Navigate to the frontend directory:
```bash
cd frontend
```

2. Install Node.js dependencies:
```bash
npm install
```

3. Return to the project root:
```bash
cd ..
```

## Usage

### Stage 1 & 2: Terminal Application

Run the command-line interface:

```bash
python main.py
```

The terminal application provides an interactive menu with the following options:

1. **Add Book (API)**: Enter ISBN to automatically fetch book details
2. **Add Book (Manual)**: Manually enter book information
3. **Delete Book**: Remove books by ISBN
4. **List All Books**: Display all books in the library
5. **Search Book**: Find books by ISBN or keyword search
6. **Library Statistics**: View comprehensive library analytics
7. **Exit**: Save and close the application

### Stage 3: Web Application

#### Starting the Backend Server

```bash
uvicorn api:app --reload
```

The API server will be available at `http://127.0.0.1:8000`

#### Starting the Frontend Application

```bash
cd frontend
npm start
```

The web application will open at `http://localhost:3000`

#### API Documentation

FastAPI automatically generates interactive documentation available at:
- Swagger UI: `http://127.0.0.1:8000/docs`
- ReDoc: `http://127.0.0.1:8000/redoc`

## API Reference

### Authentication
No authentication required for basic operations.

### Base URL
```
http://127.0.0.1:8000
```

### Endpoints

#### Books Management

**GET /books**
- Description: Retrieve all books with optional pagination
- Query Parameters:
  - `limit` (optional): Maximum number of books to return (1-1000)
  - `offset` (optional): Number of books to skip for pagination (default: 0)
- Response: List of books with total count

```bash
curl -X GET "http://127.0.0.1:8000/books?limit=10&offset=0"
```

**POST /books**
- Description: Add a book using ISBN lookup from Open Library API
- Request Body:
```json
{
  "isbn": "978-0262033848"
}
```
- Response: Added book details or error message

```bash
curl -X POST "http://127.0.0.1:8000/books" \
  -H "Content-Type: application/json" \
  -d '{"isbn": "978-0262033848"}'
```

**POST /books/manual**
- Description: Manually add a book with complete information
- Request Body:
```json
{
  "title": "Introduction to Algorithms",
  "author": "Thomas H. Cormen",
  "isbn": "978-0262033848",
  "genre": "Science"
}
```

**GET /books/{isbn}**
- Description: Retrieve a specific book by ISBN
- Path Parameter: `isbn` - The book's ISBN
- Response: Book details or 404 if not found

**PUT /books/{isbn}**
- Description: Update book information
- Request Body:
```json
{
  "genre": "Computer Science",
  "title": "Updated Title"
}
```

**DELETE /books/{isbn}**
- Description: Remove a book from the library
- Path Parameter: `isbn` - The book's ISBN
- Response: Confirmation message with deleted book details

#### Search and Statistics

**GET /search**
- Description: Search books by title, author, or ISBN
- Query Parameters:
  - `q` (required): Search query string
  - `limit` (optional): Maximum results to return (default: 10)

```bash
curl -X GET "http://127.0.0.1:8000/search?q=algorithm&limit=5"
```

**GET /stats**
- Description: Retrieve comprehensive library statistics
- Response: Total books, unique authors, and author rankings

**GET /health**
- Description: Health check endpoint for monitoring
- Response: Service status and basic library statistics

### Response Format

All API responses follow a consistent format:

**Success Response:**
```json
{
  "books": [...],
  "total": 42
}
```

**Error Response:**
```json
{
  "error": "Error message",
  "detail": "Additional error details"
}
```

### HTTP Status Codes

- `200 OK`: Successful retrieval
- `201 Created`: Successful creation
- `400 Bad Request`: Invalid input data
- `404 Not Found`: Resource not found
- `409 Conflict`: Duplicate resource
- `500 Internal Server Error`: Server error
- `502 Bad Gateway`: External API error
- `503 Service Unavailable`: Service temporarily unavailable

## Library Organization

The web interface organizes books across multiple floors:

### Ground Floor
- **Fiction**: General fiction and literary works
- **Mystery**: Detective stories and thrillers
- **Romance**: Romantic fiction and love stories
- **Children**: Children's books and educational material

### Second Floor
- **Science Fiction**: Sci-fi and futuristic literature
- **Fantasy**: Fantasy novels and magical realism
- **Horror**: Horror and suspense stories
- **Adventure**: Adventure and action stories

### Third Floor
- **Science**: Scientific literature and research
- **History**: Historical texts and biographies
- **Philosophy**: Philosophical works and essays
- **Biography**: Autobiographies and biographical works

### Fourth Floor
- **Unassigned**: Books pending categorization (24-book capacity per section)

## Development

### Project Structure

```
library-management-system/
├── src/
│   ├── models/
│   │   ├── __init__.py
│   │   ├── book.py              # Book class definition
│   │   └── api_models.py        # Pydantic models for API
│   ├── services/
│   │   ├── __init__.py
│   │   ├── library.py           # Library management logic
│   │   └── api_service.py       # Open Library API integration
│   └── utils/
│       ├── __init__.py
│       └── exceptions.py        # Custom exception classes
├── frontend/
│   ├── src/
│   │   ├── components/          # React components
│   │   └── services/            # Frontend API client
│   ├── package.json
│   └── public/
├── tests/                       # Test suite
├── data/                        # JSON storage directory
├── api.py                       # FastAPI application
├── main.py                      # Terminal application
├── requirements.txt             # Python dependencies
└── README.md
```

### Running Tests

Execute the test suite:

```bash
pytest
```

Run tests with coverage report:

```bash
pytest --cov=src --cov-report=html
```

### Development Server

For development with auto-reload:

```bash
uvicorn api:app --reload --host 0.0.0.0 --port 8000
```

## Configuration

### Environment Variables

- `PORT`: Backend server port (default: 8000)
- `LIBRARY_FILE`: Path to JSON storage file (default: data/library.json)

### Storage Configuration

Books are stored in `data/library.json` with automatic backup creation. The system creates the data directory automatically if it doesn't exist.

## Error Handling

The application implements comprehensive error handling:

- **Network Errors**: Graceful handling of API connectivity issues
- **Invalid ISBN**: Validation and user feedback for malformed ISBNs
- **Duplicate Books**: Prevention of duplicate entries based on ISBN
- **File Corruption**: Automatic recovery from corrupted storage files
- **Missing Dependencies**: Clear error messages for missing requirements

## Dependencies

### Backend Dependencies
```
fastapi>=0.100.0
uvicorn>=0.22.0
pydantic>=2.0.0
requests>=2.31.0
rich>=13.0.0
colorama>=0.4.6
cachetools>=5.3.0
pytest>=7.0.0
pytest-cov>=4.0.0
```

### Frontend Dependencies
- React 18 with hooks and functional components
- Framer Motion for animations
- React Hot Toast for notifications
- Lucide React for icons

## Performance Considerations

- **Caching**: Open Library API responses are cached to minimize external requests
- **Pagination**: Large book collections are paginated for optimal performance
- **Lazy Loading**: Frontend components use lazy loading for improved responsiveness
- **Memory Management**: Efficient data structures and cleanup procedures

## Known Limitations

- External API dependency for ISBN lookups
- Local JSON storage (not suitable for concurrent users)
- Limited to English language book data from Open Library
- No user authentication or authorization system

## Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Make your changes with appropriate tests
4. Commit your changes (`git commit -m 'Add amazing feature'`)
5. Push to the branch (`git push origin feature/amazing-feature`)
6. Open a Pull Request

## License

This project is created as part of the Global AI Hub Python 202 Bootcamp.