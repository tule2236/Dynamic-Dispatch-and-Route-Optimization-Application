# work balance by the distance
from simanneal import Annealer
import math, pdb
import numpy as np 
class TravellingSalesmanProblem(Annealer):
    import random
    """Test annealer with a travelling salesman problem.
    """
    # pass extra data (the distance matrix) into the constructor
    def __init__(self, state, distance_matrix):
        self.distance_matrix = distance_matrix
       
        super(TravellingSalesmanProblem, self).__init__(state)  # important!

    def move(self):
        import random
        """Swaps two cities in the route."""
        a = random.randint(0, len(self.state) - 1)
        b = random.randint(0, len(self.state) - 1)
        self.state[a], self.state[b] = self.state[b], self.state[a]

    def energy(self):
        """Calculates the length of the route."""
        e = 0
        for i in range(len(self.state)):
            e += self.distance_matrix[self.state[i-1]][self.state[i]]    
        return e

def distance(lat1, long1, lat2, long2):
    radius_earth = 3959
    # Convert latitude and longitude to
    # spherical coordinates in radians.
    degrees_to_radians = math.pi/180.0
    phi1 = lat1 * degrees_to_radians
    phi2 = lat2 * degrees_to_radians
    lambda1 = long1 * degrees_to_radians
    lambda2 = long2 * degrees_to_radians
    dphi = phi2 - phi1
    dlambda = lambda2 - lambda1

    a = haversine(dphi) + math.cos(phi1) * math.cos(phi2) * haversine(dlambda)
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1-a))
    d = radius_earth * c
    return d

def haversine(angle):
  h = math.sin(angle / 2) ** 2
  return h

def distance_2_point(a, b):
    import math
    """Calculates distance between two latitude-longitude coordinates."""
    R = 3963  # radius of Earth (miles)
    lat1, lon1 = math.radians(a[0]), math.radians(a[1])
    lat2, lon2 = math.radians(b[0]), math.radians(b[1])
    try:
        result = math.acos(math.sin(lat1) * math.sin(lat2) +
                     math.cos(lat1) * math.cos(lat2) * math.cos(lon1 - lon2)) * R
    except ValueError:
        result = 0
    return result

def euclidean(point1,point2):
    euclideandistance=math.sqrt(sum([(a - b) ** 2 for a, b in zip(point1, point2)]))
    return euclideandistance

def create_list(job_file):
    import pandas as pd
    from sklearn import preprocessing
    import numpy as np
    job_list = []
    job = pd.read_csv(job_file)
    for i in range(len(job)):
        job_list.append( [ job['Address'].loc[i], job['Longitude'].loc[i], job['Latitude'].loc[i], job['Description'].loc[i] ] )
    return job_list

import dispy
class FilterNodeAllocate(dispy.NodeAllocate):
   def allocate(self, cluster, ip_addr, name, cpus, avail_info=None, platform=''):
       # use only nodes that have 1GB of memory and 100GB of disk space available
       # and run Linux 64-bit
       GB = 1024 / 3

       if (isinstance(avail_info, dispy.DispyNodeAvailInfo) and
           avail_info.memory > GB ):
           return cpus # use all available CPUs on this node
       else:
           return 0

def routing( data, route ):
    import random, math
    import matplotlib.pyplot as plt
    import routing

    print(route)
    
    cities, unormalized_cities = {}, {}
    name = {}

    # assign a group of cities to different workers
    for i in range(len(route)):
      cities[route[i][1]] = route[i][2:4]
      unormalized_cities[route[i][1]] = [data[route[i][0]][1:3], route[i][0], route[i][4]] 
      if route[i][1] in name:
        name[route[i][1]].append(route[i][0])
      else:
        name[route[i][1]] = [ route[i][0] ]
    # initial state, a randomly-ordered itinerary
    init_state = list(cities.keys())
    random.shuffle(init_state)

    # create a distance matrix
    distance_matrix = {}
    for ka, va in cities.items():
      distance_matrix[ka] = {}
      for kb, vb in cities.items():
          if kb == ka:
              distance_matrix[ka][kb] = 0.0
          else:
              distance_matrix[ka][kb] = distance_2_point(va, vb)

    tsp = TravellingSalesmanProblem(init_state, distance_matrix)
    tsp.steps = 100000
    # since our state is just a list, slice is the fastest way to copy
    tsp.copy_strategy = "slice"
    state, e= tsp.anneal()
    route = [ ]   

    while state[0] != list(name.keys())[0]:
      state = state[1:] + state[:1]  
      
    print()
    print("%i mile route:" % e)

    x, y =[],[]
    city_route = []
    
    for city in state:     
        x.append(cities[city][0])
        y.append(cities[city][1])
        for jobInd in name[city]:
            city_route.append([city, unormalized_cities[city][0][0], unormalized_cities[city][0][1], jobInd, unormalized_cities[city][2]])

    # plot the optimized route on the normalized coordinate
    # plt.plot(x, y, 'r', zorder=1, lw=3)
    # plt.scatter(x, y, s=120, zorder=2)
    # plt.show()  
    return city_route

