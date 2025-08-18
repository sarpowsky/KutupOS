// src/services/genreService.js

const GENRE_KEYWORDS = {
  'Fiction': ['novel', 'story', 'tale', 'narrative', 'fiction'],
  'Mystery': ['mystery', 'detective', 'crime', 'murder', 'investigation', 'clue', 'suspect', 'thriller'],
  'Romance': ['romance', 'love', 'heart', 'passion', 'relationship', 'wedding', 'bride', 'dating'],
  'Children': ['children', 'kids', 'young', 'tale', 'story', 'adventure', 'learning'],
  'Science Fiction': ['science', 'fiction', 'sci-fi', 'space', 'future', 'robot', 'alien', 'cyberpunk', 'dystopian'],
  'Fantasy': ['fantasy', 'magic', 'wizard', 'dragon', 'quest', 'realm', 'kingdom', 'sword', 'epic'],
  'Horror': ['horror', 'scary', 'fear', 'ghost', 'vampire', 'zombie', 'terror'],
  'Adventure': ['adventure', 'journey', 'quest', 'exploration', 'travel', 'expedition'],
  'Science': ['science', 'physics', 'chemistry', 'biology', 'mathematics', 'research', 'theory'],
  'History': ['history', 'historical', 'war', 'ancient', 'civilization', 'empire', 'revolution'],
  'Philosophy': ['philosophy', 'wisdom', 'ethics', 'truth', 'existence', 'consciousness', 'meaning'],
  'Biography': ['biography', 'memoir', 'life', 'autobiography', 'story of', 'journey of']
};

const BOOK_COLORS = [
  '#8B4513', '#2E8B57', '#4682B4', '#CD853F', '#A0522D',
  '#6B8E23', '#B8860B', '#20B2AA', '#9932CC', '#FF6347',
  '#4169E1', '#32CD32', '#FFD700', '#FF69B4', '#00CED1',
  '#DC143C', '#00FF7F', '#1E90FF', '#FF1493', '#7FFF00',
  '#D2691E', '#48D1CC', '#C71585', '#191970', '#228B22'
];

export const detectGenre = (book) => {
  const { title, author } = book;
  
  const searchText = `${title} ${author}`.toLowerCase();
  
  let bestMatch = 'Unassigned';
  let maxScore = 0;
  
  for (const [genre, keywords] of Object.entries(GENRE_KEYWORDS)) {
    const score = keywords.reduce((acc, keyword) => {
      return acc + (searchText.includes(keyword) ? 1 : 0);
    }, 0);
    
    if (score > maxScore) {
      maxScore = score;
      bestMatch = genre;
    }
  }
  
  return bestMatch;
};

export const getRandomBookColor = (isbn) => {
  // Use ISBN as seed for consistent color per book
  const hash = isbn.split('').reduce((a, b) => {
    a = ((a << 5) - a) + b.charCodeAt(0);
    return a & a;
  }, 0);
  return BOOK_COLORS[Math.abs(hash) % BOOK_COLORS.length];
};

export const getTextColor = (backgroundColor) => {
  // Calculate luminance to determine if text should be light or dark
  const hex = backgroundColor.replace('#', '');
  const r = parseInt(hex.substr(0, 2), 16);
  const g = parseInt(hex.substr(2, 2), 16);
  const b = parseInt(hex.substr(4, 2), 16);
  const luminance = (0.299 * r + 0.587 * g + 0.114 * b) / 255;
  return luminance > 0.5 ? '#2C1810' : '#F5F1EA';
};

export const getGenreColor = (genre) => {
  const colors = {
    'Fiction': '#424242', 'Mystery': '#E65100', 'Romance': '#C2185B',
    'Children': '#FBC02D', 'Science Fiction': '#1565C0', 'Fantasy': '#7B1FA2',
    'Horror': '#B71C1C', 'Adventure': '#0097A7', 'Science': '#1976D2',
    'History': '#5D4037', 'Philosophy': '#512DA8', 'Biography': '#2E7D32',
    'Unassigned': '#607D8B'
  };
  return colors[genre] || colors['Unassigned'];
};