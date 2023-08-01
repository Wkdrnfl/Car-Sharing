import numpy as np
import random as rd
from Vehicle_object import Vehicle
from Reservation_object import Reservation
import data
from Gantt import gantt
import copy

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
clone_vehicles = []
for i in range(vehicles_quantity):
  index = i+1
  dispatchings = []
  initial_location = rd.choice(locations_list)
  curr_location = initial_location
  capacity = np.random.choice([4, 8], p = [0.8, 0.2])
  vehicle = Vehicle(index, dispatchings, initial_location, curr_location, capacity)
  vehicles.append(vehicle)
clone_vehicles = copy.deepcopy(vehicles)

#Generating Reservations
reservations = []
clone_reservations = []
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
clone_timeblock = list(list(None for i in range(0, vehicles_quantity)) for i in range(0,block_num+1))

#Dispatching each reservation to available vehicle
def dispatching(vehicles, reservations):
  ##sorted_reservations = sorted(reservations, key=lambda reservation: reservation.start_time)
  for i in range(len(reservations)):
    #print(sorted_reservations[i].index, sorted_reservations[i].start_time)
    this_reservation = reservations[i]
    clone_reservation = copy.deepcopy(this_reservation)
    candidates = []
    for j in range(len(vehicles)):
      overlaps_vehicle_tuple = this_reservation.overlaps_vehicle(vehicles[j], startime_block)
      if overlaps_vehicle_tuple[0] == False:
      #if overlaps_vehicle == False:
        #candidates.append(vehicles[j])
        candidates.append([vehicles[j],overlaps_vehicle_tuple[1]])
    if len(candidates) == 0:                                                                    #candidate 0 이면 일단 취소한다는 건가?
      continue
    #print(len(candidates))

    selected_vehicle_tuple = rd.choice(candidates)
    #selected_vehicle = rd.choice(candidates)
    selected_vehicle = selected_vehicle_tuple[0]
    clone_selected_vehicle = clone_vehicles[selected_vehicle.index - 1]

    this_reservation_order = selected_vehicle_tuple[1]
    if this_reservation_order == -1:
      this_reservation_order = len(selected_vehicle.dispatchings)

    selected_vehicle.dispatchings.insert(this_reservation_order, this_reservation)
    clone_selected_vehicle.dispatchings.insert(this_reservation_order, clone_reservation)

    this_reservation.vehicle = selected_vehicle.index
    clone_reservation.vehicle = selected_vehicle.index

    startime_block[this_reservation.start_time][this_reservation.vehicle - 1] = this_reservation
    clone_timeblock[this_reservation.start_time][this_reservation.vehicle - 1] = clone_reservation
    #print(i, 'th reservation be successfully dispatched')

dispatching(vehicles, reservations)

#Check
#Original vehicles
for i in range(len(vehicles)):
  this_vehicle = vehicles[i]
  print("The car", i, "has been dispatched", end = " ")
  for j in range(len(this_vehicle.dispatchings)):
    this_dispatchings = this_vehicle.dispatchings[j]
    print(this_dispatchings.index, end = " ")
  #print(vehicles[i].dispatchings)

#Clone vehicles (should be identical with the result above)
for i in range(len(clone_vehicles)):
  this_vehicle = clone_vehicles[i]
  print("The car", i, "has been dispatched", end = " ")
  for j in range(len(this_vehicle.dispatchings)):
    this_dispatchings = this_vehicle.dispatchings[j]
    print(this_dispatchings.index, end = " ")
  #print(clone_vehicles[i].dispatchings)

#Generating Gantt Chart
gantt(vehicles)