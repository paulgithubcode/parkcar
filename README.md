Develop Using:
Djanggo 1.8
Python 2.7
Mysql 5.7

Please change user and password Mysql at settings.py

1.Park a car
Method = GET
Request variable = plate_number, park_name
Request = http://localhost:8000/park/?plate_number=AB123BM&park_name=ABBuilding
Response = {"message": "Car plate Number AB123BM entered parking area at 2020-10-05 10:00:08.722975+00:00", "code": 200, "data": {"status": "parked", "entry_time": "2020-10-05 10:00:08.722975+00:00", "parking_ticket_id": 43, "exit_time": "None", "maximum_no_cars": 10, "plate_number": "AB123BM", "park_id": 8, "park_name": "ABBuilding", "fee_paid": 0.0}}

2. Unpark a car
Method = GET
Request variable = plate_number
Request = http://localhost:8000/unpark/?plate_number=AB123BM
Response = {"message": "Car plate Number AB123BM exit from parking ABBuilding area at 2020-10-05 10:01:25.310623+00:00", "code": 200, "data": {"status": "exited", "entry_time": "2020-10-05 10:00:08.722975+00:00", "parking_ticket_id": 43, "exit_time": "2020-10-05 10:01:25.310623+00:00", "maximum_no_cars": 10, "plate_number": "AB123BM", "park_id": 8, "park_name": "ABBuilding", "fee_paid": 0.0}}

3. Get Car Information
Method = GET
Request variable = plate_number
Request = http://localhost:8000/get_car_information/?plate_number=AB123BM
Response = {"message": "Car plate Number AB123BM informations", "code": 200, "data": [{"entry_time": "2020-10-05 10:00:08.722975+00:00", "parking_ticket_id": "43", "exit_time": "2020-10-05 10:01:25.310623+00:00", "maximum_no_cars": 10, "plate_number": "AB123BM", "park_id": "8", "park_name": "ABBuilding", "fee_paid": "0.0"}]}

4. Get Slot Information
Method = GET
Request variable = park_name
Request = http://localhost:8000/get_slot_information/?park_name=ABBuilding
Response = {"message": "Park information ABBuilding", "code": 200, "data": {"park_name": "ABBuilding", "available_space_for_cars": 9, "maximum_no_cars": 10, "park_id": 8}}


If all the request above more than 10 times in less than 10 second, it will be get response like this
{"message": "Your Acccess more than 10 request in 10 second", "code": 200, "data": {}}
