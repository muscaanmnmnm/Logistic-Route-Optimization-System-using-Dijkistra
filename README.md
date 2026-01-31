# Logistics Route Optimization System

**Course:** CSC-200L Data Structures and Algorithms
**Institution:** Namal University Mianwali (Department of Electrical Engineering)
**Authors:** Muskan Aman Khan & Sana Azeem

## 📌 Project Overview
The **Logistics Route Optimization System** is a desktop-based Graphical User Interface (GUI) application designed to optimize delivery routes in logistics networks. By modeling cities and warehouses as a weighted graph, the system calculates the most efficient paths based on **Distance**, **Time**, or **Cost**.

This tool addresses the complexity of modern logistics by replacing manual intuition with algorithmic precision, allowing for dynamic network adjustments and visual route planning.

## 🚀 Key Features
* **Optimal Pathfinding:** Calculates the shortest route between a source and destination using **Dijkstra’s Algorithm**.
* **Multi-Criteria Optimization:** Users can optimize routes based on three distinct weights:
    * Distance (km)
    * Time of Travel (minutes)
    * Operational Cost ($)
* **Multi-Stop Routing:** Supports route planning for multiple delivery stops using a **Nearest Neighbor Heuristic**.
* **Dynamic Network Management:** Users can add or remove locations (nodes) and routes (edges) in real-time.
* **Interactive Visualization:** Visualizes the network graph with color-coded paths (Green=Start, Red=End, Orange=Intermediate).

## 🛠️ Tech Stack
* **Language:** Python 3
* **GUI Framework:** Tkinter
* **Data Modeling:** NetworkX (Graph/Adjacency List)
* **Visualization:** Matplotlib
* **Algorithms:** Dijkstra's Algorithm, Greedy Best-First Search

## ⚙️ Algorithms & Data Structures
This project demonstrates the practical application of several core data structures:
* **Graph (Adjacency List):** Stores the network topology (Locations and Routes).
* **Priority Queue (Min-Heap):** Used efficiently within Dijkstra's algorithm for vertex selection.
* **Hash Maps:** Used to track distances and visited nodes.
* **Sets:** Used to manage visited nodes during path computation.

## 📸 Screenshots
*(You can upload the screenshot from Figure 1 in your report here)*

## 📦 How to Run
1.  **Clone the repository:**
    ```bash
    git clone [https://github.com/your-username/logistics-optimizer.git](https://github.com/your-username/logistics-optimizer.git)
    ```
2.  **Install dependencies:**
    ```bash
    pip install networkx matplotlib
    ```
3.  **Run the Application:**
    ```bash
    python main.py
    ```
    *(Replace `main.py` with your actual script name)*
