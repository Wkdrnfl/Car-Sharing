import numpy as np
import random as rd
import plotly.express as px
import pandas as pd

"""# Car Sharing Environment
* Number of vehicles: 50
* Average utilization of vehicle: 40%
* Time scale: A week
* Details of booking time: avg 240m, minimum 10m
* Number of locations: 10
* Customer's refusal probability = 0.1
"""

#Locations
locations_list = [('계양구',0), ('미추홀구',1), ('부평구', 2), ('용산구',3), ('마포구',4), ('서초구',5), ('송파구',6), ('유성구',7), ('서구',8), ('중구',9)]
travel_time_list = [[0, 3, 2, 9, 8, 11, 11, 23, 25, 25], [3, 0, 2, 9, 8, 11, 11, 23, 25, 25], [2, 2, 0, 7, 6, 9, 9, 21, 23, 23], [9, 9, 7, 0, 1, 2, 2, 14, 16, 16], [8, 8, 6, 1, 0, 3, 3, 15, 17, 17], [11, 11, 9, 2, 3, 0, 3, 12, 14, 14], [11, 11, 9, 2, 3, 3, 0, 15, 17, 17], [23, 23, 21, 14, 15, 12, 15, 0, 2, 2], [25, 25, 23, 16, 17, 14, 17, 2, 0, 3], [25, 25, 23, 16, 17, 14, 17, 2, 3, 0]]

#Generating Vehicles
vehicles_quantity = 10
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
reservation_index = 0
booking_quantity = 5
reservations = []
block_num = 144
refuse_probability = 0.5

for i in range(booking_quantity):
  reservation_index += 1
  start_location = rd.choice(locations_list)
  end_location = rd.choice(locations_list)
  end_time = 100000
  while end_time > block_num:
    travel_time = travel_time_list[start_location[1]][end_location[1]]
    start_time = rd.randrange(0,block_num)
    end_time = start_time + travel_time + round(abs(np.random.normal(4, 2)))
  new_booking = Reservation(start_time, end_time, start_location, end_location, reservation_index)
  refuse_with_probability(new_booking, refuse_probability)
  reservations.append(new_booking)
new_reservation = rd.choice(reservations)
print(new_reservation.start_time, new_reservation.end_time, new_reservation.start_location[0], new_reservation.end_location[0])

'''<h1> Generating Initial Schedule </h1>'''


#block list which includes reservation list
startime_block = list(list(None for i in range(0, vehicles_quantity)) for i in range(0,block_num))


#Dispatching each reservation to available vehicle
def dispatching(vehicles, reservations):
  ##sorted_reservations = sorted(reservations, key=lambda reservation: reservation.start_time)
  for i in range(len(reservations)):
    #print(sorted_reservations[i].index, sorted_reservations[i].start_time)
    this_reservation = reservations[i]
    candidates = []
    for j in range(len(vehicles)):
      overlaps_vehicle_tuple = overlaps_vehicle(this_reservation, vehicles[j])
      if overlaps_vehicle_tuple[0] == False:
      #if overlaps_vehicle == False:
        #candidates.append(vehicles[j])
        candidates.append([vehicles[j],overlaps_vehicle_tuple[1]] )
    if len(candidates) == 0:                                                                    #candidate 0 이면 일단 취소한다는 건가?
      continue
    #print(len(candidates))

    selected_vehicle_tuple = rd.choice(candidates)
    #selected_vehicle = rd.choice(candidates)
    selected_vehicle = selected_vehicle_tuple[0]
    this_reservation_order = selected_vehicle_tuple[1]
    if this_reservation_order == -1:
      this_reservation_order = len(selected_vehicle.dispatchings)
    selected_vehicle.dispatchings.insert(this_reservation_order, this_reservation)
    this_reservation.vehicle = selected_vehicle.index

    startime_block[this_reservation.start_time][this_reservation.vehicle - 1] = this_reservation
    #print(i, 'th reservation be successfully dispatched')

#New reservation
def new_reservation():
  reservation_index = len(reservations) + 1
  start_location = rd.choice(locations_list)
  end_location = rd.choice(locations_list)
  end_time = 100000
  while end_time > block_num:
    travel_time = travel_time_list[start_location[1]][end_location[1]]
    start_time = rd.randrange(0,block_num)
    end_time = start_time + travel_time + round(np.random.normal(4, 2))
    #print(travel_time)
    #print(start_time)
    #print(end_time)
    #print(reservation_index)
  new = Reservation(start_time, end_time, start_location, end_location, reservation_index)
  refuse_with_probability(new, refuse_probability)
  reservations.append(new)
  return new

#Making 10m-basis time to day-hour-minute form
def convertToDateTime(tenm_time):
  total_min = tenm_time*10
  total_hour = total_min//60
  remain_min = total_min%60
  total_date = 1+total_hour//24
  remain_hour = total_hour%24
  return '2023-08-0' + str(total_date) + ' ' + str(remain_hour).zfill(2) + ':' + str(remain_min).zfill(2) + ':00'

