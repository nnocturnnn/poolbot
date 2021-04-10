# import pyowm

#owm = pyowm.OWM("7769486dbc7a1ffcd4ac29ea209fe0a1")

# def get_own_three_hour(lat,lon):
#     observation = owm.three_hours_forecast_at_coords(lat,lon)
#     forecast = observation.get_forecast()
#     for i in forecast:
#         print(i)
        # data_list = []
        # data_list.append(i.get_reference_time('date').strftime("%H:%M"))
        # data_list.append(i.get_temperature("celsius"))
        # for key in data_list[1]:
        #     try:
        #         data_list[1][key] = toFixed(data_list[1][key],1)
        #     except:
        #         continue
        # data_list.append(i.get_detailed_status())
        # list_wether.append(data_list)
    # return list_wether
        
    
# get_own_three_hour(50.45466,30.5238)