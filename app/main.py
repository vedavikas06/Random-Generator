from flask import Blueprint, render_template, request, abort
from flask_login import login_required, current_user
# from total_app import limiter
import requests, json
from ratelimiter import rate_limiter, remaining_requests

def error_handler():
    return abort(403,description = "Request Limit Exhausted! Please Try after a minute")


main = Blueprint('main', __name__)

@main.route('/')
def index():
    return render_template('index.html')


@main.route('/call_api')
@login_required
@rate_limiter(limit=5, minutes=1) 
def call_api():
    response = requests.get(url= "http://" + request.host + "/get_number")
    json_data = json.loads(response.text)
    return render_template('random.html', number=json_data["Random_Number"])


@main.route('/see_remaining_limits')
@login_required
def remaining_limits():
    remaining = remaining_requests(limit=5)
    return  render_template('rem_lim.html', number=remaining)