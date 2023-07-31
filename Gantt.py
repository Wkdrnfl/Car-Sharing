import plotly.express as px
import pandas as pd

#Making 10m-basis time to day-hour-minute form
def convertToDateTime(tenm_time):
    total_min = tenm_time*10
    total_hour = total_min//60
    remain_min = total_min%60
    total_date = 1+total_hour//24
    remain_hour = total_hour%24
    return '2023-08-0' + str(total_date) + ' ' + str(remain_hour).zfill(2) + ':' + str(remain_min).zfill(2) + ':00'


#Generating Gantt Chart
def gantt(vehicles):
    gantt_data = []
    for i in range(len(vehicles)):
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