def find_clusters(data, nofv):
    from math import sqrt
    from math import sin,cos
    import numpy as np
    from random import randint
    import random
    import matplotlib.pyplot as plt
    
    host = socket.gethostname()

    def euclidean(point1,point2):
        euclideandistance=sqrt(sum([(a - b) ** 2 for a, b in zip(point1, point2)]))
        return euclideandistance

    def findminpoint(address,series,startpoint):
        distancelist=[]
        for i in range(0,len(series)):
            for j in range(0,len(address)):
                distancelist.append(euclidean(startpoint[series[i]],address[j]))
        darr=np.array(distancelist)
        return (darr.argmin()-1)%len(address)

    def averagelocation(address):      
        rowx=0
        rowy=0
        averloc=[]
        for j, i in enumerate(address):
            rowx+=i[0]
            rowy+=i[1]     
        averloc=[rowx/len(address),rowy/len(address)]
        return averloc 

    def routeoptimize(routelist):
        totalpoint=len(routelist)
        totaldistance=[]
        for i in range(0,len(routelist)):
            temptdistance=0
            finishlist=[routelist[i]]
            startlist=routelist.copy()
            currentpoint=routelist[i]
            startlist.pop(i)
            while len(finishlist)!=totalpoint:
                 distopoint=[]
                 for j in range(0,len(startlist)):
                     distopoint.append(euclidean(currentpoint,startlist[j]))
                 darr = np.array(distopoint)
                 currentpoint=startlist[darr.argmin()]
                 temptdistance+=darr.min()
                 finishlist.append(currentpoint)
                 startlist.pop(darr.argmin())
            totaldistance.append(temptdistance)     
        darr2 = np.array(totaldistance)
        return darr2.min()

    address, job =[], []
    for i, row in enumerate(data):
        job.append( (i, row[0], row[1], row[2], row[3])) #[index, address, lat, long, description)]
        address.append( row[1:3] )

    maxdistance=routeoptimize(address)
    limitdistance=maxdistance/nofv 

    totalpoint=len(address)
    startpointindex=[]
    iterationseed=[]
    b=randint(0,len(address)-1)
    startpointindex.append(b)

    # Initialize center 'mu'
    oldmu = random.sample(address, nofv)
    startpoint = random.sample(address, 1)

    while len(startpoint) <= nofv:
        cent = startpoint
        D2 = np.array([sum([np.linalg.norm(np.array(x)-c)**2 for c in cent]) for x in address])
        ind = np.argmax(D2)       
        next_center = address[ind]
        startpoint.append(next_center)
    startpoint.pop(0)
    iterationseed = startpoint[:]
    iteration = 1

    # Convergence condition
    while not (set([tuple(a) for a in iterationseed]) == set([tuple(a) for a in oldmu])) and iteration <= 300:
        iteration += 1
        oldmu= iterationseed
        workaddress=address.copy()
        job_list = job.copy()

    # cluster is reset        
        cluster=[]
        series=[]
        for i in range(0,nofv):
            cluster.append([])
            series.append(i)
        totalsizecluster=sum([len(cluster[i]) for i in range(0,len(cluster))])
        while totalsizecluster<len(address):
            #check if any cluster is saturated
            if len(series)>1: 
                indice=-1
                for i in range(0,len(series)):
                    if len(cluster[series[i]])>0:
                        clusterdistance=routeoptimize([x[2:4] for x in cluster[series[i]]])
                        if clusterdistance>=limitdistance:
                            indice=i
                if indice!=-1:
                    series.pop(indice)               
                comparedistance=[]
                aindex=findminpoint(workaddress,series,startpoint)
                for i in range(0,len(series)):
                    comparedistance.append(euclidean(workaddress[aindex],startpoint[series[i]]))
                darr=np.array(comparedistance)
                cluster[series[darr.argmin()]].append(job_list[aindex])
                workaddress.pop(aindex) 
                job_list.pop(aindex)
                totalsizecluster=sum([len(cluster[i]) for i in range(0,len(cluster))])
            else:
                cluster[series[0]].append(job_list[0])
                workaddress.pop(0) 
                job_list.pop(0)
                totalsizecluster=sum([len(cluster[i]) for i in range(0,len(cluster))])
        
        # print('cluster',[ len(cluster[i]) for i in range(len(cluster))])
        for i in range(0,nofv):
            startpoint[i]=averagelocation([x[2:4] for x in cluster[i]])
        iterationseed = startpoint 

    # check if any cluster has <= 1 jobs
    # lengthList = [len(x) <= 1 for x in cluster]
    # if any(lengthList): # if the cluster is saturated
    #     indice = [i for i,j in enumerate(lengthList) if j == True]

    return host,cluster

def func(data, K):
    import dispy, logging, random, os, math, sys, threading
    from sklearn import preprocessing
    import pandas as pd 
    import numpy as np
    import matplotlib.pyplot as plt 

    jobs_cond = threading.Condition()
    map_cluster = dispy.JobCluster(find_clusters, nodes=['*'] , depends = [routing])
    #map_cluster = dispy.JobCluster(find_clusters, nodes=[FilterNodeAllocate('13.229.83.167','*')] )

    # map_cluster = dispy.JobCluster(find_clusters, nodes=['*'],ip_addr='172.31.28.189')
    # cluster_status = status_cb)

    jobs, optimized_route= {}, []
    job = map_cluster.submit(data, K)
    if job.status == dispy.DispyJob.Created or job.status == dispy.DispyJob.Running:
        host, delta_clusters = job()
        print('%s executed job %s at %s with %s' % (host, job.id, job.start_time, [len(x) for x in delta_clusters] ))
  
    for route in delta_clusters:
        optimized_route.append( routing(data, route) )

    map_cluster.print_status()
    map_cluster.close()
    # print('optimized', [len(x) for x in optimized_route])
    return optimized_route

# if __name__ == '__main__':
#    data = create_list('Joblist_reduced.csv')
#    route= find_clusters(data, 3)