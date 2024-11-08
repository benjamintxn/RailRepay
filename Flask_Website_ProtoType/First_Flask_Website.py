from flask import Flask, render_template, request, redirect, url_for
from datetime import datetime

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        # Get the first and last name from the form
        first_name = request.form.get('first_name')
        last_name = request.form.get('last_name')
        selected_option = request.form.get('option')
        
        # Redirect to the new page with the name, first name, and selected option as URL parameters
        return redirect(url_for('show_refund', last_name=last_name, first_name=first_name, selected_option=selected_option))

    return render_template('index.html')


@app.route('/refund', methods=['GET', 'POST'])
def show_refund():
    # Get the URL parameters for full name, first name, and selected option
    last_name = request.args.get('last_name', '')
    first_name = request.args.get('first_name', '')
    selected_option = request.args.get('selected_option', '')

    # Initialize the train_date variable
    train_date = None

    if request.method == 'POST':
        # Get the train date and time from the form
        train_date_str = request.form.get('train_date') + ' ' + request.form.get('train_time')
        
        # Convert the submitted date and time string to a datetime object
        train_date = datetime.strptime(train_date_str, '%Y-%m-%d %H:%M')

        # Get current date and time
        current_date = datetime.now()

        # Check if the train date is in the future
        if train_date > current_date:
            return render_template('refund.html', 
                                   last_name=last_name, 
                                   first_name=first_name, 
                                   selected_option=selected_option, 
                                   error_message="The date and time cannot be in the future.")

    return render_template('refund.html', last_name=last_name, first_name=first_name, selected_option=selected_option, train_date=train_date)


if __name__ == '__main__':
    app.run(debug=True)