#main
dispatching(vehicles, reservations)

for i in range(len(vehicles)):
  this_vehicle = vehicles[i]
  print("The car", i, "has been dispatched", end = " ")
  for j in range(len(this_vehicle.dispatchings)):
    this_dispatchings = this_vehicle.dispatchings[j]
    print(this_dispatchings.index, end = " ")
  print()

#Generating Gantt Chart
gantt_data = []
for i in range(vehicles_quantity):
  print('This is car No.'+str(vehicles[i].index)+'\'s reservations: ')
  for j in range(len(vehicles[i].dispatchings)):
    this_booking = vehicles[i].dispatchings[j]
    newdict = dict(Task=str(this_booking.index), Start=str(convertToDateTime(this_booking.start_time)), Finish=str(convertToDateTime(this_booking.end_time)), Resource='Car No.'+str(vehicles[i].index), Location=str(this_booking.start_location[0]) + ' to ' + str(this_booking.end_location[0]))
    print('   '+ str(this_booking.index) + 'starts at ' + str(convertToDateTime(this_booking.start_time)) + 'from ' + str(this_booking.start_location[0]) + 'and ends at ' + str(convertToDateTime(this_booking.end_time)) + ' to ' + str(this_booking.end_location[0]))
    gantt_data.append(newdict)
print(len(gantt_data))
df = pd.DataFrame(gantt_data)

fig = px.timeline(df, x_start="Start", x_end="Finish", y="Resource", color="Task", text="Location")
fig.show()

""" Dynamic Schedule """

#Rescheduling:
 #들어온 예약을 바로 할당할 수 있는 차량이 있으면 바로 할당하기
 #할당할 수 있는 차량이 없으면
  #overlap되는 예약을 모두 rescheduling_candidates 리스트에 저장한 후
  #모든 overlap되는 예약들에 대해 다시 서로 overlap되지 않는 예약이 있는지 search한 뒤에
  #overlap되지 않는 예약이 있다면 그 예약을 한 차량에 배정하기 -> 여기까지 함
    #그 다음, 들어온 예약을 빈 공간이 생긴 차에 할당하기 -> 이건 아직 안 함
def rescheduling(Reservation):
  rescheduling_candidates = []    #새로운 예약과 시간이 겹치는 예약들을 보관
  for i in range(len(vehicles)):    #모든 차량에 대해서 겹치는 예약 검색; 각 차량 하나에 대해서
    this_vehicle = vehicles[i]
    count = 0
    for j in range(len(this_vehicle.dispatchings)):   #각 예약 하나에 대해서
      if overlaps(this_vehicle.dispatchings[j], Reservation):   #그 예약이 새로운 예약과 겹치는 경우
        rescheduling_candidates.append(this_vehicle.dispatchings[j])    #cadidates 리스트에 겹치는 예약 저장
        count += 1    #해당 차량에 대해 새로운 예약과 겹치는 예약의 갯수
    if count == 0:    #해당 챠량이 새로운 예약과 겹치는 예약이 전혀 없을 경우
      this_vehicle.dispatchings.append(Reservation)   #새로운 예약을 해당 차에 할당하고
      Reservation.vehicle = this_vehicle.index
      print("Code: 01")
      return 0    #종결

  #모든 차량에 대해서 겹치는 예약이 존재하는 경우 **중요 고려사항: Real-time이기 때문에 이미 진행 중인 예약은 건들면 안 됨!**
  for i in range(len(rescheduling_candidates)-1):
    #print('i = ', i)
    for j in range(i+1, len(rescheduling_candidates)):
      #print('j = ', j)
      if rescheduling_candidates[i].vehicle != rescheduling_candidates[j].vehicle:
        if overlaps(rescheduling_candidates[i], rescheduling_candidates[j]) == False:
          this_vehicle = vehicles[rescheduling_candidates[i].vehicle - 1]
          that_vehicle = vehicles[rescheduling_candidates[j].vehicle - 1]
          '''
          print('------------')
          print(this_vehicle.index)
          print(that_vehicle.index)
          print('------------')
          '''
          #overlaps_vehicle_tuple_1 = overlaps_vehicle(rescheduling_candidates[j], this_vehicle)[0]
          #overlaps_vehicle_tuple_2 = overlaps_vehicle(rescheduling_candidates[i], that_vehicle)[0]
          if overlaps_vehicle(rescheduling_candidates[j], this_vehicle)[0] == False:
            that_vehicle.dispatchings.remove(rescheduling_candidates[j])
            if overlaps_vehicle(Reservation, that_vehicle) == False:
              rescheduling_candidates[j].vehicle = rescheduling_candidates[i].vehicle
              this_vehicle.dispatchings.append(rescheduling_candidates[j])
              #that_vehicle.dispatchings.remove(rescheduling_candidates[j])
              that_vehicle.dispatchings.append(Reservation)
              Reservation.vehicle = that_vehicle.index
              startime_block[Reservation.start_time][Reservation.vehicle - 1] = Reservation
              print('Code: 02')
              return 0
            else:
              that_vehicle.dispatchings.append(rescheduling_candidates[j])
              continue
          elif overlaps_vehicle(rescheduling_candidates[i], that_vehicle)[0] == False:
            this_vehicle.dispatchings.remove(rescheduling_candidates[i])
            if overlaps_vehicle(Reservation, this_vehicle) == False:
              rescheduling_candidates[i].vehicle = rescheduling_candidates[j].vehicle
              that_vehicle.dispatchings.append(rescheduling_candidates[i])
              #this_vehicle.dispatchings.remove(rescheduling_candidates[i])
              this_vehicle.dispatchings.append(Reservation)
              Reservation.vehicle = this_vehicle.index
              startime_block[Reservation.start_time][Reservation.vehicle - 1] = Reservation
              print('Code: 03')
              return 0
            else:
              this_vehicle.dispatchings.append(rescheduling_candidates[i])
              continue
      else: continue
  print('Code: 04')
  return False

