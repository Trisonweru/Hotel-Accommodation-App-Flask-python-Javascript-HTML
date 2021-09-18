from datetime import time
import re
from flask import render_template, session, redirect, url_for, request, flash, make_response, jsonify
import json
from requests.auth import HTTPBasicAuth
from datetime import datetime
import base64
from wtforms.validators import Email
from Application import app, photos, db, bcrypt
from ..decorators import login_required, admin_required
from .forms import Add_Listing, Book, AdminUser
from Application.models import Listing, Booking,Customer, Admin
import secrets
import time
import requests


@app.route("/", methods=["POST", "GET"])
def home():
    products = Listing.query.order_by(Listing.pub_date.desc()).all()
    return render_template("index.html", title="Home", products=products)

@app.route("/add_listing", methods=["POST", "GET"])
@admin_required
def add_listing():
    form=Add_Listing(request.form)
    if request.method=="POST": #if the request is post, get the fields data and store it into respective varables
        name=form.name.data
        price=form.price.data
        discount=form.discount.data
        desc=form.description.data
        image_1=photos.save(request.files.get('image_1'), name=secrets.token_hex(10)+".")
        image_2=photos.save(request.files.get('image_2'), name=secrets.token_hex(10)+".")
        image_3=photos.save(request.files.get('image_3'), name=secrets.token_hex(10)+".")
        #add the listing data to the addlisting table in the database
        add_listing=Listing(name=name, price=price, discount=discount,description=desc,image_1=image_1, image_2=image_2, image_3=image_3)
        flash(f"The product {name} was added succesfully.", "success")
        db.session.add(add_listing)
        db.session.commit() #commits the changes
        return redirect(url_for("add_listing"))
    return render_template("add_listing.html", form=form, title="Add Listing")

@app.route("/view_bookings", methods=["POST", "GET"])
@login_required
def view_bookings():
    customer = Customer.query.filter_by(username=session['username']).first()
    bookings=Booking.query.filter_by(user_id=customer.id).order_by(Booking.date_in.desc()).all()
    return render_template("view_bookings.html", bookings=bookings, title="View Bookings")

@app.route("/bookings/<int:id>", methods=["POST", "GET"])
@login_required
def bookings(id):
    form=Book(request.form)
    customer = Customer.query.filter_by(username=session['username']).first()
    product=Listing.query.get_or_404(id) #get the product with the id from the the request and pass in the product to the template for display.
    if request.method=="POST":
        days=form.days.data
        date_in=form.date_in.data
        date_out=form.date_out.data
        user_id=customer.id
        listing_id=product.id
        booking=Booking(days=days, date_in=date_in, date_out=date_out, user_id=user_id, listing_id=listing_id)
        db.session.add(booking)
        db.session.commit()
        flash(f"You booked {product.name} for {days} days.", "success")
        return redirect(url_for("payment", booking=booking.id, product=id))
    return render_template("bookings.html", product=product, title=product.name, form=form)

@app.route("/all_bookings", methods=["POST", "GET"])
@admin_required
def all_bookings():
    bookings=Booking.query.order_by(Booking.date_in.desc()).all()
    return render_template("all_bookings.html", bookings=bookings, title="All Bookings")

@app.route("/create_admin", methods=["POST", "GET"])
@admin_required
def create_admin():
    form=AdminUser(request.form)
    if request.method=="POST":
        name=form.name.data
        username=form.username.data
        email=form.email.data
        password=form.password.data
        hashedPass=bcrypt.generate_password_hash(password)
        admin=Admin(name=name, username=username, email=email, password=hashedPass)
        db.session.add(admin)
        db.session.commit()
        flash(f'Admin {username} registered!', 'success')
    return render_template("create_admin.html", title="Create Admin User", form=form)

@app.route("/cancel-booking/<int:id>", methods=["POST", "GET"])
@login_required
def cancel_booking(id):
    booking=Booking.query.get_or_404(id)
    if booking.active:
        booking.active=False
        db.session.commit()
        flash(f'Booking was cancelled succesfully', 'success')
        return redirect(url_for("view_bookings"))
    return redirect(url_for("view_bookings"))

