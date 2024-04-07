It is not simpler why ppl are driven to use them?\
1. parallelism - because ppl want to achieve, high performance, parallelism, lots of CPUs, lots of memories, lots of disk arms moving in parallel
2. fault tolerance 
3. physical - bank a computer in NY bank b computer in London
4. security/isolated

Course will focus on 1&2.

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
weak: 