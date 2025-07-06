# FreelanceCalc - Freelance Business Management Tool

FreelanceCalc is a comprehensive web application designed to help freelancers manage their business operations, track projects, monitor payments, and achieve financial goals.

## Features

### 🎯 Project Management
- Create and manage client projects
- Track project status (In Progress, Completed, On Hold)
- Monitor project timelines and deliverables
- View project history and performance

### 💰 Payment Tracking
- Record and track payments from clients
- Monitor payment status (Pending, Received)
- View payment history and revenue trends
- Generate payment reports

### 🎯 Goal Setting & Tracking
- Set monthly income goals
- Track progress towards financial targets
- Visualize goal achievement with charts
- Monitor year-over-year growth

### 📊 Analytics Dashboard
- Real-time revenue analytics
- Payment pipeline visualization
- Project status overview
- Revenue vs growth tracking
- Interactive charts and insights

### 👤 User Management
- User registration and authentication
- Profile management with photo upload
- Password change functionality
- User initials display for profile pictures

## Technology Stack

- **Backend**: Django 4.x
- **Database**: SQLite (development) / PostgreSQL (production)
- **Frontend**: HTML5, CSS3, JavaScript
- **UI Framework**: Bootstrap 5
- **Charts**: ApexCharts
- **Icons**: Tabler Icons

## Installation

### Prerequisites
- Python 3.8+
- pip

### Setup Instructions

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd freelancecalc-core
   ```

2. **Create a virtual environment**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Run migrations**
   ```bash
   python manage.py makemigrations
   python manage.py migrate
   ```

5. **Create a superuser (optional)**
   ```bash
   python manage.py createsuperuser
   ```

6. **Run the development server**
   ```bash
   python manage.py runserver
   ```

7. **Access the application**
   - Open your browser and go to `http://127.0.0.1:8000`
   - Register a new account or login with existing credentials

## Project Structure

```
freelancecalc-core/
├── freelancecalc_core/     # Django project settings
├── main/                   # Main application
│   ├── models.py          # Database models
│   ├── views.py           # View functions
│   ├── urls.py            # URL routing
│   └── admin.py           # Admin interface
├── templates/             # HTML templates
│   ├── dashboard.html     # Main dashboard
│   ├── profile.html       # User profile page
│   └── components/        # Reusable components
├── static/               # Static files
│   ├── assets/           # CSS, JS, images
│   └── scss/             # SCSS source files
└── manage.py            # Django management script
```

## Key Models

### User
- Custom user model with profile picture support
- Name, email, and authentication fields
- Profile management functionality

### Project
- Client association
- Project status tracking
- Timeline and description fields

### Payment
- Project association
- Payment status (Pending/Received)
- Amount and date tracking

### MonthlyGoal
- Monthly income targets
- Year-based goal tracking
- Progress monitoring

## Features in Detail

### Dashboard Analytics
- **Revenue Overview**: Monthly revenue tracking with percentage changes
- **Payment Pipeline**: Line chart showing revenue trends over 6 months
- **Project Status**: Progress ring showing project distribution
- **Revenue vs Growth**: Comparison chart for business growth analysis

### Profile Management
- Upload profile pictures
- Display user initials when no picture is available
- Update personal information
- Change password securely

### Responsive Design
- Mobile-friendly interface
- Bootstrap-based responsive layout
- Touch-friendly navigation

## Development

### Adding New Features
1. Create models in `main/models.py`
2. Add views in `main/views.py`
3. Create templates in `templates/`
4. Update URL patterns in `main/urls.py`
5. Run migrations for database changes

### Static Files
- CSS files are in `static/assets/css/`
- JavaScript files are in `static/assets/js/`
- Images are in `static/assets/images/`

### Database Migrations
```bash
python manage.py makemigrations
python manage.py migrate
```

## Deployment

### Production Setup
1. Set `DEBUG = False` in settings
2. Configure database (PostgreSQL recommended)
3. Set up static file serving
4. Configure environment variables
5. Set up web server (nginx + gunicorn)

### Environment Variables
- `SECRET_KEY`: Django secret key
- `DATABASE_URL`: Database connection string
- `ALLOWED_HOSTS`: Allowed host domains

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Support

For support and questions, please open an issue in the repository or contact the development team.

---

**FreelanceCalc** - Empowering freelancers with smart business management tools.