from flask import Flask, render_template, request, redirect, url_for, session
import uuid

app = Flask(__name__)
app.secret_key = 'your-secret-key'

users = {}
booking_details = {}

photographers = [
    {"id": "p1", "name": "Amit Lensman", "skills": ["Wedding", "Corporate"], "image": "amit.jpg"},
    {"id": "p2", "name": "Sana Clickz", "skills": ["Fashion", "Anniversary"], "image": "sana.jpg"},
    {"id": "p3", "name": "Frame by Ananya", "skills": ["Baby Shower", "Corporate"], "image": "ananya.jpg"},
    {"id": "p4", "name": "Priya Pixels", "skills": ["Sports Event", "Graduation"], "image": "priya.jpg"},
    {"id": "p5", "name": "Arjun Clicks", "skills": ["Birthday", "Wedding","Music Concert"], "image": "arjun.jpg"},
    {"id": "p6", "name": "Karthik Captures", "skills": ["anniversary", "Fashion","Baby Shower"], "image": "karthik.jpg"},
    {"id": "p7", "name": "Manas Moments", "skills": ["Product Launch", "Engagement","Birthday"], "image": "manas.jpg"},
    {"id": "p8", "name": "Studio Arav", "skills": ["Music Concert", "product Launch","Anniversary"], "image": "arav.jpg"}
]

availability_data = {
    "p1": ["2025-07-01", "2025-07-07"],
    "p2": ["2025-07-05", "2025-07-11"],
    "p3": ["2025-07-15", "2025-07-23"],
    "p4": ["2025-07-12", "2025-07-17"],
    "p5": ["2025-07-20", "2025-07-25"],
    "p6": ["2025-07-22", "2025-07-29"],
    "p7": ["2025-07-18", "2025-07-23"],
    "p8": ["2025-07-15", "2025-07-22"]
}

ALL_EVENTS = [
    "Wedding", "Birthday", "Fashion", "Corporate", "Graduation",
    "Baby Shower", "Engagement", "Anniversary", "Music Concert",
    "Product Launch", "Sports Event"
]

ALL_EVENT_STYLES = {
    "Wedding": ["Traditional", "Candid", "Pre-Wedding"],
    "Birthday": ["Kids", "Themed", "Outdoor"],
    "Fashion": ["Portfolio", "Editorial", "Runway"],
    "Corporate": ["Headshot", "Team", "Office"],
    "Graduation": ["Ceremony", "Friends", "Family"],
    "Baby Shower": ["Decor", "Indoor", "Family"],
    "Engagement": ["Night", "Ring Ceremony", "Traditional"],
    "Anniversary": ["Romantic", "Candid", "Family"],
    "Music Concert": ["Stage", "Crowd", "Backstage"],
    "Product Launch": ["Booth", "People", "Product Shots"],
    "Sports Event": ["Action", "Candid", "Medals"]
}

@app.route('/')
def home():
    logged_in = 'user_id' in session
    return render_template('home.html', events=ALL_EVENTS, logged_in=logged_in)

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        name = request.form.get('name')
        email = request.form.get('email')

        if not name or not email:
            return "Name and Email are required."

        existing_user_id = next((uid for uid, u in users.items() if u['email'] == email), None)

        if existing_user_id:
            session['user_id'] = existing_user_id
            return render_template('user_info.html', user=users[existing_user_id], existing=True)
        else:
            user_id = str(uuid.uuid4())[:8]
            users[user_id] = {'name': name, 'email': email}
            session['user_id'] = user_id
            return render_template('user_info.html', user=users[user_id], existing=False)

    return render_template('login.html')

@app.route('/my_space')
def my_space():
    user_id = session.get('user_id')
    if not user_id or user_id not in users:
        return redirect(url_for('login'))
    user_info = users[user_id]
    booking = booking_details.get(user_id, {})
    return render_template('my_space.html', user=user_info, booking=booking)

@app.route('/logout')
def logout():
    session.pop('user_id', None)
    return redirect(url_for('home'))

@app.route('/events')
def events():
    return render_template('events.html', events_styles=ALL_EVENT_STYLES)

@app.route('/events/<event_name>')
def event_photographers(event_name):
    styles = ALL_EVENT_STYLES.get(event_name, [])
    filtered_photographers = [
        p for p in photographers if event_name in p['skills']
    ]
    return render_template(
        'event_photographers.html',
        event=event_name,
        styles=styles,
        photographers=filtered_photographers
    )

@app.route('/events/<event_name>/<style_name>')
def style_samples(event_name, style_name):
    prefix = f"{event_name.lower().replace(' ', '')}_{style_name.lower().replace(' ', '')}"
    samples = [f"images/samples/{prefix}{i}.jpg" for i in range(1, 6)]
    return render_template('style_samples.html', event=event_name, style=style_name, samples=samples)

@app.route('/book', methods=['GET', 'POST'])
def book():
    if request.method == 'POST':
        details = {
            'photographer_id': request.form['photographer_id'],
            'user_id': request.form['user_id'],
            'date': request.form['date'],
            'event_type': request.form['event_type'],
            'payment_method': request.form['payment_method']
        }
        booking_details[details['user_id']] = details
        return redirect(url_for('payment', user_id=details['user_id']))
    return render_template('book.html', events=ALL_EVENTS)

@app.route('/show-photographers')
def show_photographers():
    return render_template('photographers.html', photographers=photographers, availability_data=availability_data)

@app.route('/payment')
def payment():
    user_id = request.args.get('user_id')
    booking = booking_details.get(user_id, {})
    return render_template('payment.html', booking=booking)

if __name__ == '__main__':
    app.run(debug=True)
