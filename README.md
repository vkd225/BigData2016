```
Final Project - NYC Taxi Data
An Analysis of the Yellow Cab Data

Satish Kapalavayi sk6140
Vikash Deo vkd225
Viswanatha Mehta vsm263
```

```
### Introduction:
The New York City Taxi & Limousine Commission periodically release a staggeringly detailed historical dataset that cover almost 1.2 billion individual taxi trips in the city from January 2009 through June 2015. Along with a multitude of other datasets available such as weather and income data, it is possible to analyze the data to find particular patterns. In particular, we attempt to find the way people tip the cab drivers.

### Brief
The project will attempt to find the correlation between the way people tip and the average income of the neighborhood. The project will later delve into finding if the rider’s tip percentage varies in accordance to the distance travelled. A better analysis of the same was done, where the tip percentage dependance on time spent in the cab was measured. 

As we envisioned, the tip percentage gradually increases as the riders spend more time in the cab. This we assume is owing to the fact that the human connect between the riders and the drivers lead to more tipping. One caveat to this was when the number of passengers in the car increases, tip dependency on time spent in the car decreases. This we assume is because the passenger’s interaction to the cabbie is limited and thus the tip percentage dependency is also lower. 



Current Architecture:








The Current architecture stops with the static analysis of the data, whereas future implementations of the project will include the usage of cassandra DB system to save the output and realtime querying of the data, so that map box uses all of the information available and is not constrained by the browser’s capacity to handle.
A overall picture of the future implementation, which would use spark to make it better would be as shown below.




Reproducibility
For the sake of reproducibility, all the scripts are available under the GitHub at : https://github.com/vzmehta/BigData2016.git[0]
And the S3 bucket used is also published at s3://bigdatanyctaxi/
Technology:
The AWS Cluster Setup used: 1 core, 5 slave with custom bootstrap actions to install rtree, pyProj and shapefile extensions to python. The bootstrap shell script can be found at: s3://bigdatanyctaxi/rtree.sh
The rtree setup was based off the ViDA-NYU project.[1]
Cartographer used : MapBox 
Visualization tool used : Tableau

The Data
For This Analysis, we used the dataset that was provided by the The New York City Taxi & Limousine Commission[1]. The detailed and extensive dataset contains useful variables such as price, duration, distance, passengers, date, time, and most importantly, origin and destination latitude/longitude coordinate pairs. The zip-code data derived from shp files were used to geocode the pickup location[2].

Cleaning of Data: A simple clean of data was done, wherein only rows with data were used.
A more thorough cleaning of the data is in works, wherein we use the polygons provided by the NYC Civic Dashboard to make sure that the pickup points were not in the hudson or east river[4]. Useful until TLC provide RiverTaxi Data. 

Joining the Two Tables
TLC provide data as two tables for every month. A Fare Table with all relevant details entailing Cost/Money and a Trip Table entailing all data relevant to the trip such as location. The datasets were joined using “medallion, hack_license, vendor_id, pickup_datetime” as its key. The data Join was necessary to ensure that trip data(s) without any corresponding fare is removed and any fare data without the corresponding trip Data is removed. Also, the analysis was heavily dependent on using the data from both the datasets. The Join function here also does the initial cleaning process we require.

The Join function available under join/mapper.py and join/reducer.py in the github

The files are available at s3://bigdatanyctaxi/mapper.py,  s3://bigdatanyctaxi/reduce.py
The output is available at s3://bigdatanyctaxi/output_final

The argument  for this function should the 24 files. one Fare data and one Trip data for each month of the year.
 
Argument Used:
hadoop-streaming -D mapreduce.job.reduces=100 -files s3://bigdatanyctaxi/map.py,s3://bigdatanyctaxi/reduce.py -mapper map.py -reducer reduce.py -input s3://bigdatanyctaxi/csv01/,s3://bigdatanyctaxi/csv02/,s3://bigdatanyctaxi/cs03/,s3://bigdatanyctaxi/cs04/,s3://bigdatanyctaxi/cs05/,s3://bigdatanyctaxi/cs06/,s3://bigdatanyctaxi/cs07/,s3://bigdatanyctaxi/cs08/,s3://bigdatanyctaxi/csv09/,s3://bigdatanyctaxi/csv10/,s3://bigdatanyctaxi/csv11/,s3://bigdatanyctaxi/csv/ -output s3://bigdatanyctaxi/output_final
Running time : 33 minutes


Analysis
Every Query ran here is available in the s3 bucket and in the github link provided[0]
Tip Percentage and Pick-UP Location
The Tip Percentage clustered around pick-up Coordinates was queried.
The queries are available under s3://bigdatanyctaxi/mapper_tip.py, s3://bigdatanyctaxi/reduce_tip.py
The queries are simple enough where the mapper selects only the required data and the reducer groups all the similar data together, such that making the analysis later easier.
Arguments: hadoop-streaming -D mapreduce.job.reduces=50 -files s3://bigdatanyctaxi/mapper_tip.py,s3://bigdatanyctaxi/reduce_tip.py -mapper mapper_tip.py -reducer reduce_tip.py -input s3://bigdatanyctaxi/output_final/ -output s3://bigdatanyctaxi/tip_final_output/
Running time : 18 minutes


















Inference:
Here, form the mapBox code provided[0] and as shown in the image below, we can see that higher percentage of tippers belong to downtown or midtown business hubs.
We also see that FiDi/Wall street live up to their name of bankers and not tip enough :)
This may also be due to them paying in Cash, and cash tips do not get recorded 










Tip Variance With Passenger count
The tip variance for every passenger count clustered for every distance travelled was queried.
The most important query, here we see that our first assumption was true, where when a single passenger travels, they tend to tip more. 
Arguements: hadoop-streaming -D mapreduce.job.reduces=15 -files s3://bigdatanyctaxi/mapper_pcount.py,s3://bigdatanyctaxi/reduce_tip.py -mapper mapper_pcount.py -reducer reduce_tip.py -input s3://bigdatanyctaxi/output_final/ -output s3://bigdatanyctaxi/pcount_dist/
Running time : 13 Minutes
Inference:
This query shows the social factor that influence the tipping scale.
The same variance as distance travelled is followed here, but if the passenger count increases, the tip percentage is lower, as the interaction between the driver and the passengers are lower.



Tip Percentage and Distance Travelled
The Tip Percentage clustered around distance was queried.
The queries are available under s3://bigdatanyctaxi/mapper_dist.py, s3://bigdatanyctaxi/reduce_dist.py
Arguments: hadoop-streaming -D mapreduce.job.reduces=50 -files s3://bigdatanyctaxi/mapper_dist.py,s3://bigdatanyctaxi/reduce_tip.py -mapper mapper_dist.py -reducer reduce_tip.py -input s3://bigdatanyctaxi/output_final/ -output s3://bigdatanyctaxi/dist_tip/
Running time : 13 minutes

Inference:
Here, we see that as the passengers tend to travel more, they tend to tip more, but if the travel hits a tip over point, the tipping tends to fall back down to low double digits. 

Tip Percentage and Time Travelled
The Tip Percentage clustered around Time travelled was queried.
The queries are available under s3://bigdatanyctaxi/mapper_dist.py, s3://bigdatanyctaxi/reduce_dist.py
Arguments: hadoop-streaming -D mapreduce.job.reduces=50 -files s3://bigdatanyctaxi/mapper_time.py,s3://bigdatanyctaxi/reduce_tip.py -mapper mapper_time.py -reducer reduce_tip.py -input s3://bigdatanyctaxi/output_final/ -output s3://bigdatanyctaxi/time_tip
Running time : 14 minutes

Inference:
Here, we see that as the passengers tend to travel more, they tend to tip more, but if the travel hits a tip over point, the tipping tends to fall back down to low double digits. 

Tip Percentage variance with Time and distance Travelled
The Tip Percentage clustered around Distance travelled along with time travelled was queried.
The queries are available under s3://bigdatanyctaxi/mapper_tip_dist.py, s3://bigdatanyctaxi/reduce_dist.py
Arguments: hadoop-streaming -D mapreduce.job.reduces=50 -files s3://bigdatanyctaxi/mapper_tip_dist.py,s3://bigdatanyctaxi/reduce_tip.py -mapper mapper_tip_dist.py -reducer reduce_tip.py -input s3://bigdatanyctaxi/output_final/ -output s3://bigdatanyctaxi/time_tip_dist/
Running time : 12 minutesFuture Analysis:
Tip variance according to time of day and time of the year
This analysis would show how the tip varies as day progresses and around social hotspots such as meatpacking shows increase in tip percentages as the evening progresses.
Tip Variance according to mean income
This analysis would also show if high earning members of the community tend to tip more than the average joe. 
TipVariance according to weather Data
This is another important social factor we would like to study, where we would want to see if the weather conditions would influence the tipping.

Individual Contributions:
The whole project was a joint effort, as electrical students, we three were new to programming and data sciences and we had to help each other to learn more.
The order shows the importance given by each member to the task. 
Vishwanath - Map reduce Queries, Tableau
Vikash - Mapbox, mapreduce Queries, 
Satish - Mapreduce Queries, Data Cleaning 
REFERENCES
[0] https://github.com/vzmehta/BigData2016.git

[1] http://www.nyc.gov/html/tlc/html/about/trip_record_data.shtml

[2]https://github.com/vzmehta/BigData2016/blob/master/postal.zip

[3] https://github.com/ViDA-NYU/aws_taxi/blob/master/rtree.sh

[4] http://catalog.civicdashboards.com/dataset/e5bbe399-aee4-45d4-a7d3-d6ece7f18bf4/resource/a31b967f-3df2-47da-ac67-50fa420f9cb2/download/9a2703e0737d4aab855017ff2d636603nycboroughboundaries.geojson

```

