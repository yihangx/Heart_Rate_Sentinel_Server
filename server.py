from flask import Flask, jsonify, request
from datetime import datetime
from pymodm import connect, MongoModel, fields
import validate_heart_rate as vhr
import average_heart_rate as arg
import sendgrid
import sys
import os
import logging
import json
from logging import getLogger
from sendgrid.helpers.mail import *
connect("mongodb+srv://xinyihang1:19950301@bme547-q262c.mongodb.net/bme547")
app = Flask(__name__)


@app.route("/", methods=["GET"])
def server_on():
    """ Check the server status.
    Args:
        None
    Returns:
        server_on(str):server is on.
    """
    server_on = "Heart Rate Sentinel Server Server is On"
    return server_on


class Patient(MongoModel):
    patient_id = fields.IntegerField(primary_key=True)
    attending_email = fields.EmailField()
    age = fields.IntegerField()
    new_heart_rate = fields.IntegerField()
    new_timestamp = fields.DateTimeField()
    heart_rates = fields.ListField()
    timestamps = fields.ListField()


@app.route("/api/new_patient", methods=["POST"])
def add_new_patient():
    """ Add new patient information.
    Args:
        None
    Returns:
        str(200)
    """
    r = request.get_json()
    p = Patient(r['patient_id'],
                attending_email=r['attending_email'],
                age=r['age'])
    try:
        r1 = json.dumps(r)
        json_object = json.loads(r1)
    except ValueError or TypeError as json_error:
        print(json_error)
    else:
        p.save()
        import logging
        logging.basicConfig(filename="patient_info.log", level=logging.INFO)
        a = 'patient id is {}'.format(p.patient_id)
        logging.info(a)
        return str(200)


@app.route("/api/heart_rate", methods=["POST"])
def add_heart_rate():
    """ Add heart rate information, and if patient is in tachycardia,
    email will be sent to the physician.
    Args:
        None
    Returns:
        str(200)
    """
    r = request.get_json()
    p = Patient.objects.raw({"_id": int(r['patient_id'])}).first()
    try:
        r1 = json.dumps(r)
        json_object = json.loads(r1)
    except ValueError or TypeError as json_error:
        print(json_error)
    else:
        if "tachycardia" is vhr.validate_heart_rate(p.age,
                                                    r['heart_rate']):
            date_string = datetime.now().strftime('%Y-%m-%d %H:%M:%S.%f')
            p.new_heart_rate = r['heart_rate']
            p.heart_rates.append(p.new_heart_rate)
            p.new_timestamp = datetime.now()
            p.timestamps.append(p.new_timestamp)
            p.save()
            sg = sendgrid.SendGridAPIClient(
                apikey=os.environ.get('SENDGRID_API_KEY'))
            from_email = Email("xinsg0@gmail.com")
            to_email = Email(p.attending_email)
            subject = "Patient's is in Tachycardia!"
            content = "Heart rate is abnormal, ({} at date {}), " \
                      "Check patient!".format(p.new_heart_rate, date_string)
            (p.new_heart_rate, date_string)
            content = Content("text/plain", content)
            notif_mail = Mail(from_email, subject, to_email, content)
            response = sg.client.mail.send.post(request_body=notif_mail.get())
            import logging
            logging.basicConfig(filename="patient_info.log",
                                level=logging.INFO)
            b = 'patient id is {}'.format(p.patient_id)
            logging.info(b)
            c = 'The physician email is {}'.format(p.attending_email)
            logging.info(c)
            return str(200)
        elif "tachycardia" is not vhr.validate_heart_rate(p.age,
                                                          r['heart_rate']):
            date_string = datetime.now().strftime('%Y-%m-%d %H:%M:%S.%f')
            p.new_heart_rate = r['heart_rate']
            p.heart_rates.append(p.new_heart_rate)
            p.new_timestamp = datetime.now()
            p.timestamps.append(p.new_timestamp)
            p.save()
            return str(200)
        else:
            raise ValueEbrror("Cannot find patient in database.")


@app.route("/api/status/<patient_id>", methods=["GET"])
def get_status(patient_id):
    """ Get patient's current status.
    Args:
        patient_id(string): unique patient ID
    Returns:
        data(dict):dictionary has patient'status
    """
    p = Patient.objects.raw({"_id": int(patient_id)}).first()
    if p is not None:
        status = vhr.validate_heart_rate(p.age, p.new_heart_rate)
        timestamp_str = p.new_timestamp.strftime('%Y-%m-%d %H:%M:%S.%f')
        data = {
            "status": status,
            "timestamp": timestamp_str
        }
        return jsonify(data)
    else:
        raise ValueError("No heart rate information in the database")


@app.route("/api/heart_rate/<patient_id>", methods=["GET"])
def get_heart_rates(patient_id):
    """ Get patient's heart rate
    Args:
        patient_id(string): unique patient ID
    Returns:
        data(dict):dictionary has patient's heart rate
    """
    p = Patient.objects.raw({"_id": int(patient_id)}).first()
    if p is not None:
        data = {
            "heart_rates": p.heart_rates
        }
        return jsonify(data)
    else:
        raise ValueError("No heart rate information in the database")


@app.route("/api/heart_rate/average/<patient_id>", methods=["GET"])
def get_heart_rate_average(patient_id):
    """ Get patient's average heart rate
    Args:
        patient_id(string): unique patient ID
    Returns:
        data(dict):dictionary has patient's average heart rate
    """
    p = Patient.objects.raw({"_id": int(patient_id)}).first()
    if p is not None:
        heart_rate_avg = arg.average_heart_rate(p.heart_rates)
        data = {"heart_rate_average": heart_rate_avg}
        return jsonify(data)
    else:
        raise ValueError("No heart rate information in the database")


@app.route("/api/heart_rate/interval_average", methods=["POST"])
def post_heart_rate_interval_average():
    """ Get patient's average heart rate in a specific interval
    Args:
        None
    Returns:
        data(dict):dictionary has patient's average heart rate
        in a specific interval
    """
    r = request.get_json()
    p = Patient.objects.raw({"_id": r['patient_id']}).first()
    try:
        r1 = json.dumps(r)
        json_object = json.loads(r1)
    except ValueError or TypeError as json_error:
        print(json_error)
    else:
        try:
            heart_rates = [p.heart_rates[x]
                           for x, y in enumerate(p.timestamps)
                           if y > datetime.strptime
                           (r['heart_rate_average_since'],
                            '%Y-%m-%d %H:%M:%S.%f')]
            data = {
                'heart_rate_interval_average': arg.average_heart_rate
                (heart_rates)
            }
            return jsonify(data)
        except ZeroDivisionError as error:
            print(error)
        return str(500)


if __name__ == '__main__':
    app.run(host='0.0.0.0')
