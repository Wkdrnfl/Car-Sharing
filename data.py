#data
locations_list = [('계양구',0), ('미추홀구',1), ('부평구', 2), ('용산구',3), ('마포구',4), ('서초구',5), ('송파구',6), ('유성구',7), ('서구',8), ('중구',9)]
travel_time_list = [[0, 3, 2, 9, 8, 11, 11, 23, 25, 25], [3, 0, 2, 9, 8, 11, 11, 23, 25, 25], [2, 2, 0, 7, 6, 9, 9, 21, 23, 23], [9, 9, 7, 0, 1, 2, 2, 14, 16, 16], [8, 8, 6, 1, 0, 3, 3, 15, 17, 17], [11, 11, 9, 2, 3, 0, 3, 12, 14, 14], [11, 11, 9, 2, 3, 3, 0, 15, 17, 17], [23, 23, 21, 14, 15, 12, 15, 0, 2, 2], [25, 25, 23, 16, 17, 14, 17, 2, 0, 3], [25, 25, 23, 16, 17, 14, 17, 2, 3, 0]]
vehicles_quantity = 10
booking_quantity = 5  #initial booking quantity
block_num = 144   #24hours
refuse_probability = 0.5
new_reservation_probability = 0.3