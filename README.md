# **🚀 Scalable Finder Service Backend System**

This repository contains the backend system for the Finder Service platform. It leverages **Redis Cluster** for high availability, **Daphne** for WebSocket handling, and **Nginx** as a reverse proxy. The architecture is designed for scalability and high performance. 

---

## **📖 Table of Contents**

1. [About the System](#about-the-system)  
2. [Key Features](#key-features)  
3. [Tech Stack](#tech-stack)  
4. [System Architecture](#system-architecture)  
5. [Setup Instructions](#setup-instructions)  
   - Redis Cluster  
   - Nginx WebSocket Proxy  
   - Daphne ASGI Server  
6. [Testing and Validation](#testing-and-validation)  
7. [Future Improvements](#future-improvements)  

---

## **🔍 About the System**

The Finder Service platform connects businesses with financial professionals (e.g., accountants, CFOs, revenue specialists). The backend system is designed to handle high volumes of traffic while ensuring real-time communication between users.

Key components:
- **Redis Cluster**: Sharded and highly available in-memory store.  
- **Daphne**: ASGI server for handling WebSocket connections.  
- **Nginx**: Reverse proxy and WebSocket traffic balancer.  

---

## **✨ Key Features**

- **Scalable Redis Cluster** for real-time caching and pub/sub.  
- **WebSocket Communication** for real-time notifications.  
- **Load Balancing with Nginx** to ensure smooth traffic flow.  
- **High Availability** with fault tolerance in Redis and WebSocket handling.  

---

## **🛠 Tech Stack**

- **Programming Language**: Python 🐍  
- **Framework**: Django + Django Channels 🌐 , Nextjs 
- **WebSocket Server**: Daphne 💬  
- **Reverse Proxy & Load Balancer**: Nginx 📡  
- **In-Memory Data Store**: Redis 🧠  
- **Containerization**: Docker 🐳  
- **Search**: ElasticSearch
- **MessageBroker**: RabbitMQ

---

## **📐 System Architecture**

The system is designed to handle both HTTP and WebSocket traffic efficiently.

1. **Nginx**  
   - Acts as a reverse proxy for HTTP requests to the Django application.  
   - Handles WebSocket traffic and forwards it to Daphne.  
   - Load balances across multiple Daphne instances.  

2. **Daphne**  
   - ASGI server to handle WebSocket connections.  
   - Communicates with Django Channels for real-time events.  

3. **Redis Cluster**  
   - Used for caching and as a pub/sub broker for WebSocket communication.  
   - High availability with sharded nodes and replicas.  

---

## **⚙️ Setup Instructions**

### **1. Deploy Redis Cluster (🧠)**

1. Install Redis on all nodes:
   ```bash
   sudo apt update
   sudo apt install redis
   ```

2. Configure Redis for clustering:  
   Update `/etc/redis/redis.conf`:
   ```conf
   cluster-enabled yes
   cluster-config-file nodes.conf
   cluster-node-timeout 5000
   appendonly yes
   bind 0.0.0.0
   ```

3. Start Redis:
   ```bash
   sudo systemctl start redis
   ```

4. Create the cluster:
   ```bash
   redis-cli --cluster create \
   <node1_ip>:6379 <node2_ip>:6379 <node3_ip>:6379 \
   <node4_ip>:6379 <node5_ip>:6379 <node6_ip>:6379 \
   --cluster-replicas 1
   ```

5. Verify the cluster:
   ```bash
   redis-cli -c
   > CLUSTER INFO
   > CLUSTER NODES
   ```

---

### **2. Configure Nginx for WebSocket Proxy (📡)**

1. Install Nginx:
   ```bash
   sudo apt update
   sudo apt install nginx
   ```

2. Add WebSocket proxy configuration:
   Update `/etc/nginx/sites-available/default`:
   ```conf
   server {
       listen 80;
       server_name your-domain.com;

       location /ws/ {
           proxy_pass http://127.0.0.1:8001; # Daphne
           proxy_http_version 1.1;
           proxy_set_header Upgrade $http_upgrade;
           proxy_set_header Connection "upgrade";
           proxy_set_header Host $host;
           proxy_cache_bypass $http_upgrade;
       }

       location / {
           proxy_pass http://127.0.0.1:8000; # Django
       }
   }
   ```

3. Restart Nginx:
   ```bash
   sudo systemctl restart nginx
   ```

---

### **3. Deploy Daphne for WebSocket Handling (💬)**

1. Install Daphne:
   ```bash
   pip install daphne
   ```

2. Run Daphne:
   ```bash
   daphne -b 0.0.0.0 -p 8001 finder_service.asgi:application
   ```

3. Create a systemd service for Daphne:
   ```bash
   sudo nano /etc/systemd/system/daphne.service
   ```

   Add:
   ```ini
   [Unit]
   Description=Daphne WebSocket Server
   After=network.target

   [Service]
   User=your_user
   Group=your_group
   WorkingDirectory=/path/to/project
   ExecStart=/path/to/venv/bin/daphne -b 0.0.0.0 -p 8001 finder_service.asgi:application
   Restart=always

   [Install]
   WantedBy=multi-user.target
   ```

4. Start Daphne:
   ```bash
   sudo systemctl start daphne
   sudo systemctl enable daphne
   ```

---

## **🧪 Testing and Validation**

1. Test WebSocket connections:
   - Use tools like [WebSocket King](https://websocketking.com/) to test the `/ws/` endpoint.  

2. Verify Redis Cluster:
   - Run the following command on any Redis node:
     ```bash
     redis-cli -c
     > CLUSTER INFO
     ```

3. Check logs:
   - For Nginx: `/var/log/nginx/access.log` and `/var/log/nginx/error.log`.  
   - For Daphne: `/path/to/project/logs/daphne.log`.  

---

## **🌟 Future Improvements**

- **Horizontal Scaling**: Add more Redis nodes or Daphne instances as traffic grows.  
- **Monitoring**: Use tools like **Prometheus** and **Grafana** for monitoring Redis and WebSocket performance.  
- **CI/CD Integration**: Automate deployments with Docker Compose and Kubernetes.  

---

## **🎉 Conclusion**

This scalable backend system ensures high availability and optimal performance for the Finder Service platform. 🚀 With Redis Cluster for real-time data, Nginx for efficient traffic handling, and Daphne for WebSocket connections, the system is ready for production-level demands.

---

Feel free to contribute to this project or report any issues! 🙌  
For any questions, contact us at **support@finder-service.com**. 😊

--- 

Enjoy building your scalable Finder Service! 🎉