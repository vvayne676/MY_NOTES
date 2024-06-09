 Distributed system is not simpler, then why ppl are driven to use them?
1. parallelism - because ppl want to achieve, high performance, parallelism, lots of CPUs, lots of memories, lots of disk arms moving in parallel
2. fault tolerance 
3. physical - internal bank transfer, bank a computer in NY bank b computer in London
4. security/isolated

Course will focus on above problem 1 and 2.

Challenges:
1. concurrency
2. partial failure
3. performance

This course is all about infrastructure(abstraction, look and act as a single computer):
1. storage
2. communication
3. computation


Implementation: how to build system up
1. RPC
2. threads
3. concurrency control - locks

Performance: 
* scalability - 2 x computers -> 2 x throughput
    * Big e-commerce website, when you add more computers, bottle neck move to DB

Fault Tolerance:
1. availability
2. recoverability
    * non-volatile storage(expensive)
    * replication

Consistency
* Put(k,v)
* Get(k)->v

strong: be guaranteed to see most recent updated value(yet expensive communication)
weak: no guarantee to see most recent updated value

MapReduce
```
                Intermediate output
Input 1 -> map  (a:1,b:1) (so the arrow is local operation do not involve network)
Input 2 -> map  (b:1)
Input 3 -> map  (a:1, c:1)

        a -> Reduce -> a,2
        b -> Reduce -> b,2
        c -> Reduce -> c,1
```
The whole process is called a job, compose of tasks.
The example showed above for word count, Map function would look like Map(k,v). k is the file name usually could be ignored, v is the content of input file

Reduce(k,v) k is vector of all values that map produced associated with that key, key is a word and v is all ones, so len(v) will be number of word or key
```
Map(k,v)
    split v into words
    for each word w
        emit(w,"1")

Reduce(k,v)
    emit(len(v))
```  

Real life MapReduce
big collection of servers and a single master server organize the whole computation.
master tell worker server 7 to read certain file, worker read input and run map function and emit, produce the files on the local disk, accumulating all keys and values produced by the maps run on that worker. workers then arrange to move data to where it's going to be needed for the reduces. Reduce worker need talk to every single other of the thousand servers and tell them im gonna run the reduce for key "A" and ask workers to look at intermediate map output stored in your local disk and fish out all the instances of key "A" and send them over the network to the reduce worker. Once reduce workers collect all data it can call reduce function. Reduce function will call reduce emit, emit will write the output to a file in a cluster file service that Google uses.

Input and output are files stored in GFS. GFS would automatically splits up any big file you store on it across lots of servers and 64 megabytes chunks. 

So map workers can read data in parallel from thousand GFS file servers.

Run GFS servers and the MapReduce workers on the same set of machines. When master was splitting up the map work and farming it out to different workers it would cleverly when it was about to run the map that was going to read from input file X it would figure out from GFS which server actually holds input file X on its local disk and it would send the map for that input file to the MapReduce software on the same machine.

Data from Map workers to Reduce workers need network and this movement is called shuffle. shuffle phase is responsible for transferring and sorting the output from the map tasks before feeding it to the reduce tasks: 
1. Partitioning: The output from each map task is partitioned based on the key values. All key-value pairs with the same key are assigned to the same partition. This ensures that all values associated with a particular key are processed by the same reducer.
2. Sorting: Within each partition, the key-value pairs are sorted based on the key values. This sorting is necessary because the reduce task expects all values for a particular key to be grouped together.
3. Transfer: The partitioned and sorted data is transferred from the map tasks to the appropriate reduce tasks. Each reduce task receives a partition of the data based on the partitioning scheme.