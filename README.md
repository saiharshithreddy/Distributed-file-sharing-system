# Distributed-file-sharing-system

Read the report [link](https://github.com/harshithreddyhr9/Distributed-file-sharing-system/blob/master/Team_Drop.io_CMPE275_Project1_Report.pdf)  


**Requirements:**
grpc
Protobuf
Redis cache
MongoDB

Install grpcio  ``` sudo python -m pip install grpcio```  
Install grpcio  ```python -m pip install grpcio-tools```

The aim of the project is to develop a distributed data storage system. The system consists of multiple heterogeneous clusters; heterogeneous in the sense that each cluster’s choice of internal design is independent of the design choices made by the other clusters. However, since the clusters together form a single service, they need to agree on the mode of communication
with each other.  
A user can opt to use the services of a particular cluster by talking to the cluster’s end-point. Alternatively, the user can use the service through the common endpoint, called the “super node” and supports data of all forms text, structured or images.  

#### Architecture:
The cluster always has a leader node, dynamically elected among its members using RAFT algorithm. The leader takes care of the control plane tasks, which are mainly cluster management and communication with the outside world. Rest of the 3 nodes handle the data plane. They are responsible for handling user data and providing quick access to it.


