# BookNest

A full-stack library management system with a React frontend and FastAPI backend. Features automatic book data retrieval, multi-floor library visualization, and real-time search capabilities.

## Quick Start

### Prerequisites

- Python 3.8+
- Node.js 16+
- npm or yarn

### Backend Setup

```bash
# Install Python dependencies
pip install -r requirements.txt

# Start the API server
uvicorn api:app --reload
```

The API will be available at `http://127.0.0.1:8000`

### Frontend Setup

```bash
# Navigate to frontend directory
cd frontend

# Install dependencies
npm install

# Start development server
npm start
```

The application will open at `http://localhost:3000`

## Features

### Core Functionality
- Add books via ISBN lookup using Open Library API
- Manual book entry with genre categorization
- Interactive multi-floor library visualization
- Real-time search with dropdown suggestions
- Book genre editing and shelf reorganization
- Library statistics dashboard

### Library Organization
- **Ground Floor**: Fiction, Mystery, Romance, Children's books
- **Second Floor**: Science Fiction, Fantasy, Horror, Adventure
- **Third Floor**: Science, History, Philosophy, Biography
- **Fourth Floor**: Unassigned books (24-book capacity per section)

## API Reference

### Books
- `GET /books` - List all books with pagination support
- `POST /books` - Add book by ISBN (auto-fetch from Open Library)
- `POST /books/manual` - Add book with manual entry
- `GET /books/{isbn}` - Get specific book details
- `PUT /books/{isbn}` - Update book information
- `DELETE /books/{isbn}` - Remove book from library

### Search & Statistics
- `GET /search?q={query}` - Search books by title, author, or ISBN
- `GET /stats` - Get library statistics
- `GET /health` - Health check endpoint

## Technical Architecture

### Backend
- **FastAPI** with automatic OpenAPI documentation
- **Pydantic** for data validation and serialization
- **Requests** for external API integration
- **JSON file storage** with automatic backups
- **Comprehensive error handling** and logging

### Frontend
- **React 18** with hooks and functional components
- **Framer Motion** for smooth animations
- **React Hot Toast** for user notifications
- **Lucide React** for consistent iconography
- **CSS custom properties** for theming

### Data Flow
1. Books added via ISBN are automatically categorized as "Unassigned"
2. Manual entries can be directly assigned to specific genres
3. Genre changes move books between floors in real-time
4. Search operates on local data for instant results

## Development

### Project Structure
```
├── api.py                 # FastAPI application
├── src/
│   ├── models/           # Data models and API schemas
│   ├── services/         # Business logic and external APIs
│   └── utils/            # Utilities and exceptions
├── frontend/
│   ├── src/
│   │   ├── components/   # React components
│   │   └── services/     # Frontend API client
│   ├── package.json
│   └── public/
└── data/                 # JSON storage directory
```

### Running Tests
```bash
# Backend tests
pytest

# Frontend tests
npm test
```

### API Documentation
Visit `http://127.0.0.1:8000/docs` when the backend is running for interactive API documentation.

## Configuration

### Environment Variables
- `PORT` - Backend port (default: 8000)
- `LIBRARY_FILE` - Path to JSON storage file (default: data/library.json)

### Customization
- Modify `GENRE_OPTIONS` in `AddBookModal.js` to add new categories
- Update floor configurations in `LibraryMap.js` for different layouts
- Adjust book colors in `genreService.js` for visual customization

## Production Deployment

### Backend
```bash
pip install gunicorn
gunicorn api:app -w 4 -k uvicorn.workers.UvicornWorker
```

### Frontend
```bash
npm run build
# Serve build directory with your preferred web server
```

## Known Limitations

- External API dependency for ISBN lookups
- Local JSON storage (not suitable for concurrent users)
- No user authentication or authorization
- Limited to English language book data

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes with appropriate tests
4. Submit a pull request

## License

MIT License - see LICENSE file for details.