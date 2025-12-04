# ✈️ microservices-registry

A microservices architecture project for CS4471 — Software Architecture

Welcome to our project repository! This system implements a **custom-built service registry** and a suite of **independent microservices**, all containerized with Docker and orchestrated locally. Built with industry best practices and #grindset.

This README includes setup instructions, an overview of the project, and architecture documentation.

---

## 🚀 Quick Start
#### 1️⃣ Start Docker

Make sure Docker Desktop is running.

#### 2️⃣ Open Two Terminals

* Terminal A → Registry:
```bash
cd registry
```

* Terminal B → Template Microservice:
```bash
cd microservices/<select_service>
```
#### 3️⃣ Build & Run with Docker Compose

Run these in the Terminal A, then B (linearly):
```bash
docker-compose up --build
```

This builds and starts the registry + the microservice containers.
You should now see them running inside Docker Desktop → Containers.

#### 4️⃣ Access the MySQL Database (Optional)

If you want to inspect or interact with the database:

- Open Docker Desktop → Containers
- Expand the registry stack
- Find db container → click the ellipsis → Open in Terminal
- Run:
    ```bash
    mysql -u root -p
    ```
    > Password: group4

You're now in the SQL terminal and can inspect the registry + service DB tables.

#### 5️⃣ Microservice URLs

🔧 Service Registry	http://35.183.109.248:7993/

🛩️ Flight Search [Live](https://fl-de3f8a0e6af748038ef355972a20521b.ecs.us-east-1.on.aws/) (Localhost:8081)

🔍 Live Flight Tracking [Live](https://li-40b92eb981954e4581668dc1cc36b298.ecs.us-east-1.on.aws/) (Localhost:8084)

💱 Currency Converter [Live](https://cu-a0042894c410436ab2c094d13df074cb.ecs.us-east-1.on.aws/) (Localhost:8443)

🌦️ Airport Weather Forecast [Live](https://we-af8b7e20f67648cead41df4e07c514bc.ecs.us-east-1.on.aws/) (Localhost:8088)

🏝️ Destination Wishlist [Live](https://de-d997e67f7e56494381db18389e1de654.ecs.us-east-1.on.aws/) (Localhost:5002)

---

### Project Overview
This project was created for CS4471: Software Architecture. Our goal was to design and implement a complete microservices ecosystem from scratch, including:
- a custom-built service registry
- multiple independent microservices
- containerization + orchestration
- cloud deployment considerations
- architectural documentation (context, quality, structure, & more)

<br>

🗂️ Implemented Microservices
\> S1   Flight Search Service	🛩️
\> S2	Live Flight Tracking Service	🔍👀
\> S4	Currency Converter Service	💱
\> S5	Airport Weather Forecast Service	🌦️
\> S8	Destination Wishlist Service	🏝️

More details (API endpoints, workflows, etc.) will be added once all services are finalized.

> [S3, S6, S7] were dropped due to time constraints.

---

### 🛠️ Tech Stack

We used a modern industry-aligned toolset to build and orchestrate the system:

* **Docker** — Containerization
* **MySQL** — Persistent service registry + microservice data
* **AWS** — Cloud hosting & infrastructure (future deployment path)
* **Python (Flask)** — Microservice development
* **React** — Frontend for interacting with services
* **Git** — Version control

We also implemented techniques such as:
* **Load Balancing**,
* **Microservice Health Checks**,
* **Microservice Discovery**,
* *Redis Cache (WIP)*
* ...

---

### 📚 Architecture & Documentation 

We’ve produced the following documentation (to be added to the repo soon):

**Context Model**

![plot](./system%20diagrams/ContextModel.png)

**Cloud Provider Topology**

![plot](./system%20diagrams/CloudProviderTopology.png)

**Component & Connector View**

![plot](./system%20diagrams/Component&Connector.png)

**Progress Report 1 Presentation** ([link](https://docs.google.com/presentation/d/1vAZWEF2lelkwSzCr29qFf9iV2MIH415dUiA6GrElisE/edit?usp=sharing))

**Progress Report 2 Presentation** ([link](https://docs.google.com/presentation/d/1W_QkgMWos6S_lUP6HcFW8jcfWjvJ-DfM/edit?usp=sharing&ouid=115699878098283755598&rtpof=true&sd=true))


---

#### Made with ❤️

**Group 4** — Software Architecture, Western University
```json
team = [
    Naseer Rehman (Liason),
    Muhammad Imran Asghar,
    Galen Meesters,
    Devarshi Patel,
    Tyler Larson
]
```