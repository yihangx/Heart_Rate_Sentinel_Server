import requests
r1 = requests.get("http://127.0.0.1:5000/")
patient_data = {
                "patient_id": 1048596,
                "attending_email":  "xinsg0@gmail.com",
                "age": 24
               }
r = requests.post("http://127.0.0.1:5000/api/new_patient", json=patient_data)
print("'r' = {}".format(r))
print("'r.json() = {}".format(r.json()))
heart_rate = {
                "patient_id": 1048596,
                "heart_rate": 78
               }
r = requests.post("http://127.0.0.1:5000/api/heart_rate", json=heart_rate)
print(r)
r_status = requests.get("http://127.0.0.1:5000/api/status/1048596")
status = r_status.json()
print(status)
r_heart_rate = requests.get("http://127.0.0.1:5000/api/heart_rate/1048596")
data = r_heart_rate.json()
print(data)
r_heart_rate_avg = requests.get(
    "http://127.0.0.1:5000/api/heart_rate/average/1048596")
data = r_heart_rate_avg.json()
print(data)
r_heart_rate_avg_since = requests.post(
    "http://127.0.0.1:5000/api/heart_rate/interval_average", json={
        "patient_id": 1048596,
        "heart_rate_average_since": "2019-04-04 23:00:36.372339"
        })
data = r_heart_rate_avg_since.json()
print(data)
