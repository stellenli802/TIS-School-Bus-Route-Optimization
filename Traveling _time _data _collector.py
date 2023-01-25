import requests
import datetime
#this code is used to find the durations from every bus stop to all other stops
#it is ran on every weekday morning at 7:24 and 7:42 to get average travel times with consideration of traffic

#constants for requesting a URL to get a duration of each segment
KEY = '7487ef48b2a8734006f9c9106dca8299'
URL_constant = 'https://restapi.amap.com/v3/direction/driving?'

#opens the file with all the coordinates of the stops
#each line represents two location's coordinates at origin and destination
stops_file = open('//Users/stellenshun.li/Desktop/12th Grade/AP Research/Paper/Codes/stops/stops_copy.txt','r')
stops_names = open('//Users/stellenshun.li/Desktop/12th Grade/AP Research/Paper/Codes/stops/stops_test.txt','r')

#variables and lists used to calculate and store all the durations
orig = []
dest = []
durations = []
durations_mins = []
secToMin = 60
all_coordinates = []
stop = []
NAMES = []
names_segments = []
   
#a loop to get all the coordinates of each stop
for line in stops_file.readlines():
        #splits each line into an array in the format of [origin, destination]
        stop = line.strip()
        all_coordinates.append(stop)

#builds the request URL for this segment; the URL gets the duration for each segment and puts the duration(sec) into the durations list
for i in range(len(all_coordinates)):   
    for j in range(i, len(all_coordinates)):
        orig = all_coordinates[i]
        dest = all_coordinates[j]
        URL = "https://restapi.amap.com/v3/direction/driving?key=7487ef48b2a8734006f9c9106dca8299&" + "origin=" + orig + "&destination=" + dest 
        URL2 = URL + "&originid=&destinationid=&extensions=base&strategy=10&waypoints=&avoidpolygons=&avoidroad="
        resp = requests.get(URL2)
        durations.append(resp.json()['route']['paths'][0]['duration'])
        for k in range(0, len(durations)):
            durations[k] = int(durations[k])
            
#converts all durations from seconds to minutes rounded to the nearest 1 decimal place
durations_mins = [num/secToMin for num in durations]
for i in range(len(durations)):
    durations_mins[i] = float(round(durations_mins[i], 1))
    durations_mins[i] = str(durations_mins[i])
    
#gets current time and date (month day year)
time = datetime.datetime.now()
time = time.strftime('%a-%m-%d-%y')

#loads the text file with all stops' names and puts all names into segments in a format of "(stop 1) to (stop 2): "
for line in stops_names.readlines():
    name = line.strip()
    NAMES.append(name)
for i in range(len(NAMES)):
    for j in range(i, len(NAMES)):
        names_segments.append(NAMES [i] + " to " + NAMES [j] + ": ")

#creates a text file with current date as the name of the file and all stops' names and durations of that day
with open(r'//Users/stellenshun.li/Desktop/12th Grade/AP Research/Paper/Codes/Data/'+time + '.txt', 'w') as filehandle:
    for i in range(len(names_segments)):
            filehandle.write(names_segments[i] + durations_mins[i] + '\n')

        
