# MinHome

A free and open-source personal productivity dashboard built with Django. MinHome serves as a custom home page application that focuses on speed, simplicity, and minimalism while providing comprehensive personal organization tools.

![Django](https://img.shields.io/badge/Django-4.2.11-092E20?style=flat&logo=django&logoColor=white)
![Python](https://img.shields.io/badge/Python-3.12-3776AB?style=flat&logo=python&logoColor=white)
![PostgreSQL](https://img.shields.io/badge/PostgreSQL-336791?style=flat&logo=postgresql&logoColor=white)
![Bootstrap](https://img.shields.io/badge/Bootstrap-5.0.2-7952B3?style=flat&logo=bootstrap&logoColor=white)

## ✨ Features

### 🔖 **Favorites Management**
- Cloud-based bookmark storage with hierarchical folder organization
- Browser extension for one-click saving (Firefox & Chrome)
- Drag-and-drop interface for easy organization
- Priority favorites displayed on home page

### ✅ **Task Management**
- Simple, flexible task lists with folder organization
- Status tracking (pending/completed)
- Shared folder support with multiple editors
- Home page display of active tasks

### 👥 **Contact Management**
- Comprehensive contact information storage
- Google Contacts integration and synchronization
- Support for multiple phone numbers, addresses, and notes
- Folder-based organization system

### 📝 **Notes System**
- Markdown-supported note-taking
- Folder organization with 3-level nesting
- Subject-based categorization
- Full-text search capabilities

### 📈 **Financial Tracking**
- Real-time cryptocurrency price monitoring
- Securities/stock market data tracking
- Customizable symbol lists per user
- Multiple API integrations (CoinMarketCap, Alpha Vantage, Finnhub)

### 🌤️ **Weather Integration**
- Real-time weather data via OpenWeatherMap API
- ZIP code-based location settings
- Current conditions and forecasts
- Home page weather widget

### 🔍 **Unified Search**
- Multiple search engine options (Google, DuckDuckGo, Wikipedia, Bing)
- Search term preservation across sessions
- Integrated search interface on home page

### ⚙️ **Customization & Settings**
- Multiple theme options (Original, Jay, Matcha)
- User preference management
- Financial symbol customization
- Google account integration

## 🚀 Quick Start

### Prerequisites

- Python 3.12+
- PostgreSQL
- Node.js (for frontend development)

### Installation

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd mh
   ```

2. **Create virtual environment**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Set up environment variables**
   ```bash
   cp .env.example .env
   # Edit .env with your configuration
   ```

5. **Configure your `.env` file**
   ```env
   # Django Settings
   SECRET_KEY=your-secret-key-here
   DEBUG=True
   ENV=dev
   SITE_NAME=MinHome
   ALLOWED_HOSTS=localhost,127.0.0.1

   # Database
   DB_NAME=your-db-name
   DB_USER=your-db-user
   DB_PASSWORD=your-db-password

   # API Keys (optional - get from respective services)
   OPEN_WEATHER_API_KEY=your-openweather-key
   CRYPTO_API_KEY=your-coinmarketcap-key
   ALPHAVANGAGE_STOCKS_API_KEY=your-alphavantage-key
   FINNHUB_API_KEY=your-finnhub-key

   # Email Settings
   EMAIL_HOST_PASSWORD=your-email-password
   EMAIL_HOST=smtp.example.com
   EMAIL_HOST_USER=your-email@example.com
   ```

6. **Set up database**
   ```bash
   python manage.py migrate
   python manage.py createsuperuser
   ```

7. **Run development server**
   ```bash
   python manage.py runserver
   ```

8. **Visit the application**
   Open `http://localhost:8000` in your browser

## 🛠️ Development

### Code Quality

This project uses several tools to maintain code quality:

```bash
# Install pre-commit hooks
pre-commit install

# Run code formatting
black .

# Run import sorting
isort .

# Run linting
flake8

# Run template linting
djlint templates/
```

### Testing

```bash
# Run all tests
pytest

# Run with coverage
pytest --cov
```

### Browser Extension Development

The included browser extension is located in the `extension/` directory:

1. Load unpacked extension in Chrome/Firefox developer mode
2. Point to the `extension/` directory
3. Configure the extension to point to your MinHome instance

## 🏗️ Architecture

### Backend Structure

```
apps/
├── favorites/      # Bookmark management
├── tasks/          # Task/todo management
├── contacts/       # Contact information
├── notes/          # Note-taking system
├── finance/        # Financial data tracking
├── weather/        # Weather integration
├── search/         # Search functionality
├── settings/       # User preferences
├── folders/        # Hierarchical organization
└── management/     # Utility management commands
```

### Key Technologies

- **Backend**: Django 4.2.11, PostgreSQL, django-environ
- **Frontend**: Bootstrap 5, SortableJS, Vanilla JavaScript
- **APIs**: Google APIs, OpenWeatherMap, Financial APIs
- **Development**: pytest, Black, pre-commit hooks
- **Deployment**: Gunicorn, environment-based configuration

## 🔧 Configuration

### API Integrations

To enable full functionality, obtain API keys from:

- **OpenWeatherMap**: Weather data
- **CoinMarketCap**: Cryptocurrency prices
- **Alpha Vantage**: Stock market data
- **Finnhub**: Financial data
- **Google APIs**: Contacts and Calendar integration

### Environment Variables

All sensitive configuration is managed through environment variables. See `.env.example` for required variables.

### Database

The application uses PostgreSQL as the primary database. Update your `.env` file with appropriate database credentials.

## 🚀 Deployment

### Production Settings

For production deployment:

1. Set `DEBUG=False` in your `.env` file
2. Configure proper `ALLOWED_HOSTS`
3. Set up SSL/TLS certificates
4. Configure static file serving
5. Set up proper logging

### Security Considerations

- All API keys are stored in environment variables
- CSRF protection is enabled
- Session security is configured
- Input validation on all forms
- XSS protection in templates

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add some amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

### Development Guidelines

- Follow PEP 8 style guidelines
- Write tests for new functionality
- Update documentation as needed
- Use pre-commit hooks for code quality

## 📝 License

This project is open source and available under the [MIT License](LICENSE).

## 🆘 Support

If you encounter any issues or have questions:

1. Check the existing issues on GitHub
2. Create a new issue with detailed information
3. Provide logs and error messages when applicable

## 🙏 Acknowledgments

- Django community for the excellent framework
- Bootstrap team for the responsive CSS framework
- All API providers for their services
- Contributors who help improve the project

---

**MinHome** - Your personal productivity dashboard, simplified.
