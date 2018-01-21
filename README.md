# Dynamic-Dispatch-and-Route-Optimization-Application 
# Motivation
Skyfy Technology which is provides vehicle tracking and fleet management system on subscription basis. While interning there, I have worked on the Dynamic Job Dispatch algorithm on Mobile and Web platform. Dispatch function has proved to increase productivity and efficiency by more than two times by assigning the most ideal list of jobs to an appropriate worker. Moreover, I also designed the Route Optimization algorithm that plan the shortest route for the assigned list of jobs given the dispatch decision, workload, and job descriptions. This function helps to reduce delivery timing and cost by at least 10%.
# Prerequisites
- [Python](https://www.python.org/downloads/)
- [Dispy](http://dispy.sourceforge.net/dispy.html)
- [Flask](http://flask.pocoo.org/)
- [MySQL](https://www.mysql.com/downloads/)
- [Android](https://developer.android.com/index.html)

# 3-tier Architecture
I design the Dynamic Dispatch application following a 3-tier architecture which are well-known to shorten time to market and reduces the cost to integrate new features into software. It can also maximize user adoption through the flexibility it provides when integrating analytics into existing  infrastruture and application workflows.  
3-tier architecture is a client-server architecture in which the user interface, functional process logic and data storage are developed and maintained as independent modules on separate platforms:
- **Presentation Layer**: sends unassigned jobs to browsers and displays them as light blue markers. Then, after receiving the clustered jobs from the application layer, displaying them on the *manager interface* with different colors for different groups and send these assigned jobs to *driver interface*. If the drivers finish their jobs, they can send signals to the application and the job markers would be disappeared on the map.  The layer is written in HTML, Javascript and jQuery.
- **Application Layer**: implement clustering, assignment and route optimization algorithms on Python platform.  
    + Clustering: I revised **Unsupervised Learning** algorithm, k-means clusters, to cluster jobs lists into approximately similar workload job groups. This customized k-means considers job locations, workload, due time, and job durations to result the best clusters
    + Assignment: I apply the **Hungarian algorithm** to assign the most ideal workers to the clustered jobs.
    + Route optimization: I apply **Randomized Optimization_Simulated Annealing** to find the shortest path for each job cluster. 

- **Data Layer**: store new jobs as "unassigned" jobs and pass them to the application layer, which arrange jobs to the most optimized route, dispatch to the ideal driver. The database system runs the query, update job statuses to "assigned" and format them into both manager and driver interface. After the drivers finish their assigned jobs, they can send signals on the presentation layer, and update the job statuses to "finished" in the data layer, and delete the markers of finished jobs on the data layer. The data management system is on MySQL.

# Dynamic Dispatch Algorithm
The application can take the list of jobs through the uploaded excel file or every single job that a user inputs into the interface. The input data would contain information such as job addresses, workloads and job descriptions.  

![alt text](https://user-images.githubusercontent.com/30711638/35186355-dc53c538-fde0-11e7-9ad2-990abbddc8e7.png)
After uploading, the [Google Geocoding API](https://developers.google.com/maps/documentation/javascript/geocoding) converts the job addresses into geographic coordinates, which are used to place markers on the map. The markers of unassigned jobs have light blue color.  
![alt text](https://user-images.githubusercontent.com/30711638/35186909-05c32da6-fdea-11e7-978f-94c641a6e83c.png)  

In the back-end the **clustering algorithm** will group the list of input jobs into the most ideal number of job groups depending on the number of active vehicles, job locations, workload, due time and job durations. Afterward, the algorithm assigns the clustered jobs into the appropriate drivers (**assignment problem**), and plans the shortest routes for the clustered jobs based on the locations, workload and due time (**route optimization**).  

![alt text](https://user-images.githubusercontent.com/30711638/35186313-14e50318-fde0-11e7-906f-7cbc068f14a4.png)

The application can **dispatch jobs dynamically**, which means that every time users input new jobs, the app would combine them with all unfinished jobs and repeat clustering, assignment and route optimization algorithms to dispatch the new ideal groups of jobs. This process makes sure that all the jobs get assigned to the most ideal worker and arranged to the most optimized route.  
![alt text](https://user-images.githubusercontent.com/30711638/35186959-cfb2899a-fdea-11e7-959c-10e28a922436.png)  

The application has **two user sides**: one for the **managers** to dispatch the jobs, and one for the **drivers** to view the dispatched jobs and update the job status when the drivers have finished their assigned tasks. The manager-side interface is built on [Flask](http://flask.pocoo.org/), a micro web framework written in Python while the driver-side interface is built on [Android](https://developer.android.com/studio/index.html).  

# Distributed Computing using Dispy module
In deployment, this application will be used by many users. Considering Skyfy Technology, the company that I interned, currently have approximately 1000 subscribers and more than 3000 vehicles tracked. If for any given time, 1% of the subscribers process their jobs on the application (either managers upload and dispatch new jobs, or drivers update the job status from "assigned" to "finished"), our application has to process 10 different job lists through three algorithms which are clustering, assignment, route optimization and display the results on the map. Each job list might contain 20 to 200 jobs depending on the company sizes, thus resulting a huge amount of jobs for our application to process. In order to prevent slow processing time, or even worse, congestion, I use [Dispy](http://dispy.sourceforge.net/dispy.html), an API that support **distributed computing** written in Python to share and process the program on multiple computers, improving efficiency and performance. 
