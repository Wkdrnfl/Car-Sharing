import random as rd
from data import travel_time_list, block_num

class Reservation:
    def __init__(self, start_time, end_time, start_location, end_location, index):
        self.start_time = start_time
        self.end_time = end_time
        self.start_location = start_location #2d tuple
        self.end_location = end_location  #2d tuple
        self.index = index
        self.vehicle = 0
        self.refusal = False

    #Customer's refusal
    def refuse_with_probability(self, probability):
        if rd.random() < probability:
            self.refusal = True

    def overlaps(self, Reservation):
        #새로운 예약의 시작 시간이 비교 예약의 종료 시간보다 늦은 경우
        if self.end_time < Reservation.start_time:
            if travel_time_list[self.end_location[1]][Reservation.start_location[1]] < (Reservation.start_time - self.end_time):      #거리 조건 만족 여부
                return False
            else: return True
        #새로운 예약의 종료 시간이 비교 예약의 시작 시간보다 이른 경우
        elif self.start_time > Reservation.end_time:
            if travel_time_list[Reservation.end_location[1]][self.start_location[1]] < (self.start_time - Reservation.end_time):      #거리 조건 만족 여부
                return False
            else: return True
        else: return True

    #A function checking whether a reservation overlaps with specific vehicle
    def overlaps_vehicle(self, Vehicle, timeblock):
        startime_index = self.start_time
        endtime_index = self.end_time
        #Check if other reservations overlap directly
        for i in range(startime_index, endtime_index+1):
            if str(type(timeblock[i][Vehicle.index-1])) != '<class \'NoneType\'>': return (True, 10000)
            else: continue
        #Check if other reservations overlap indirectly
        startime_index -= 1
        endtime_index += 1
            #Check if the reservation overlaps with previous reservation
        if startime_index >= 0:
            while str(type(timeblock[startime_index][Vehicle.index-1])) == '<class \'NoneType\'>':
                if startime_index == 0: break
                startime_index -= 1
            if startime_index != 0:
                previous_reservation = timeblock[startime_index][Vehicle.index-1]
                if self.overlaps(previous_reservation) == True: return (True, 10000)
            #Check if the reservation overlaps with following reservation
        if endtime_index >= block_num:  return (False, 10000)
        else:
            while str(type(timeblock[endtime_index][Vehicle.index-1])) == '<class \'NoneType\'>':
                if endtime_index == block_num-1: return (False, 10000)
                endtime_index += 1
            following_reservation = timeblock[endtime_index][Vehicle.index-1]
            if self.overlaps(following_reservation) == True: return (True, 10000)
            else: return (False, 10000)


 



