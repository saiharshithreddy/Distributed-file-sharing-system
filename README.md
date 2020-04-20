# Distributed-file-sharing-system


## Installation
Install grpcio  ``` sudo python -m pip install grpcio```

Install grpcio  ```python -m pip install grpcio-tools```

```MongoDB``` ```Redis```

## Technologies

1. Language used for the application code – Python
2. gRPC (Both inter-cluster communication and intra-cluster communication)
3. Protobuf as the interface definition language
4. Redis cache – In-memory database
5. MongoDB – Durable database

## Goal
The aim of the project is to develop a distributed data storage system. The system consists of multiple heterogeneous clusters; heterogeneous in the sense that each cluster’s choice of internal design is independent of the design choices made by the other clusters. However, since the clusters together form a single service, they need to agree on the mode of communication
with each other.

A user can opt to use the services of a particular cluster by talking to the cluster’s end-point. Alternatively, the user can use the service through the common endpoint, called the “super node” and supports data of all forms text, structured or images.

## Architecture:
The cluster always has a leader node, dynamically elected among its members using RAFT algorithm. The leader takes care of the control plane tasks, which are mainly cluster management and communication with the outside world. Rest of the 3 nodes handle the data plane. They are responsible for handling user data and providing quick access to it.

![Architecture](images/architecture.png)
### Structure of an internal cluster
1. The cluster always has a leader node which is dynamically elected among its members.
2. The leader takes care of the control plane tasks, which are mainly cluster management and communicating with the outside world.
3. Remaining nodes handle the data plane (user data)

## Design components

### Leader node
1. Performs the task of a load balancer by distributing the requests to the slave nodes.
   * Leader sends health checks to its nodes.
   * Slave nodes respond with alive status and statistics (CPU load, memory usage, disk usage)
2. Data handling: When the file access request is routed to the cluster, the request is handled by the leader. Leader chooses the right node based on the above statistics and routes the file to the node with least load.
3. Maintains metadata (which file is in which node)

### Raft

RAFT is the algorithm we use for leader election. Initially, each node starts out with a timer of random count. Whichever node times out first, increments its term, marks itself as a candidate and starts a leader election and asks for votes from other nodes. The candidate node can vote for itself. When the candidate node receives n/2 + 1 votes (n: No of nodes in the cluster) then the candidate node becomes the leader. Otherwise, re-election occurs. In the event of leader failure, follower nodes do not receive a heartbeat from the leader to reset their timer. The node whose timer runs out first will be become a candidate node and re-election takes place
![](images/raft.png)

### Caching
Frequent file accesses are optimized by the use of in-memory caching. All the nodes support caching, including the leader node, which uses cache for storing the metadata. Redis is used as the in-memory caching database. Any new data is entered in both Redis as well as the general purpose and more durable database MongoDB. During file search and data retrieval, each node first checks in Redis whether the data is available. If not found, it accesses the data residing in MongoDB. The use of cache improved the performance of the system in case of repeated file accesses. Below is a graph showing the latency statistics with and without caching

![](images/caching.png)
### Work stealing
Work Stealing is the task scheduling strategy used within the cluster. When a nodes has no work to do or has capability to do work, it is picked up to do the task and leaving other nodes aside to complete their tasks and in this this way a node "steals" work items from other nodes.

**Cluster Status:** A cluster to store data is selected is based on average of cpu usage of live nodes within cluster, average of memory usage of live nodes within cluster, average of disk usage of live nodes within cluster sent by the leader of the cluster. After the cluster is selected to store data it’s on the cluster’s leader to select node to store.
**Least Busy Server/node**: the leader selects the node whose cpu usage is least at the moment when transfer of file occurs, instead of any random server/node to store the data.

![workstealing](images/workstealing.png)

### Performance Testing

1. Dynamic Leader Election when all nodes are connected. Latency ranges from 30 seconds to 45 seconds
2. Dynamic Leader Election when one or more nodes go down. Latency ranges from 40 seconds to 1 minute
3. Replication of data uploaded by client
4. Availability of data when one or more nodes go down
5. Uploading 5 files each of 500MB to 1GB sizes parallelly to the cluster Individual file upload takes about 10 seconds
