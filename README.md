# Coding Challenge – Assignments PC-001 and SA-001

This repository contains two assignments from Intuit Build Challange

---

## 📁 Repository Structure

```
├── assignment-1/ # PC-001: Producer–Consumer concurrency problem
│ ├── src/
│ ├── tests/
│ ├── run.sh
│ └── README.md
│
└── assignment-2/ # SA-001: Sales data analysis using FP pipelines
├── src/
├── tests/
├── data/
├── run.sh
└── README.md
```
## 🧩 Assignment Overview

### **PC-001: Producer–Consumer Pattern (Assignment 1)**  
Implements a classic producer–consumer system demonstrating:
- Thread synchronization  
- Use of condition variables  
- Shared buffer with bounded capacity  
- Graceful shutdown via poison-pill signaling  
- Clean, object-oriented structure (`Producer`, `Consumer`, `SharedBuffer`)  

A runnable demo and comprehensive stress-tested unit suite are included.

---

### **SA-001: Sales Data Analysis Using Functional Programming (Assignment 2)**  
Processes a CSV dataset of sales transactions using functional programming techniques:
- `map`, `filter`, `reduce`, and `groupby` pipelines  
- Functional transformations and aggregations  
- Multiple analyses including:  
  - Total revenue  
  - Revenue by region / category  
  - Revenue by month  
  - Top-N products  
  - Salesperson performance metrics  

Includes a CLI runner, stream-based CSV loader, pretty-printed reports, and unit tests covering all analysis functions.

---

## ▶️ How to Run Each Assignment

Each assignment is fully isolated and contains its own `run.sh`.

### **Assignment 1**
```
cd assignment-1
./run.sh run # Run concurrency demo
./run.sh test # Run unit tests
```

### **Assignment 2**
```
cd assignment-2
./run.sh run # Run sales analyzer report
./run.sh test # Run unit tests
```

## Technologies Used
- Python 3  
- Threading, Condition variables  
- Functional programming utilities (`map`, `filter`, `reduce`, `groupby`)  
- CSV processing  
- `pytest` for testing  
- Shell scripting for local automation  

---

## 📝 Notes
- See `assignment-1/README.md` and `assignment-2/README.md` for details on each implementation.

