from flask import Flask, render_template, request, redirect, session, send_file, make_response
from functions import parse_data, build_pdf, email_registrar, test_email_cookies
from keys import SECRET_KEY
import os

# Sets CWD to whatever directory app.py is located in
os.chdir(os.path.dirname(os.path.abspath(__file__)))

# Initialize flask app, SECRET_KEY can be found in keys.py
app = Flask(__name__, template_folder="templates")
app.secret_key = SECRET_KEY
app.root_path = os.path.dirname(os.path.abspath(__file__))
app.config['TEMPLATES_AUTO_RELOAD'] = True
app.config['EXPLAIN_TEMPLATE_LOADING'] = True

# Homepage route
@app.route('/')
def home():
    if 'channel' in request.cookies:
        print(request.cookies.get('channel'))
        test_email_cookies()
    return render_template('index.html')


# TODO: Catch specific types of errors, inform that pdf was not sent.
@app.route('/form/', methods=['POST', 'GET'])
def process_form():
    """ Form Route: Returns form when requested,
    collects data from user when inputted. The data is sent to
    functions.py, where it is parsed and converted,
    built into the PDF, and emailed to the respective registar. If
    unable to send the PDF, an error page is returned. """
    if request.method == 'POST':
        # try:
        email_registrar(
            build_pdf(
                *parse_data(request)))  # * unpacks tuple returned by parse_data into arguments for build_pdf
        # except(Exception):
        #     return redirect('/error/')
        return redirect('/confirmation/')
    else:
        return render_template('form.html')


# Error Route
@app.route('/error/', methods=['GET'])
def error_page():
    return render_template('formerror.html')

# Credits Route
@app.route('/credits/', methods=['GET'])
def credits_page():
    return render_template('credits.html')


# TODO: Redirect to page based off of succesful submission
@app.route('/confirmation/', methods=['GET'])
def confirmation_page():
    """Confirmation Route: user is redirected here
    after submission of form. """
    return render_template('confirmation.html')
    # if session.get('output_pdf') is not None:
    #     return render_template('confirmation.html')
    # else:
    #     # TODO: redirect to more appropriate error page (like 403 forbidden)
    #     return redirect('/404/')


@app.route('/applications/<id>.pdf')
def render_pdf(id: str):
    """Displays application once submitted to user in PDF form"""
    return send_file(
        open(session['output_file'], 'rb'),
        attachment_filename=session['output_file']
    )


@app.route('/fillableform')
def render_fillableform_pdf():
    """Displays fillable form online. """
    return send_file(
        open('static/blankAppFillable.pdf', 'rb'),
        attachment_filename='blankAppFillable.pdf'
    )


@app.route('/printform')
def render_printform_pdf():
    """Displays printable form online. """
    return send_file(
        open('static/blankApp.pdf', 'rb'),
        attachment_filename='blankApp.pdf'
    )


@app.route('/canvass/<channel>')
def canvass(channel: str):
    response = make_response(redirect('/'))
    response.set_cookie('channel', channel)
    return response


@app.route('/about')
def about():
    return(render_template('about.html'))


@app.errorhandler(404)
def page_not_found(e):
    """Render the 404 page if an incorrect URL is entered. """
    return render_template('404.html'), 404


if __name__ == '__main__':
    app.run()
