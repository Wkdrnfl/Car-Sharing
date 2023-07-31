import numpy as np
import random as rd
from Reservation_object import Reservation
import data


#block_t에서 refusal 발생했는지 확인하고 refusal reservation list return
def refusal(t, startime_block):
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
def unavail_car_reser(t, refuse_list, startime_block):
    unavail_list = []
    for i in range(len(refuse_list)):
        unavail_vehicle = refuse_list[i].vehicle
        for i in range(1,12):   #block 11개(2시간-10분) check
            if startime_block[t+i][unavail_vehicle- 1] == None:
                continue
            else:
                unavail_list.append(startime_block[t+i][unavail_vehicle - 1])
    return unavail_list

def new_reservation_with_probability(t, probability, reservations):
    if rd.random() < probability:
        reservation_index = len(reservations) + 1
        start_location = rd.choice(data.locations_list)
        end_location = rd.choice(data.locations_list)
        start_time = t
        end_time = 100000
        while end_time > data.block_num:
            travel_time = data.travel_time_list[start_location[1]][end_location[1]]
            end_time = start_time + travel_time + round(np.random.normal(4, 2))
        new = Reservation(start_time, end_time, start_location, end_location, reservation_index)
        new.refuse_with_probability(data.refuse_probability)
        reservations.append(new)
        return new