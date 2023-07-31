import random as rd
from data import travel_time_list

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

    def overlaps_vehicle(self, Vehicle):
        #print(len(Vehicle.dispatchings))
        vehicle_dispatchings = Vehicle.dispatchings
        if len(vehicle_dispatchings) == 0:
            return (False, 0)

        #만약 새로운 예약이 vehicle 예약 리스트에 가장 첫번째에 위치할 경우
        if self.start_time < vehicle_dispatchings[0].start_time:
            if self.end_time <= vehicle_dispatchings[0].start_time:  #travel time이 0인 경우도 있으니까 등호도 포함?
                if travel_time_list[self.end_location[1]][vehicle_dispatchings[0].start_location[1]] <= (vehicle_dispatchings[0].start_time - self.end_time): #등호 포함 추가
                    return (False,0)
                else: return (True, 100000)
            else: return (True, 100000)


        #만약 새로운 예약이 vehicle 예약 리스트에 가장 마지막에 위치할 경우
        elif self.start_time >= vehicle_dispatchings[-1].end_time:  #travel time이 0인 경우도 있으니까 등호도 포함?
            if travel_time_list[vehicle_dispatchings[-1].end_location[1]][self.start_location[1]] <= (self.start_time - vehicle_dispatchings[-1].end_time):
                return (False,-1)
            else: return (True, 100000)


        #만약 새로운 예약이 vehicle 예약 리스트에서 예약들 사이에 위치할 경우
        else:
            for i in range(len(vehicle_dispatchings)-1):
                if vehicle_dispatchings[i].end_time <= self.start_time:  #새로운 예약의 시작 시간이 비교 예약의 종료 시간 이후인 경우
                    if travel_time_list[vehicle_dispatchings[i].end_location[1]][self.start_location[1]] <= (self.start_time - vehicle_dispatchings[i].end_time): #이전 예약과의 거리 조건
                        if self.end_time <= vehicle_dispatchings[i+1].start_time:  #새로운 예약의 종료 시간이 다음 예약의 시작 시간보다 앞선 경우
                            if travel_time_list[self.end_location[1]][vehicle_dispatchings[i+1].start_location[1]] <= (vehicle_dispatchings[i+1].start_time - self.end_time): #다음 예약과의 거리 조건
                                return (False, i+1)
                            else: return (True, 100000)
                        elif vehicle_dispatchings[i+1].end_time <= self.start_time:
                            continue
                        else: return (True, 100000)
                    else: return (True, 100000)
                else: return (True, 100000)

        return (True, 100000)

    #Rescheduling:
    '''
    def rescheduling(self, vehicles):
        rescheduling_candidates = []    #새로운 예약과 시간이 겹치는 예약들을 보관
        for i in range(len(vehicles)):    #모든 차량에 대해서 겹치는 예약 검색; 각 차량 하나에 대해서
            this_vehicle = vehicles[i]
            count = 0
            for j in range(len(this_vehicle.dispatchings)):   #각 예약 하나에 대해서
                if self.overlaps(this_vehicle.dispatchings[j]):   #그 예약이 새로운 예약과 겹치는 경우
                    rescheduling_candidates.append(this_vehicle.dispatchings[j])    #cadidates 리스트에 겹치는 예약 저장
                    count += 1    #해당 차량에 대해 새로운 예약과 겹치는 예약의 갯수
            if count == 0:    #해당 챠량이 새로운 예약과 겹치는 예약이 전혀 없을 경우
                this_vehicle.dispatchings.append(self)   #새로운 예약을 해당 차에 할당하고
                self.vehicle = this_vehicle.index
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
                        
                        #print('------------')
                        #print(this_vehicle.index)
                        #print(that_vehicle.index)
                        #print('------------')
                        
                        #overlaps_vehicle_tuple_1 = overlaps_vehicle(rescheduling_candidates[j], this_vehicle)[0]
                        #overlaps_vehicle_tuple_2 = overlaps_vehicle(rescheduling_candidates[i], that_vehicle)[0]
                        if rescheduling_candidates[j].overlaps_vehicle(this_vehicle)[0] == False:
                            that_vehicle.dispatchings.remove(rescheduling_candidates[j])
                            if self.overlaps_vehicle(that_vehicle) == False:
                                rescheduling_candidates[j].vehicle = rescheduling_candidates[i].vehicle
                                this_vehicle.dispatchings.append(rescheduling_candidates[j])
                                #that_vehicle.dispatchings.remove(rescheduling_candidates[j])
                                that_vehicle.dispatchings.append(self)
                                self.vehicle = that_vehicle.index
                                #startime_block[self.start_time][self.vehicle - 1] = self
                                print('Code: 02')
                                return 0
                            else:
                                that_vehicle.dispatchings.append(rescheduling_candidates[j])
                                continue
                        elif rescheduling_candidates[i].overlaps_vehicle(that_vehicle)[0] == False:
                            this_vehicle.dispatchings.remove(rescheduling_candidates[i])
                            if self.overlaps_vehicle(this_vehicle) == False:
                                rescheduling_candidates[i].vehicle = rescheduling_candidates[j].vehicle
                                that_vehicle.dispatchings.append(rescheduling_candidates[i])
                                #this_vehicle.dispatchings.remove(rescheduling_candidates[i])
                                this_vehicle.dispatchings.append(self)
                                self.vehicle = this_vehicle.index
                                #startime_block[self.start_time][self.vehicle - 1] = self
                                print('Code: 03')
                                return 0
                        else:
                            this_vehicle.dispatchings.append(rescheduling_candidates[i])
                            continue
                else: continue
        print('Code: 04')
        return False
        '''



