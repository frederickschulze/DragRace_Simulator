The goal of this project was to decide if it would be worth changing my final drive gear in my 2001 2zz swapped MR-2. I was comparing a C56 final drive gear with a C60 final drive gear, both with the 6-speed C60 gearset. In the end, I was able to justify keeping the shorter gear ratios from the C60 final drive gear. 

Horsepower and Torque curves used in this simulation. Based on csv data from a dyno of my car:
![MR2TransProject_Fig1](https://github.com/user-attachments/assets/ec1f5a84-44d2-46ca-b697-3da57446ec10)

The program simulates a drag race using this power curve along with simulated drag, time to shift gears, and rolling resistance.

The following plots show the car's performance in this drag race with the C56 and C60 final drive ratios. First is a plot of the speed over time with both final drive ratios. Second is a plot which shows the time difference between the two. The time difference is calculated based on the distance between the two cars divided by the speed of the second car. Time difference is a popular metric in racing to compare distance between the two vehicles, as it is independent of speed.
![MR2TransProject_Fig3](https://github.com/user-attachments/assets/b39b63a5-2662-4ba1-890f-1066184555cf)

The shorter ratios from the C60 results in a large time gained initially, which is important in AutoX racing where the lap always begins with a launch from standstill. Also, since the car would be in 2nd gear most of the time in AutoX runs, it's important to have better acceleration out of the corner from the shorter gearset (C60). The drawback is that the top speed in 2nd gear is lower with the C60 and shifting to 3rd gear is often awkward in AutoX, as it would normally be followed by shifting back to 2nd gear immediately. However, even if the top speed in 2nd is reached, and the driver is unable to shift, the time gained from the faster acceleration (of the C60) generally outweighs the time lost from the lower top speed. The only downside of this is being stuck at the 9000 RPM redline for several seconds in some rare cases, which could hurt engine reliability. In these cases, the driver could shift to 3rd gear early, and in most cases, still have a faster lap than with the longer C56 final drive. 

In general, the C60 final drive results in faster times at a slight potential cost to engine reliability. 
