from flask import Flask, Response, request
from CREPE.communication.queue_service import QueueService

# Credits: https://stackoverflow.com/questions/40460846/using-flask-inside-class

class HWAPIWrapper(QueueService):
    app = None  # Do not make more than one WHAPIWrapper please

    def __init__(self,queue_out, queue_in, name="HWAPI"):
        # Initialize queue service
        QueueService.__init__(
            self, 
            name=name, 
            queue_out=queue_out, 
            queue_in=queue_in
        )

        # Initialize flask app
        self.app = Flask(__name__)

        # Add 'routes'/endpoints
        self.add_endpoint(
            endpoint='/', 
            endpoint_name='home', 
            handler=hello_world
        )
        self.add_endpoint(
            endpoint='/hw-api/input/', 
            endpoint_name='input', 
            handler=get_input(self)
        )
        self.add_endpoint(
            endpoint='/hw-api/output/', 
            endpoint_name='output', 
            handler=get_result(self)
        )
        self.add_endpoint(
            endpoint='/hw-api/echo/', 
            endpoint_name='echo', 
            handler=get_echo
        )
        
    def run(self):
        self.app.run()

    def add_endpoint(self, endpoint=None, endpoint_name=None, handler=None):
        self.app.add_url_rule(endpoint, endpoint_name, EndpointAction(handler))


class EndpointAction(object):

    def __init__(self, action):
        self.action = action
        self.default_response = Response(status=200, headers={})

    def __call__(self, *args):
        return self.action(self)


# Test route
# ------------------------------------------------------------------------------
def hello_world(self):
    return "Hello, World!"

# Input from sensor
# ------------------------------------------------------------------------------
# Receive hardware data as a json object. 
# Should be one accumulated unit, such as a full image matrix, array data read
# over a period, etc. 
def get_input(self):
    if request.method == 'GET':
        return 'Send a POST request here to transmit a json'
    elif request.method == 'POST':
        data_json = request.get_json()
        self.put(data_json)
        return 'OK'

# Interpretation output to hardware unit
# ------------------------------------------------------------------------------
# Return the current best guess of the system
# Returns a json 
def get_result(self):
    # Get current interpretation of data (as json)
    # out_json = get_from_readout_current()
    # Return output (as json)
    # return out_json
    return self.get() # TODO: TIMEOUT - if timeout, return last data

# Screen data output
# -----------------------------------------------------------------------------
# Return the input data which was last submitted by the hardware
# Intended for external visualization/monitoring 
# Returns a json
def get_echo(self):
    # Get the last input submitted by the hardware (as json)
    # out_json = get_from_input_current()
    # Return output (as json)
    # return out_json
    return 'Placeholder'

