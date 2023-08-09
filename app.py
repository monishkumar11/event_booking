from ctypes import addressof
from flask import Flask, render_template, request, redirect, url_for, flash
import json, requests
from datetime import datetime
app = Flask(__name__)
app.secret_key = 'your_secret_key'  # Change this to a secure secret key

# Mocked user data for demonstration
users = {'admin': 'password'}

@app.route('/')
def login():
    return render_template('login.html')

# Define the sample route
@app.route('/dashboard')
def dashboard():
    return render_template('dashboard.html')

# Define the add_events route
@app.route('/add_events', methods=['get'])
def add_events():
    city_list=json.loads(requests.get("https://demo1-800076217.development.catalystserverless.com/server/get_city/city").text)['city']
    
    return render_template('add_event.html',city_list=city_list)


# Define the save_events route
@app.route('/save_events', methods=['post'])
def save_events():
    city_list=json.loads(requests.get("https://demo1-800076217.development.catalystserverless.com/server/get_city/city").text)['city']
    # Get form data
    place=request.form['place']
    event=request.form['event']
    address=request.form['address']
    organizer=request.form['organizer']
    total_seats=request.form['total_seats']
    date = request.form['date']
    from_time = request.form['fromtime']
    to_time = request.form['totime']
    seconds ='00'
    # Create an object with form data
    datetime_str1 = f'{date} {from_time}:{seconds}'
    datetime_str2 = f'{date} {to_time}:{seconds}'
    datetime_obj1 = datetime.strptime(datetime_str1, '%Y-%m-%d %H:%M:%S')
    datetime_obj2 = datetime.strptime(datetime_str2, '%Y-%m-%d %H:%M:%S')
    res=requests.post(url = 'https://demo1-800076217.development.catalystserverless.com/server/file_store_sample/addEvent',headers={"event_name":event,"city":place,'from_time':str(datetime_obj1),'to_time':str(datetime_obj2),"address":address,"total_seats":total_seats,"organiser":organizer})
    print(res.text)
    if res.status_code==200:
        return render_template('admin.html')
    else:
        flash('Invalid entries', 'error')
        #sleep(2.0)
        return render_template('add_event.html',city_list=city_list)
    
# Define the add_details route
@app.route('/add_city')
def add_city():
    return render_template('add_city.html')

@app.route('/add_eve/<string:table_name>')
def add_eve(table_name):
    # You can customize this to display specific details for each table
    return render_template('add_eve.html', table_name=table_name)

# Define the add_details route
@app.route('/add_details')
def add_details():
    return render_template('add_details.html')

# Define the user_detail route
@app.route('/user_details')
def user_details():
    return render_template('user_details.html')

# Define the seats_avaliable route
@app.route('/seats_avaliable')
def seats_avaliable():
    return render_template('seats_avaliable.html')

@app.route('/table_details/<int:table_id>')
def table_details(table_id):
    # You can customize this to display specific details for each table
    table_name = f'Table {table_id}'
    return render_template('table_details.html', table_name=table_name)

# Define the admin_login route
@app.route('/admin_login')
def admin_login():
    return render_template('admin_login.html')

# Define the admin_login_check route
@app.route('/admin_login_check', methods=['post'])
def admin_login_check():
    import requests
    #import json
    #sample details
    user_det = {}
    user_det['user_name'] = request.form['username']
    user_det['password'] = request.form['password']
    #post call
    res = requests.post('https://demo1-800076217.development.catalystserverless.com/server/datastore_test/adminLogin', json=user_det)
    print(res)
    if res.status_code==200:
        return redirect(url_for('admin'))
    else:
        flash('Invalid entries', 'error')
        #sleep(2.0)
        return redirect(url_for('admin_login'))
    
# Define the event_details route
@app.route('/event_detail',methods=['POST'])
def event_detail():
    # Get form data
    date = request.form['date']
    from_time = request.form['fromtime']
    to_time = request.form['totime']
    seconds ='00'
    # Create an object with form data
    datetime_str1 = f'{date} {from_time}:{seconds}'
    datetime_str2 = f'{date} {to_time}:{seconds}'
    datetime_obj1 = datetime.strptime(datetime_str1, '%Y-%m-%d %H:%M:%S')
    datetime_obj2 = datetime.strptime(datetime_str2, '%Y-%m-%d %H:%M:%S')
 

    # Pass the form data to another HTML page
    return redirect(url_for('admin', datetime_obj1=datetime_obj1, datetime_obj2=datetime_obj2))

# Define the admin route
@app.route('/admin')
def admin():
    # Get form data from URL parameters
    date = request.args.get('date')
    from_time = request.args.get('from_time')
    to_time = request.args.get('to_time')
    return render_template('admin.html')
    #return render_template('admin.html', date=date, from_time=from_time, to_time=to_time)
# Define the new_user route
@app.route('/new_user')
def new_user():
    return render_template('new_user.html')

# Define the time_slot route
@app.route('/time_slot')
def time_slot():
    return render_template('time_slot.html')

# Define the new_user_check route
@app.route('/new_user_check', methods=['post'])
def new_user_check():
    import requests
    #import json
    #sample details
    user_det = {}
    user_det['user_name'] = request.form['name']
    user_det['phone_number'] = request.form['phone']
    user_det['email'] = request.form['email']
    user_det['card_number'] = request.form['cardnumber']
    user_det['city']=request.form['city']
    user_det['password'] = request.form['password']
    #post call
    res = requests.post('https://demo1-800076217.development.catalystserverless.com/server/datastore_test/signUp', json=user_det)
    print(res)
    if res.status_code==200:
        return redirect(url_for('login'))
    else:
        #flash('Invalid entries', 'error')
        #sleep(2.0)
        return redirect(url_for('new_user'))
    

# Define the do_login route
@app.route('/login', methods=['POST'])
def do_login():
    username = request.form['username']
    password = request.form['password']
    if username in users and users[username] == password:
        #flash('Login successful!', 'success')
        return redirect(url_for('user_details'))
    else:
        #flash('Invalid username or password', 'error')
        return redirect(url_for('login'))

if __name__ == '__main__':
    app.run(debug=True)
