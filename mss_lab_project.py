import numpy as np
import random as rd
from Vehicle_object import Vehicle
from Reservation_object import Reservation
import block
import data
from Gantt import gantt

"""# Car Sharing Environment
* Number of vehicles: 50
* Average utilization of vehicle: 40%
* Time scale: A week
* Details of booking time: avg 240m, minimum 10m
* Number of locations: 10
* Customer's refusal probability = 0.1
"""

#data
locations_list = data.locations_list
travel_time_list = data.travel_time_list
vehicles_quantity = data.vehicles_quantity
booking_quantity = data.booking_quantity
block_num = data.block_num
refuse_probability = data.refuse_probability
new_reservation_probability = data.new_reservation_probability

#Generating Vehicles
vehicles = []
for i in range(vehicles_quantity):
  index = i+1
  dispatchings = []
  initial_location = rd.choice(locations_list)
  curr_location = initial_location
  capacity = np.random.choice([4, 8], p = [0.8, 0.2])
  vehicle = Vehicle(index, dispatchings, initial_location, curr_location, capacity)
  vehicles.append(vehicle)

#Generating Reservations
reservations = []
for i in range(booking_quantity):
  reservation_index = i+1
  start_location = rd.choice(locations_list)
  end_location = rd.choice(locations_list)
  end_time = 100000
  while end_time > block_num:
    travel_time = travel_time_list[start_location[1]][end_location[1]]
    start_time = rd.randrange(0,block_num)
    end_time = start_time + travel_time + round(abs(np.random.normal(4, 2)))
  new_booking = Reservation(start_time, end_time, start_location, end_location, reservation_index)
  new_booking.refuse_with_probability(refuse_probability)
  reservations.append(new_booking)
new_reservation = rd.choice(reservations)
print(new_reservation.start_time, new_reservation.end_time, new_reservation.start_location[0], new_reservation.end_location[0])

#block list which includes reservation's start_time
startime_block = list(list(None for i in range(0, vehicles_quantity)) for i in range(0,block_num)) 
def update_startime_block(Reservation):
  startime_block[Reservation.start_time][Reservation.vehicle - 1] = Reservation




"""Generating Initial Schedule"""
#Dispatching each reservation to available vehicle
def dispatching(vehicles, reservations): 
  for i in range(len(reservations)):
    #print(sorted_reservations[i].index, sorted_reservations[i].start_time)
    this_reservation = reservations[i]
    candidates = []
    for j in range(len(vehicles)):
      overlaps_vehicle_tuple = this_reservation.overlaps_vehicle(vehicles[j])
      if overlaps_vehicle_tuple[0] == False:
        candidates.append([vehicles[j],overlaps_vehicle_tuple[1]] )
    if len(candidates) == 0:             #candidate 0 이면 일단 취소
      continue
    #print(len(candidates))
    selected_vehicle_tuple = rd.choice(candidates)
    selected_vehicle = selected_vehicle_tuple[0]
    this_reservation_order = selected_vehicle_tuple[1]
    if this_reservation_order == -1:
      this_reservation_order = len(selected_vehicle.dispatchings)
    selected_vehicle.dispatchings.insert(this_reservation_order, this_reservation)
    this_reservation.vehicle = selected_vehicle.index
    update_startime_block(this_reservation)
    #print(i, 'th reservation be successfully dispatched')

dispatching(vehicles, reservations)
#check
for i in range(len(vehicles)):
  this_vehicle = vehicles[i]
  print("The car", i, "has been dispatched", end = " ")
  for j in range(len(this_vehicle.dispatchings)):
    this_dispatchings = this_vehicle.dispatchings[j]
    print(this_dispatchings.index, end = " ")
  print()



#Generating Gantt Chart
gantt(vehicles)


'''

""" Dynamic Schedule """

#Real time new reservation
def new_reservation():
  reservation_index = len(reservations) + 1
  start_location = rd.choice(locations_list)
  end_location = rd.choice(locations_list)
  end_time = 100000
  while end_time > block_num:
    travel_time = travel_time_list[start_location[1]][end_location[1]]
    start_time = rd.randrange(0,block_num)
    end_time = start_time + travel_time + round(np.random.normal(4, 2))
  new = Reservation(start_time, end_time, start_location, end_location, reservation_index)
  new.refuse_with_probability(refuse_probability)
  reservations.append(new)
  return new

#Rescheduling test
for i in range(40): new_reservation().rescheduling(vehicles)

#Generating Gantt Chart
#gantt()


#state change
time_step = 1 #10분
for t in range(0, block_num, time_step):
  if t == 100:
    break

  new_reser = block.new_reservation_with_probability(t, new_reservation_probability, reservations)
  #print(new_reser)
  refuse_list = block.refusal(t, startime_block)
  unavail_list = []

  if len(refuse_list) == 0:
    pass
  else:
    #refuse_list에 있는 reservations의 vehicle에서 뒤에 2시간 사이에 예약 있는지 확인. 그 예약도 같이 리스트에 넣어서 rescheduling
    unavail_list = block.unavail_car_reser(t, refuse_list, startime_block)

  if new_reser != None:
    print('new reservation occurs')
    r1 = new_reser.rescheduling(vehicles)
    if r1 == 0: #배차 됐을 때
      update_startime_block(new_reser)


  if len(refuse_list) != 0:
    for i in range(len(refuse_list)):
      print('rejection occurs')
      r2 = refuse_list[i].rescheduling(vehicles)
      if r2 == 0:
        update_startime_block(refuse_list[i])

  if len(unavail_list) != 0:
    for i in range(len(unavail_list)):
      print('unavil_reser occurs')
      r3 = unavail_list[i].rescheduling(vehicles)
      if r3 == 0:
        update_startime_block(unavail_list[i])

  print('block' + str(t) + ' ends')
  print()

  '''
