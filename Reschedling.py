import numpy as np
import random as rd
import copy
from Vehicle_object import Vehicle
from Reservation_object import Reservation
#import block
import data
from Gantt import gantt
import initial_schedule
import Reschedling

reservations = initial_schedule.reservations
vehicles = initial_schedule.vehicles
clone_vehicles = initial_schedule.clone_vehicles
startime_block = initial_schedule.startime_block
clone_timeblock = initial_schedule.clone_timeblock
locations_list = data.locations_list
block_num = data.block_num
travel_time_list = data.travel_time_list
refuse_probability = data.refuse_probability
new_reservation_probability = data.new_reservation_probability

print(reservations)
print(vehicles)
print(startime_block)

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

#Calculating total empty travel time of a whole schedule
def total_traveltime(this_vehicles):
  traveltime = 0
  for i in range(len(this_vehicles)):
    this_vehicle = this_vehicles[i]
    sorted_dispatchings = sorted(this_vehicle.dispatchings, key=lambda reservation: reservation.start_time)
    for j in range(len(sorted_dispatchings)):
      this_reservation = sorted_dispatchings[j]
      if j == 0: traveltime += travel_time_list[this_vehicle.initial_location[1]][this_reservation.start_location[1]]
      else:
        prev_reservation = sorted_dispatchings[j-1]
        traveltime += travel_time_list[prev_reservation.end_location[1]][this_reservation.start_location[1]]
  return traveltime

#Rescheduling test
for i in range(100):
  count = 0
  clone_count = 0
  new = new_reservation()
  clone_new = copy.deepcopy(new)

  '''
  print(new.index)
  print(clone_new.index)
  clone_new.index = -5
  print(new.index)
  print(clone_new.index)
  '''
  print('***Information of new reservation***')
  print('Start location: ', new.start_location, 'Start time: ', new.start_time, 'End location: ', new.end_location, 'End time: ', new.end_time)
  #print(new)
  Reschedling.reschedule(new, vehicles, startime_block)

  for j in range(len(vehicles)):
    count += len(vehicles[j].dispatchings)
  #print('Length of vehicles dispatchings: ', count)


  Reschedling.reschedule_random(clone_new, clone_vehicles, clone_timeblock)

  for k in range(len(clone_vehicles)):
    clone_count += len(clone_vehicles[k].dispatchings)
  print('Length of clone_vehicles dispatchings: ', clone_count)


#Generating Gantt Chart
gantt(vehicles)
gantt(clone_vehicles)





'''
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
      startime_block[new_reser.start_time][new_reser.vehicle - 1] = new_reser


  if len(refuse_list) != 0:
    for i in range(len(refuse_list)):
      print('rejection occurs')
      r2 = refuse_list[i].rescheduling(vehicles)
      if r2 == 0:
        startime_block[refuse_list[i].start_time][refuse_list[i].vehicle - 1] = refuse_list[i]

  if len(unavail_list) != 0:
    for i in range(len(unavail_list)):
      print('unavil_reser occurs')
      r3 = unavail_list[i].rescheduling(vehicles)
      if r3 == 0:
        startime_block[unavail_list[i].start_time][unavail_list[i].vehicle - 1] = unavail_list[i]

print('block' + str(t) + ' ends')
print()
print(reservations)
print(vehicles)
print(startime_block)
print(initial_schedule.reservations)
print(initial_schedule.vehicles)
print(initial_schedule.startime_block)
'''
  