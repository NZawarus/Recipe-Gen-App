# RecipeIQ Frontend Client

A modern React-based frontend for the RecipeIQ application, which allows users to upload photos of ingredients and generate custom recipes using AI.

## Features

- Upload photos of ingredients/food items
- AI-powered ingredient detection
- Generate customized recipes based on available ingredients
- Modern UI with responsive design

## Project Structure

```
recipe-iq-client/
├── public/                  # Static files
├── src/                     # Source code
│   ├── api/                 # API communication
│   │   ├── models/          # Data models mirroring backend models
│   │   └── routers/         # API clients for backend routes
│   ├── components/          # Reusable React components
│   ├── pages/               # Page components
│   ├── App.js               # Main App component
│   ├── index.js             # Entry point
│   └── index.css            # Global styles
└── package.json             # Dependencies and scripts
```

## Getting Started

### Prerequisites

- Node.js (>= 14.x)
- npm (>= 6.x)

### Installation

1. Clone the repository:

```
git clone <repository-url>
cd recipe-iq-client
```

2. Install dependencies:

```
npm install
```

3. Start the development server:

```
npm start
```

4. Open [http://localhost:3000](http://localhost:3000) to view the app in your browser.

## Backend Connection

The frontend expects the backend API to be running at `http://localhost:8000`. You can change this in `src/api/config.js` if needed.

## Available Scripts

In the project directory, you can run:

- `npm start`: Runs the app in development mode
- `npm test`: Launches the test runner
- `npm run build`: Builds the app for production
- `npm run eject`: Ejects the create-react-app configuration

## Color Theme

The application uses a warm color palette:
- Primary: Red (#f44336)
- Secondary: Orange (#ff9800)
- Accent: Yellow (#ffeb3b) 