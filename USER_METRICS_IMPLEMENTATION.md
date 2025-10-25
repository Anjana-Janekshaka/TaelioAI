# User Metrics Dropdown Implementation

## Overview
This implementation adds a user metrics dropdown to the navbar that displays real-time usage statistics from the database. The dropdown shows key metrics including request counts, token usage, costs, and feature breakdown.

## Features

### 1. UserMetricsDropdown Component
- **Location**: `frontend/src/components/UserMetricsDropdown.tsx`
- **Purpose**: Displays user usage metrics in a dropdown format
- **Data Source**: Backend API endpoints (`/user/me/usage`)

### 2. Key Metrics Displayed
- **Total Requests**: Number of API requests made
- **Total Cost**: Cost in USD for API usage
- **Token Usage**: Input and output tokens consumed
- **Feature Breakdown**: Usage by feature type (idea, story, workflow)
- **Period**: Last 30 days by default

### 3. API Integration
- **Endpoint**: `/user/me/usage?days=30`
- **Authentication**: Uses JWT token from localStorage
- **Error Handling**: Graceful fallback with retry option
- **Loading States**: Skeleton loading animation

## Implementation Details

### Backend API Endpoints
The following endpoints are used:
- `GET /user/me/usage` - User usage summary
- `GET /user/me/profile` - User profile information
- `GET /moderation/metrics` - Content moderation metrics
- `GET /moderation/stats` - Detailed moderation statistics

### Frontend Components
1. **Header.tsx** - Updated to include metrics dropdown button
2. **UserMetricsDropdown.tsx** - New component for metrics display
3. **api.ts** - Updated with new API service methods

### Database Schema
The metrics are pulled from the following database tables:
- `users` - User information and roles
- `usage` - Usage tracking records
- `daily_aggregates` - Aggregated usage data
- `plans` - User subscription plans

## Usage

### For Users
1. Click the "Metrics" button in the navbar
2. View your usage statistics in the dropdown
3. Click "View Full Metrics" to go to the detailed metrics page

### For Developers
1. The dropdown automatically fetches data when opened
2. Data is cached during the session
3. Clicking outside the dropdown closes it
4. Mobile-responsive design included

## Testing
- Test page available at `/test-metrics`
- Backend server should be running on port 8000
- Frontend server should be running on port 3000

## Future Enhancements
- Real-time updates
- Historical data visualization
- Export functionality
- Custom date range selection
- Advanced filtering options
