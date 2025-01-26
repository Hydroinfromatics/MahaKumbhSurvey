from flask import Flask, render_template, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import pytz
import logging

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///kumbh_mela_survey.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)
# Define Indian Standard Time
IST = pytz.timezone('Asia/Kolkata')

# Logging configuration
logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(message)s')

# Database model
class Survey(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    timestamp = db.Column(db.String(50), nullable=False, default=lambda: datetime.now(IST).strftime('%d-%m-%Y %H:%M'))
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), nullable=False)
    phone = db.Column(db.String(20), nullable=False)
    travel_origin = db.Column(db.String(50), nullable=False)
    water_facility_location = db.Column(db.String(50), nullable=False)
    facility_frequency = db.Column(db.String(50), nullable=False)
    facility_type = db.Column(db.String(50), nullable=False)
    facility_functionality = db.Column(db.String(50), nullable=False)
    water_sufficiency = db.Column(db.String(50), nullable=False)
    waiting_time = db.Column(db.String(50), nullable=False)
    water_quality = db.Column(db.String(50), nullable=False)
    water_characteristics = db.Column(db.String(50), nullable=False)
    health_issues = db.Column(db.String(200), nullable=False)
    sanitation_availability = db.Column(db.String(50), nullable=False)
    sanitation_cleanliness = db.Column(db.String(50), nullable=False)
    sanitation_accessibility = db.Column(db.String(50), nullable=False)
    dipping_visit = db.Column(db.String(200), nullable=False)
    dipping_cleanliness = db.Column(db.String(50), nullable=False)
    water_contamination = db.Column(db.String(50), nullable=False)
    dipping_health_issues = db.Column(db.String(200), nullable=False)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/submit', methods=['POST'])
def submit():
    try:
        data = request.form
        logging.debug(f"Received form data: {data}")

        # Create a new Survey instance
        survey = Survey(
            name=data['name'],
            email=data['email'],
            phone=data['phone'],
            travel_origin=data['travel_origin'],
            water_facility_location=data['water_facility_location'],
            facility_frequency=data['facility_frequency'],
            facility_type=data['facility_type'],
            facility_functionality=data['facility_functionality'],
            water_sufficiency=data['water_sufficiency'],
            waiting_time=data['waiting_time'],
            water_quality=data['water_quality'],
            water_characteristics=data['water_characteristics'],
            health_issues=data['health_issues'],
            sanitation_availability=data['sanitation_availability'],
            sanitation_cleanliness=data['sanitation_cleanliness'],
            sanitation_accessibility=data['sanitation_accessibility'],
            dipping_visit=data['dipping_visit'],
            dipping_cleanliness=data['dipping_cleanliness'],
            water_contamination=data['water_contamination'],
            dipping_health_issues=data['dipping_health_issues']
        )

        # Add to database
        db.session.add(survey)
        db.session.commit()
        logging.info("Survey submitted successfully.")
        return jsonify({'success': True, 'message': 'Survey submitted successfully!'})

    except Exception as e:
        logging.error(f"Error during form submission: {e}")
        return jsonify({'success': False, 'message': str(e)}), 400
        
