import React from 'react';
import { createRoot } from 'react-dom/client';
import App from './App';

// Create React 18 root and render App
const container = document.getElementById('root');
if (!container) {
	console.error('Root element not found');
} else {
	const root = createRoot(container);
	root.render(
		<React.StrictMode>
			<App />
		</React.StrictMode>
	);
}

