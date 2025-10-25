# TaelioAI Frontend

A beautiful, modern frontend for the TaelioAI story generation platform built with Next.js, TypeScript, and Tailwind CSS.

## Features

- 🎨 **Beautiful UI**: Modern, responsive design with smooth animations
- 🚀 **Fast Performance**: Built with Next.js 14 and optimized for speed
- 📱 **Mobile First**: Fully responsive design that works on all devices
- 🎯 **Type Safe**: Full TypeScript support for better development experience
- 🎭 **Interactive**: Smooth animations and transitions with Framer Motion
- 🔌 **API Integration**: Seamless connection to the TaelioAI backend

## Getting Started

### Prerequisites

- Node.js 18+ 
- npm or yarn
- Backend API running on http://localhost:8000

### Installation

1. Install dependencies:
```bash
npm install
```

2. Create environment file:
```bash
cp .env.example .env.local
```

3. Update the API URL in `.env.local` if needed:
```
NEXT_PUBLIC_API_URL=http://localhost:8000
```

4. Start the development server:
```bash
npm run dev
```

5. Open [http://localhost:3000](http://localhost:3000) in your browser.

## Available Scripts

- `npm run dev` - Start development server
- `npm run build` - Build for production
- `npm run start` - Start production server
- `npm run lint` - Run ESLint
- `npm run type-check` - Run TypeScript type checking

## Project Structure

```
src/
├── app/                 # Next.js app directory
│   ├── globals.css     # Global styles
│   ├── layout.tsx      # Root layout
│   └── page.tsx        # Home page
├── components/         # React components
│   ├── Header.tsx      # Navigation header
│   ├── Hero.tsx       # Hero section
│   ├── IdeaGenerator.tsx # Idea generation component
│   ├── StoryWriter.tsx # Story writing component
│   ├── WorkflowSelector.tsx # Workflow selection
│   ├── Features.tsx   # Features section
│   └── Footer.tsx     # Footer component
├── hooks/              # Custom React hooks
│   └── useApi.ts      # API integration hooks
└── lib/               # Utility libraries
    └── api.ts         # API client and types
```

## Components

### Core Components

- **Header**: Navigation with mobile menu
- **Hero**: Landing section with call-to-action
- **WorkflowSelector**: Tab-based workflow selection
- **IdeaGenerator**: AI-powered idea generation
- **StoryWriter**: Complete story writing interface
- **Features**: Feature showcase and stats
- **Footer**: Links and company information

### API Integration

The frontend connects to the TaelioAI backend through:

- **Idea Generation**: `/idea/generate-idea`
- **Story Writing**: `/story/write-story`
- **Full Workflow**: `/workflow/generate-full-story`
- **Health Check**: `/health`

## Styling

The project uses Tailwind CSS with custom design system:

- **Colors**: Blue and purple gradient theme
- **Typography**: Inter font family
- **Animations**: Framer Motion for smooth transitions
- **Responsive**: Mobile-first design approach

## Development

### Adding New Features

1. Create component in `src/components/`
2. Add API integration in `src/lib/api.ts`
3. Create custom hooks in `src/hooks/`
4. Update types as needed

### API Integration

Use the provided hooks for API calls:

```typescript
import { useIdeaGeneration } from '@/hooks/useApi';

const { idea, loading, error, generateIdea } = useIdeaGeneration();
```

## Deployment

The frontend can be deployed to:

- **Vercel** (recommended for Next.js)
- **Netlify**
- **AWS Amplify**
- **Any static hosting service**

Build the project:
```bash
npm run build
```

## Contributing

1. Follow the existing code style
2. Use TypeScript for all new code
3. Add proper error handling
4. Test on multiple screen sizes
5. Ensure accessibility standards

## License

This project is part of the TaelioAI platform.