@app.route("/update-booking/<int:id>", methods=["GET", "POST"])
@login_required
def update_booking(id):
    form=Book(request.form)
    booking=Booking.query.get_or_404(id)   
    if request.method=="POST":
        booking.days=form.days.data
        booking.date_in=form.date_in.data
        booking.date_out=form.date_out.data
        db.session.commit()
        flash(f'Booking updated succesfully', 'success')
        return redirect(url_for("view_bookings")) 
    form.days.data=booking.days
    form.date_in.data=booking.date_in
    form.date_out.data=booking.date_out
    return render_template("update.html", form=form, title="Edit Booking")


@app.route("/search-bookings", methods=["POST", "GET"])
@admin_required
def search_bookings():
    bookings=[]
    bookingz=Booking.query.order_by(Booking.date_in.desc(), Booking.time_in.desc()).all()
    val=request.form.get('search')
    if request.method=="POST":
        for item in bookingz:
            if val.lower() in item.user.name.lower() or val in item.user.phone:
                bookings.append(item)
            else:
                pass
        if len(bookings) < 1:
            flash(f'Could not match any document. Try again!', 'success')
            return redirect(url_for("all_bookings"))
        return render_template("all_bookings.html", titte="", bookings=bookings)        
    return render_template("all_bookings.html", titte="", bookings=bookingz)



    

#*********************************TO DO PAYMENT WITH STRIPE AND MPESA********************************************
# Implement MPESA STK push
phone=[]
@app.route('/mpesa-pay', methods=['POST', 'GET'])
@login_required
def mpesa_pay():
    no=request.args['phone']     
    phone.append(no)  
    return no

@app.route("/prego-mpesa-callback", methods=["POST"])
def mpesa_callback():
    json_data = request.get_json()
    result_code=json_data["Body"]["stkCallback"]["ResultCode"]
    print(request.data)
    #save data if resultcode==0
    return result_code


consumer_key="SDiFgM3qp30XkZ4AmGGqp5M5zoC8Uod2"
consumer_secret="Ix3fVKI1Pa9HoIf9"
api_URL = "https://sandbox.safaricom.co.ke/oauth/v1/generate?grant_type=client_credentials"

booking=None
product=None
@app.route("/payment", methods=["POST", "GET"])
@login_required
def payment():
    global booking
    global product
    if not request.args:
        return redirect(url_for('home'))
    if request.args.get('booking'):
        booking_id=int(request.args.get('booking'))
        booking=Booking.query.get_or_404(booking_id)
    if request.args.get('product'):
        product_id=int(request.args.get('product'))
        product=Listing.query.get_or_404(product_id)
    if len(phone)>0:
       try:
           r = requests.get(api_URL, auth=HTTPBasicAuth(consumer_key, consumer_secret))
           access_token = r.json()['access_token']
           phoneNo=int(phone[-1])
           api_url = "https://sandbox.safaricom.co.ke/mpesa/stkpush/v1/processrequest"
           callback="https://a3edbca535e9.ngrok.io/prego-mpesa-callback"
           headers = {"Authorization": "Bearer %s" % access_token}
           timestamp=datetime.now().strftime('%Y%m%d%H%M%S')
           business_short_code=174379
           pass_key="bfb279f9aa9bdbcf158e97dd71a467cd2e0c893059b10f78e6b72ada1ed2c919"
           data_to_encode = str(business_short_code) + pass_key + timestamp
           online_password = base64.b64encode(data_to_encode.encode())
           price=int(product.price)*int(booking.days)
           req = {
            "BusinessShortCode":business_short_code,
            "Password":online_password.decode('utf-8'),
            "Timestamp": timestamp,
            "TransactionType": "CustomerPayBillOnline",
            "Amount": 1,
            "PartyA": phoneNo,  
            "PartyB":174379,
            "PhoneNumber": phoneNo, 
            "CallBackURL": callback, #"https://sandbox.safaricom.co.ke/mpesa/",
            "AccountReference": "Isaac",
            "TransactionDesc": "Testing stk push"
            }
           response = requests.post(api_url, json=req, headers=headers)
           if response.json()['ResponseCode']=="0":
               booking.paid=True
               booking.payment_no=str(phoneNo)
               booking.amount_paid=str(price)
               db.session.commit()
            
           phone.clear()
           flash(f'Check your phone to finish your transaction', 'success')
           return render_template('thankyou.html', response="Thank you for choosing us. Check your phone to finish the transaction.")
       except Exception as  err:
            return render_template('thankyou.html', response="Transaction was unsuccessful, check your Mpesa number and try again!")
    return render_template("payment.html", title="Payment", booking=booking, product=product) 

