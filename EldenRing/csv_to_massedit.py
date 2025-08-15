# ===== ======== ======== ======== ======== =====


# ===== Replace fakes with real to use, I've commented out my uses =====



# ===== Fields with padding =====

fields = [
    "fakefield1:",
    "fakefield1:",
]

#fields = [
#    "lotteryWeight0:      ",
#    "lotteryWeight1:      ",
#    "lotteryWeight2:      ",
#    "lotteryWeight3:      ",
#    "lotteryWeight4:      ",
#    "lotteryWeight5:      ",
#    "lotteryWeight6:      ",
#    "lotteryWeight7:      ",
#    "lotteryWeight8:      ",
#    "lotteryWeight9:      ",
#    "lotteryWeight10:     ",
#    "lotteryWeight11:     ",
#    "lotteryWeight12:     ",
#    "lotteryWeight13:     ",
#    "lotteryWeight14:     ",
#    "lotteryWeight15:     ",
#    "timezoneLimit:       ",
#    "timezoneStartHour:   ",
#    "timezoneStartMinute: ",
#    "timezoneEndHour:     ",
#    "timezoneEndMinute:   ",
#]


#fields = [
#"NextLotIngameSecondsMin:             ",
#"NextLotIngameSecondsMax:             ",
#"aiSightRate:                         ",
#"DistViewWeatherGparamOverrideWeight: ",
#]



# ===== Multiple CSV lines, (Do Not Forget The Comma ) =====
#csv_lines = [
#"610000000,20, 380,200,200,180,60,40,0,0,0  ,0 ,0,0  ,0,0,0,0,0,0 ,0,0,",
#"610000001,20, 280,100,100,70 ,60,40,0,0,400,0 ,0,0  ,0,0,0,6,5,30,6,20,",
#"620000000,20, 400,20 ,180,210,70,0 ,0,0,100,70,0,0  ,0,0,0,0,0,0 ,0,0,",
#"630000000,20, 380,200,200,180,60,40,0,0,0  ,0 ,0,0  ,0,0,0,0,0,0 ,0,0,",
#"630000001,20, 280,100,100,70 ,60,40,0,0,400,0 ,0,0  ,0,0,0,6,5,30,6,20,",
#"635000000,20, 390,200,200,200,60,0 ,0,0,0  ,0 ,0,0  ,0,0,0,0,0,0 ,0,0,",
#"640000000,0 , 600,140,140,130,40,0 ,0,0,0  ,0 ,0,0  ,0,0,0,0,0,0 ,0,0,",
#"641000000,1 , 800,0  ,0  ,200,70,0 ,0,0,0  ,0 ,0,0  ,0,0,0,0,0,0 ,0,0,",
#"680000000,0 , 410,150,150,180,70,60,0,0,50 ,20,0,0  ,0,0,0,0,0,0 ,0,0,",
#"680000100,0 , 410,150,150,180,70,60,0,0,50 ,20,0,0  ,0,0,0,0,0,0 ,0,0,",
#"683000000,0 , 50 ,0  ,0  ,260,0 ,0 ,0,0,10 ,10,0,720,0,0,0,0,0,0 ,0,0,",
#"690000000,0 , 410,150,150,180,70,60,0,0,50 ,20,0,0  ,0,0,0,0,0,0 ,0,0,",
#]

#csv_lines = [
#"20,7200,18000,1,0.3",
#"21,7200,18000,0.9,0.3",
#"30,7200,18000,0.8,0.3",
#"52,7200,18000,0.8,0.3",
#]

csv_lines = [
    "fakeRowID,fakefield1,fakefield2",
]

# ===== Toggle to strip all spaces =====
strip_all_spaces = True  # set False to keep spaces

# ===== Process Each CSV Line =====
for csv_line in csv_lines:
    if strip_all_spaces:
        csv_line = csv_line.replace(" ", "")

    # Clean CSV values
    values = [' '.join(val.strip().split()) for val in csv_line.strip(',').split(',')]

    # Extract ID
    row_id = values[0]
    data_values = values[1:]  # skip ID for pairing

    # Generate Smithbox Output
    for field, val in zip(fields, data_values):
        print(f"param WeatherLotParam: id {row_id}: {field}= {val};")