@app.route('/analytics', methods=['GET'])
def analytics():
    try:
        # Fetch all survey data
        surveys = Survey.query.all()

        # Initialize data structure for all questions
        data = {
            'travel_origin': {'title': 'Travel Origin', 'type': 'pie', 'labels': [], 'values': [], 'colors': ['#1e88e5', '#64b5f6', '#bbdefb', '#1976d2']},
            'water_facility_location': {'title': 'Ease of Locating Water Facilities', 'type': 'bar', 'labels': [], 'values': [], 'colors': ['#ff7043', '#ffa726', '#ffcc80', '#d84315']},
            'facility_frequency': {'title': 'Frequency of Water Facilities', 'type': 'doughnut', 'labels': [], 'values': [], 'colors': ['#66bb6a', '#a5d6a7', '#388e3c', '#2e7d32']},
            'facility_type': {'title': 'Type of Water Facility', 'type': 'bar', 'labels': [], 'values': [], 'colors': ['#ab47bc', '#ce93d8', '#8e24aa', '#6a1b9a']},
            'facility_functionality': {'title': 'Functionality of Water Facilities', 'type': 'pie', 'labels': [], 'values': [], 'colors': ['#29b6f6', '#4fc3f7', '#0288d1', '#01579b']},
            'water_sufficiency': {'title': 'Water Sufficiency', 'type': 'polarArea', 'labels': [], 'values': [], 'colors': ['#42a5f5', '#90caf9', '#1e88e5', '#1565c0']},
            'waiting_time': {'title': 'Waiting Time for Water', 'type': 'doughnut', 'labels': [], 'values': [], 'colors': ['#ffa726', '#ffb74d', '#f57c00', '#e65100']},
            'water_quality': {'title': 'Water Quality Ratings', 'type': 'polarArea', 'labels': [], 'values': [], 'colors': ['#ef5350', '#e57373', '#c62828', '#b71c1c']},
            'water_characteristics': {'title': 'Water Characteristics', 'type': 'bar', 'labels': [], 'values': [], 'colors': ['#7e57c2', '#b39ddb', '#512da8', '#311b92']},
            'health_issues': {'title': 'Health Issues After Water Usage', 'type': 'bar', 'labels': [], 'values': [], 'colors': ['#29b6f6', '#4fc3f7', '#0288d1', '#01579b']},
            'sanitation_availability': {'title': 'Sanitation Availability', 'type': 'pie', 'labels': [], 'values': [], 'colors': ['#66bb6a', '#a5d6a7', '#388e3c', '#2e7d32']},
            'sanitation_cleanliness': {'title': 'Sanitation Cleanliness', 'type': 'bar', 'labels': [], 'values': [], 'colors': ['#ff7043', '#ffa726', '#ffcc80', '#d84315']},
            'sanitation_accessibility': {'title': 'Sanitation Accessibility', 'type': 'doughnut', 'labels': [], 'values': [], 'colors': ['#ef5350', '#e57373', '#c62828', '#b71c1c']},
            'dipping_visit': {'title': 'Visits to Dipping Places', 'type': 'polarArea', 'labels': [], 'values': [], 'colors': ['#ab47bc', '#ce93d8', '#8e24aa', '#6a1b9a']},
            'dipping_cleanliness': {'title': 'Cleanliness at Dipping Places', 'type': 'doughnut', 'labels': [], 'values': [], 'colors': ['#42a5f5', '#90caf9', '#1e88e5', '#1565c0']},
            'water_contamination': {'title': 'Water Contamination', 'type': 'polarArea', 'labels': [], 'values': [], 'colors': ['#29b6f6', '#4fc3f7', '#0288d1', '#01579b']},
            'dipping_health_issues': {'title': 'Health Issues After Dipping', 'type': 'bar', 'labels': [], 'values': [], 'colors': ['#7e57c2', '#b39ddb', '#512da8', '#311b92']}
        }

        # Aggregate counts for each field
        for survey in surveys:
            for key in data.keys():
                value = getattr(survey, key)
                if value not in data[key]['labels']:
                    data[key]['labels'].append(value)
                    data[key]['values'].append(1)
                else:
                    index = data[key]['labels'].index(value)
                    data[key]['values'][index] += 1

        return render_template('analytics.html', data=data)
    except Exception as e:
        logging.error(f"Error loading analytics: {e}")
        return "An error occurred while loading analytics.", 500

@app.route('/responses', methods=['GET'])
def responses():
    try:
        # Fetch data from the database
        surveys = Survey.query.with_entities(
            Survey.name, Survey.phone, Survey.timestamp
        ).all()

        # Pass data to the template
        return render_template('responses.html', surveys=surveys)
    except Exception as e:
        logging.error(f"Error fetching responses: {e}")
        return "An error occurred while fetching responses.", 500

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)