# Implementing Jenga Payment Gateway
@app.route('/card-pay', methods=["POST", "GET"])
def card_pay():
    url = "https://api-test.equitybankgroup.com/v1/token"
    payload = "grant_type=password&merchantCode=9803515731&password=vWnK1mEkInyJbLfwWaYCbzeTdQMbD2iKX"
    headers = {
    "Authorization": "Basic akhac0NzOTBNRjVwTnA2MmJVaFJXUUFBSjczU0dLR2c6YUhZUkdMVDlvVVZoaVludg==",
    "Content-Type": "application/x-www-form-urlencoded"
    }
    response = requests.request("POST", url, data=payload, headers=headers)
    token=response.json()['payment-token']

    #payment gateway
    payload2={
        'token': token,
        'amount': '1000',
        'orderReference': '4yTr67',
        'merchantCode': '9803515731',
        'merchant': 'KIW Softwares',
        'currency': 'KSH',
        'custName': 'KIW Softwares',
        'outletCode': '0000000000',
        'extraData': 'Test',
        'ez1_callbackurl': 'http://requestbin.com',
        'expiry': '2025-02-17T19:00:00'}
    uri="https://api-test.equitybankgroup.com/v2/checkout/launch"
    resp = requests.request("POST", uri, data=payload2)
    return resp.text

#*********************************END OF PAYMENT********************************************

#*********************************LAZY LOADING IMPLEMENTATION********************************************
quantity=3
products = Listing.query.order_by(Listing.pub_date.desc()).all()
items = [] 
quantity2=1
j=0
@app.route("/load", methods=["POST", "GET"])
def load():
    time.sleep(0.2)   
    if request.args.get('v'):
        counter2=int(request.args.get('c2'))
        items.clear()
        print(request.args.get('v'))
        for item in products:
            if request.args.get('v').lower() in item.name.lower():
                items.append(item.toDict())
                pass
            else:
                pass  
        print(items)      
        if counter2==0:
            print(f"Returning items 0 to {quantity2}")
            res=make_response(jsonify(items[0:quantity2]), len(items))
        elif counter2==len(items):
            print("No more items")
            res=make_response(jsonify({}), len(items))
        else:
            print(f"Returning items {counter2} to {counter2 + quantity2}")
            res= make_response(jsonify(items[counter2 : counter2+quantity2]), len(items))
    else:
        if request.args:
            for item in products:
                if len(items) < len(products):
                    items.append(item.toDict())
                else:
                    pass                  
            counter=int(request.args.get('c'))
            if counter==0:
                print(f"Returning items 0 to {quantity}")
                res=make_response(jsonify(items[0:quantity]), len(items))
            elif counter==len(items):
                print("No more items")
                res=make_response(jsonify({}), len(items))
            else:
                print(f"Returning items {counter} to {counter + quantity}")
                res= make_response(jsonify(items[counter : counter+quantity]), len(items))
    return res
#*********************************END OF LAZY LOADING IMPLEMENTATION********************************************

#*********************************HOME SEARCH IMPLEMENTATION********************************************