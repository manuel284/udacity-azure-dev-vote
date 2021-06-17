from flask import Flask, request, render_template
import os
import random
import redis
import socket
import sys
import logging
from datetime import datetime

# App Insights
from opencensus.ext.azure.log_exporter import AzureLogHandler
from opencensus.ext.azure import metrics_exporter
from opencensus.stats import aggregation as aggregation_module
from opencensus.stats import measure as measure_module
from opencensus.stats import stats as stats_module
from opencensus.stats import view as view_module
from opencensus.tags import tag_map as tag_map_module
from opencensus.ext.azure.trace_exporter import AzureExporter
from opencensus.trace.samplers import ProbabilitySampler
from opencensus.trace.tracer import Tracer
from opencensus.ext.flask.flask_middleware import FlaskMiddleware
from opencensus.ext.azure.log_exporter import AzureEventHandler


app = Flask(__name__)

# Load configurations from environment or config file
app.config.from_pyfile('config_file.cfg')

# get InstrumentationKey
if ("INSTRUMENTATIONKEY" in os.environ and os.environ['INSTRUMENTATIONKEY']):
    InstrumentationKey = os.environ['INSTRUMENTATIONKEY']
else:
    InstrumentationKey = app.config['INSTRUMENTATIONKEY']

logger = logging.getLogger(__name__)


# enable logging for testing
logger.setLevel(logging.DEBUG)

streamHandler = logging.StreamHandler()
streamEventsHandler = logging.StreamHandler()
streamHandler.setLevel(logging.DEBUG)
logger.addHandler(streamHandler)




logger.addHandler(AzureEventHandler(
    connection_string='InstrumentationKey={}'.format(InstrumentationKey))
)


# Logging
logger.addHandler(AzureLogHandler(
    connection_string='InstrumentationKey={}'.format(InstrumentationKey))
)

# Metrics
exporter = metrics_exporter.new_metrics_exporter(
  enable_standard_metrics=True,
  connection_string='InstrumentationKey={}'.format(InstrumentationKey))

# Tracing
tracer = Tracer(
    exporter=AzureExporter(
        connection_string='InstrumentationKey={}'.format(InstrumentationKey)),
    sampler=ProbabilitySampler(1.0),
)


# Requests
middleware = FlaskMiddleware(
    app,
    exporter=AzureExporter(connection_string='InstrumentationKey={}'.format(InstrumentationKey)),
    sampler=ProbabilitySampler(rate=1.0),
)

if ("VOTE1VALUE" in os.environ and os.environ['VOTE1VALUE']):
    button1 = os.environ['VOTE1VALUE']
else:
    button1 = app.config['VOTE1VALUE']

if ("VOTE2VALUE" in os.environ and os.environ['VOTE2VALUE']):
    button2 = os.environ['VOTE2VALUE']
else:
    button2 = app.config['VOTE2VALUE']

if ("TITLE" in os.environ and os.environ['TITLE']):
    title = os.environ['TITLE']
else:
    title = app.config['TITLE']

# Redis Connection
r = redis.Redis()

# Change title to host name to demo NLB
if app.config['SHOWHOST'] == "true":
    title = socket.gethostname()

# Init Redis
if not r.get(button1): r.set(button1,0)
if not r.get(button2): r.set(button2,0)

@app.route('/', methods=['GET', 'POST'])
def index():

    if request.method == 'GET':

        with tracer.span("votes") as span:

            # Get current values
            vote1 = r.get(button1).decode('utf-8')
            tracer.add_attribute_to_current_span(
                attribute_key = 'cats',
                attribute_value = vote1
            )
            vote2 = r.get(button2).decode('utf-8')
            tracer.add_attribute_to_current_span(
                attribute_key = 'dogs',
                attribute_value = vote2
            )

        # Return index with values
        return render_template("index.html", value1=int(vote1), value2=int(vote2), button1=button1, button2=button2, title=title)

    elif request.method == 'POST':

        if request.form['vote'] == 'reset':

            catVotes = r.get(button1).decode('utf-8')
            dogVotes = r.get(button2).decode('utf-8')
            # Empty table and return results
            r.set(button1,0)
            r.set(button2,0)
            vote1 = r.get(button1).decode('utf-8')
            properties = {'custom_dimensions': {'Cats Vote': catVotes}}
            logger.info('cat votes', extra=properties)

            vote2 = r.get(button2).decode('utf-8')
            properties = {'custom_dimensions': {'Dogs Vote': dogVotes}}
            logger.info('dog votes', extra=properties)

            return render_template("index.html", value1=int(vote1), value2=int(vote2), button1=button1, button2=button2, title=title)

        else:
            # Insert vote result into DB
            vote = request.form['vote']
            r.incr(vote,1)

            # Get current values
            vote1 = r.get(button1).decode('utf-8')
            vote2 = r.get(button2).decode('utf-8')

            # log to trace and custom events
            logger.info(vote)

            # Return results
            return render_template("index.html", value1=int(vote1), value2=int(vote2), button1=button1, button2=button2, title=title)

if __name__ == "__main__":
    # comment line below when deploying to VMSS
    app.run() # local
    # uncomment the line below before deployment to VMSS
    # app.run(host='0.0.0.0', threaded=True, debug=True) # remote