#Rescheduling test
new = new_reservation()
print('This booking starts at ', new.start_time, 'from ', new.start_location, 'and ends at ', new.end_time, 'at ', new.end_location)

for i in range(40): rescheduling(new_reservation())

#Generating Gantt Chart
gantt_data = []
for i in range(vehicles_quantity):
  print('This is car No.'+str(vehicles[i].index)+'\'s reservations: ')
  for j in range(len(vehicles[i].dispatchings)):
    this_booking = vehicles[i].dispatchings[j]
    newdict = dict(Task=str(this_booking.index), Start=str(convertToDateTime(this_booking.start_time)), Finish=str(convertToDateTime(this_booking.end_time)), Resource='Car No.'+str(vehicles[i].index), Location=str(this_booking.start_location[0]) + ' to ' + str(this_booking.end_location[0]))
    print('   '+ str(this_booking.index) + 'starts at ' + str(convertToDateTime(this_booking.start_time)) + 'from ' + str(this_booking.start_location[0]) + 'and ends at ' + str(convertToDateTime(this_booking.end_time)) + ' to ' + str(this_booking.end_location[0]))
    gantt_data.append(newdict)
print(len(gantt_data))
df = pd.DataFrame(gantt_data)

fig = px.timeline(df, x_start="Start", x_end="Finish", y="Resource", color="Task", text="Location")
fig.show()

#Refusal Rescheduling


#block_t에서 refusal 발생했는지 확인하고 refusal reservation list return
def refusal(t):
  refuse_list = []
  block_t = startime_block[t]
  if len(block_t) == 0:
    return refuse_list
  else:
    for i in range(len(block_t)):
      if block_t[i] == None:
        continue
      elif block_t[i].refusal == True:
        refuse_list.append(block_t[i])
  return refuse_list


#block_t에서 refusal이 일어난 vehicle 중 차를 못 쓰는 시간 동안의 예약들을 return   #일단 차 못 쓰는 시간 2시간으로 픽스
def unavail_car_reser(refuse_list, t):
  unavail_list = []
  for i in range(len(refuse_list)):
    unavail_vehicle = refuse_list[i].vehicle
    for i in range(1,12):   #block 11개(2시간-10분) check
      if startime_block[t+i][unavail_vehicle- 1] == None:
        continue
      else:
        unavail_list.append(startime_block[t+i][unavail_vehicle - 1])
  return unavail_list

def new_reservation_with_probability(t, probability):
  if rd.random() < probability:
    reservation_index = len(reservations) + 1
    start_location = rd.choice(locations_list)
    end_location = rd.choice(locations_list)
    start_time = t
    end_time = 100000
    while end_time > block_num:
      travel_time = travel_time_list[start_location[1]][end_location[1]]
      end_time = start_time + travel_time + round(np.random.normal(4, 2))
    new = Reservation(start_time, end_time, start_location, end_location, reservation_index)
    refuse_with_probability(new, refuse_probability)
    reservations.append(new)
    return new


new_reservation_probability = 0.3

#시간 흐르게
time_step = 1 #10분
for t in range(0, block_num, time_step):
  if t == 100:
    break

  new_reser = new_reservation_with_probability(t, new_reservation_probability)
  #print(new_reser)
  refuse_list = refusal(t)
  unavail_list = []

  if len(refuse_list) == 0:
    pass
  else:
    #refuse_list에 있는 reservations의 vehicle에서 뒤에 2시간 사이에 예약 있는지 확인. 그 예약도 같이 리스트에 넣어서 rescheduling
    unavail_list = unavail_car_reser(refuse_list, t)

  if new_reser != None:
    print('new reservation occurs')
    rescheduling(new_reser)

  if len(refuse_list) != 0:
    for i in range(len(refuse_list)):
      print('rejection occurs')
      rescheduling(refuse_list[i])

  if len(unavail_list) != 0:
    for i in range(len(unavail_list)):
      print('unavil_reser occurs')
      rescheduling(unavail_list[i])

  print('block' + str(t) + ' ends')
  print()

#Rescheduling under cancellation situation
def cancellation():
