from Reservation_object import Reservation
from data import travel_time_list, block_num
#Rescheduling algorithms

def reschedule(new_Reservation, the_vehicles, timeblock):
  rescheduling_candidate = None
  difference_min = 1000000
  for i in range(len(the_vehicles)):
    this_vehicle = the_vehicles[i]
    time_difference = 0
    if new_Reservation.overlaps_vehicle(this_vehicle, timeblock)[0] == False:
      after_traveltime = 0
      startblock_index = new_Reservation.start_time - 1
      endblock_index = new_Reservation.end_time + 1

      if startblock_index < 0:  previous_reservation = Reservation(0, 0, this_vehicle.initial_location, this_vehicle.initial_location, -1)
      else:
        while str(type(timeblock[startblock_index][this_vehicle.index-1])) == '<class \'NoneType\'>':
          startblock_index -= 1
          #print(startblock_index)
          if startblock_index < 0:
            #print(this_vehicle.initial_location)
            previous_reservation = Reservation(0, 0, this_vehicle.initial_location, this_vehicle.initial_location, -1)
            break
        if startblock_index != -1: previous_reservation = timeblock[startblock_index][this_vehicle.index-1]
      after_traveltime += travel_time_list[previous_reservation.end_location[1]][new_Reservation.start_location[1]]

      if endblock_index >= block_num:  following_reservation = Reservation(block_num, block_num, new_Reservation.end_location, new_Reservation.end_location, -1)
      else:
        while str(type(timeblock[endblock_index][this_vehicle.index-1])) == '<class \'NoneType\'>':
          endblock_index += 1
          #print(endblock_index)
          if endblock_index >= block_num:
            following_reservation = Reservation(block_num, block_num, new_Reservation.end_location, new_Reservation.end_location, -1)
            break
        if endblock_index < block_num: following_reservation = timeblock[endblock_index][this_vehicle.index-1]
      print(this_vehicle.index, 'th vehicle\'s previous reservation: ', previous_reservation.start_time, ' to ', previous_reservation.end_time, ', from ', previous_reservation.start_location[0], ' to ', previous_reservation.end_location[0])
      print(this_vehicle.index, 'th vehicle\'s following reservation: ', following_reservation.start_time, ' to ', following_reservation.end_time, ', from ', following_reservation.start_location[0], ' to ', following_reservation.end_location[0])
      after_traveltime += travel_time_list[new_Reservation.end_location[1]][following_reservation.start_location[1]]

      if following_reservation.index == -1: initial_traveltime = 0
      else: initial_traveltime = travel_time_list[previous_reservation.end_location[1]][following_reservation.start_location[1]]

      time_difference = after_traveltime - initial_traveltime
      print(i+1, 'th car\'s time difference: ', time_difference)
      if time_difference < difference_min:
        rescheduling_candidate = this_vehicle
        difference_min = time_difference
    else: continue

  print('-------Result of minimum schedule scheme-------')
  if str(type(rescheduling_candidate)) == '<class \'NoneType\'>':
    print('Rescheduling failed')
    return 0
  else:
    rescheduling_candidate.dispatchings.append(new_Reservation)
    new_Reservation.vehicle = rescheduling_candidate.index
    timeblock[new_Reservation.start_time][rescheduling_candidate.index-1] = new_Reservation
    print('Rescheduling succeed, travel time difference is ', difference_min)
    print('The reservation has been dispatched to vehicle ', rescheduling_candidate.index)
    return 0

def reschedule_random(new_Reservation, the_vehicles, timeblock):
  for i in range(len(the_vehicles)):
    this_vehicle = the_vehicles[i]
    if new_Reservation.overlaps_vehicle(this_vehicle, timeblock)[0] == False:
      after_traveltime = 0
      startblock_index = new_Reservation.start_time - 1
      endblock_index = new_Reservation.end_time + 1
      #print(startblock_index)
      #print(endblock_index)
      if startblock_index < 0:  previous_reservation = Reservation(0, 0, this_vehicle.initial_location, this_vehicle.initial_location, -1)
      else:
        while str(type(timeblock[startblock_index][this_vehicle.index-1])) == '<class \'NoneType\'>':
          startblock_index -= 1
          #print(startblock_index)
          if startblock_index == -1:
            #print(this_vehicle.initial_location)
            previous_reservation = Reservation(0, 0, this_vehicle.initial_location, this_vehicle.initial_location, -1)
            break
        if startblock_index != -1: previous_reservation = timeblock[startblock_index][this_vehicle.index-1]
      after_traveltime += travel_time_list[previous_reservation.end_location[1]][new_Reservation.start_location[1]]

      if endblock_index >= block_num:  following_reservation = Reservation(block_num, block_num, new_Reservation.end_location, new_Reservation.end_location, -1)
      else:
        while str(type(timeblock[endblock_index][this_vehicle.index-1])) == '<class \'NoneType\'>':
          endblock_index += 1
          #print(endblock_index)
          if endblock_index >= block_num:
            following_reservation = Reservation(block_num, block_num, new_Reservation.end_location, new_Reservation.end_location, -1)
            break
      if endblock_index < block_num: following_reservation = timeblock[endblock_index][this_vehicle.index-1]
      after_traveltime += travel_time_list[new_Reservation.end_location[1]][following_reservation.start_location[1]]

      if following_reservation.index == -1: initial_traveltime = 0
      else: initial_traveltime = travel_time_list[previous_reservation.end_location[1]][following_reservation.start_location[1]]

      time_difference = after_traveltime - initial_traveltime

      this_vehicle.dispatchings.append(new_Reservation)
      new_Reservation.vehicle = this_vehicle.index
      timeblock[new_Reservation.start_time][this_vehicle.index-1] = new_Reservation
      print('-------Result of random schedule scheme-------')
      print('Rescheduling succeed, travel time difference is ', time_difference)
      print('The reservation has been dispatched to vehicle ', this_vehicle.index)
      print
      return 0

    else: continue
  print('-------Result of random schedule scheme-------')
  print('Rescheduling failed')
  return 0

def rescheduling(Reservation, vehicles, startime_block):
  rescheduling_candidates = []    #새로운 예약과 시간이 겹치는 예약들을 보관
  for i in range(len(vehicles)):    #모든 차량에 대해서 겹치는 예약 검색; 각 차량 하나에 대해서
    this_vehicle = vehicles[i]
    count = 0
    for j in range(len(this_vehicle.dispatchings)):   #각 예약 하나에 대해서
      if this_vehicle.dispatchings[j].overlaps(Reservation):   #그 예약이 새로운 예약과 겹치는 경우
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
        if rescheduling_candidates[i].overlaps(rescheduling_candidates[j]) == False:
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
          if rescheduling_candidates[j].overlaps_vehicle(this_vehicle)[0] == False:
            that_vehicle.dispatchings.remove(rescheduling_candidates[j])
            if Reservation.overlaps_vehicle(that_vehicle) == False:
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
          elif rescheduling_candidates[i].overlaps_vehicle(that_vehicle)[0] == False:
            this_vehicle.dispatchings.remove(rescheduling_candidates[i])
            if Reservation.overlaps_vehicle(this_vehicle) == False:
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