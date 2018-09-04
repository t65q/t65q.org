from flask import Flask, render_template, request
from ics import Calendar
from ics.timeline import Timeline
from urllib.request import urlopen
from jinja2 import Environment
import arrow
import feedparser
import jinja2

app = Flask(__name__)

# to do: let's make this available to the template so it's not defined twice
RSS_FEEDS = {
    'scoutmaster': {
        'href': 'https://blog.t65q.org/feeds/posts/default/-/Scoutmaster%27s%20Minute?alt=rss',
        'long_title': "Scoutmaster's Minutes"
    },
    'troop': {
        'href': 'https://blog.t65q.org/feeds/posts/default/-/Troop%20Updates?alt=rss',
        'long_title': 'Troop Updates'
    },
    'buffaloes': {
        'href': 'https://blog.t65q.org/feeds/posts/default/-/Charging%20Buffaloes?alt=rss',
        'long_title': 'Charging Buffaloes'
    },
    'knights': {
        'href': 'https://blog.t65q.org/feeds/posts/default/-/Nuclear%20Knights?alt=rss',
        'long_title': 'Nuclear Knights'
    }
}

env = Environment()

@app.route('/', methods=['GET'])
def index():
    # To do: async this?
    

    return render_template('about.html')

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

@app.route('/news')
def news():
    publication = request.args['publication']
    return get_news(publication)

def get_news(publication):
    try:
        feed = feedparser.parse(RSS_FEEDS[publication]['href'])
        long_title = RSS_FEEDS[publication]['long_title']
    except KeyError:
        feed = feedparser.parse(RSS_FEEDS['troop']['href'])
        long_title = RSS_FEEDS['troop']['long_title']
    
    return render_template('pub.html', articles=feed['entries'], publication=publication, long_title=long_title)