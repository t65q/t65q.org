from flask import Flask, render_template
from ics import Calendar
from ics.timeline import Timeline
from urllib.request import urlopen
import arrow

app = Flask(__name__)

@app.route('/', methods=['GET'])
def index():
    # To do: async this?
    

    return render_template('index.html')

@app.route('/events', methods=['GET'])
def events():
    # To do: async this?
    ical_url = "https://www.scoutbook.com/ics/62638.E7F02.ics"
    calendar = Calendar(urlopen(ical_url).read().decode('iso-8859-1'))
    timeline = Timeline(calendar).start_after(arrow.utcnow())
    events = []
    for event in timeline:
        event_data = {
            "name":event.name, 
            "begin_human":event.begin.humanize(),
            "description":event.description.replace('HTTP','http'), 
            "location":event.location, 
            "begin":event.begin.format('dddd, MMM D, YYYY h:mm A'), 
            "end":event.end.format('dddd, MMM D, YYYY h:mm A'),
            "url":event.url
        }
        events.append(event_data)

    return render_template('events.html', context={"events": events})

@app.route('/about', methods=['GET'])
def about():

    return render_template('about.html')

@app.route('/contact', methods=['GET'])
def contact():

    return render_template('contact.html')