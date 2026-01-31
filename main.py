# -*- coding: utf-8 -*-
"""
Created on Thu Jan 15 22:32:23 2026

@author: Sana Azeem
"""

"""
Logistics Route Optimization System
A desktop GUI application for computing optimal delivery routes using Dijkstra's Algorithm
"""

import tkinter as tk
from tkinter import ttk, messagebox, scrolledtext
import networkx as nx
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
import heapq
from collections import defaultdict
import math

class LogisticsOptimizer:
    def __init__(self, root):
        self.root = root
        self.root.title("🚚 Logistics Route Optimization System")
        self.root.geometry("1400x900")
        self.root.configure(bg='#f0f4f8')
        
        # Graph data structure
        self.graph = nx.Graph()
        self.locations = {}
        self.edge_weights = {}
        
        # Add some sample data
        self.initialize_sample_data()
        
        # Create GUI
        self.create_gui()
        
    def initialize_sample_data(self):
        """Initialize with sample logistics network"""
        sample_locations = {
            'Warehouse': (0.1, 0.5),
            'City_A': (0.3, 0.8),
            'City_B': (0.5, 0.6),
            'City_C': (0.7, 0.9),
            'City_D': (0.6, 0.3),
            'City_E': (0.9, 0.5),
            'Hub_1': (0.4, 0.4),
            'Hub_2': (0.7, 0.6)
        }
        
        sample_edges = [
            ('Warehouse', 'City_A', {'distance': 25, 'time': 30, 'cost': 15}),
            ('Warehouse', 'Hub_1', {'distance': 20, 'time': 25, 'cost': 12}),
            ('City_A', 'City_B', {'distance': 18, 'time': 22, 'cost': 10}),
            ('City_B', 'Hub_1', {'distance': 15, 'time': 18, 'cost': 9}),
            ('City_B', 'City_C', {'distance': 22, 'time': 28, 'cost': 13}),
            ('City_B', 'Hub_2', {'distance': 16, 'time': 20, 'cost': 11}),
            ('City_C', 'Hub_2', {'distance': 12, 'time': 15, 'cost': 8}),
            ('City_C', 'City_E', {'distance': 20, 'time': 24, 'cost': 12}),
            ('Hub_1', 'City_D', {'distance': 14, 'time': 17, 'cost': 9}),
            ('City_D', 'Hub_2', {'distance': 13, 'time': 16, 'cost': 8}),
            ('City_D', 'City_E', {'distance': 19, 'time': 23, 'cost': 11}),
            ('Hub_2', 'City_E', {'distance': 17, 'time': 21, 'cost': 10}),
        ]
        
        for loc, pos in sample_locations.items():
            self.add_location(loc, pos)
        
        for u, v, weights in sample_edges:
            self.add_route(u, v, weights['distance'], weights['time'], weights['cost'])
    
    def add_location(self, name, pos=(0.5, 0.5)):
        """Add a location (node) to the graph"""
        self.graph.add_node(name, pos=pos)
        self.locations[name] = pos
    
    def add_route(self, from_loc, to_loc, distance, time, cost):
        """Add a route (edge) between two locations"""
        self.graph.add_edge(from_loc, to_loc, 
                           distance=distance, 
                           time=time, 
                           cost=cost)
        self.edge_weights[(from_loc, to_loc)] = {
            'distance': distance,
            'time': time,
            'cost': cost
        }
    
    def dijkstra(self, start, end, weight_type='distance'):
        """
        Dijkstra's Algorithm implementation for shortest path
        
        Args:
            start: Starting location
            end: Destination location
            weight_type: 'distance', 'time', or 'cost'
        
        Returns:
            Tuple of (path, total_weight)
        """
        # Priority queue: (weight, current_node, path)
        pq = [(0, start, [start])]
        visited = set()
        distances = {node: float('inf') for node in self.graph.nodes()}
        distances[start] = 0
        
        while pq:
            current_weight, current_node, path = heapq.heappop(pq)
            
            if current_node in visited:
                continue
            
            visited.add(current_node)
            
            if current_node == end:
                return path, current_weight
            
            # Explore neighbors
            for neighbor in self.graph.neighbors(current_node):
                if neighbor not in visited:
                    edge_data = self.graph[current_node][neighbor]
                    weight = edge_data.get(weight_type, 1)
                    new_weight = current_weight + weight
                    
                    if new_weight < distances[neighbor]:
                        distances[neighbor] = new_weight
                        new_path = path + [neighbor]
                        heapq.heappush(pq, (new_weight, neighbor, new_path))
        
        return None, float('inf')
    
    def find_multi_stop_route(self, start, stops, weight_type='distance'):
        """
        Find optimal route visiting multiple stops
        Uses nearest neighbor heuristic
        """
        if not stops:
            return [start], 0
        
        current = start
        unvisited = set(stops)
        route = [start]
        total_weight = 0
        
        while unvisited:
            nearest = None
            min_dist = float('inf')
            best_path = None
            
            for stop in unvisited:
                path, dist = self.dijkstra(current, stop, weight_type)
                if path and dist < min_dist:
                    min_dist = dist
                    nearest = stop
                    best_path = path
            
            if nearest is None:
                break
            
            route.extend(best_path[1:])
            total_weight += min_dist
            current = nearest
            unvisited.remove(nearest)
        
        return route, total_weight
    
    def create_gui(self):
        """Create the main GUI interface"""
        # Main container
        main_frame = tk.Frame(self.root, bg='#f0f4f8')
        main_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Left panel - Controls
        left_panel = tk.Frame(main_frame, bg='white', relief=tk.RAISED, borderwidth=2)
        left_panel.pack(side=tk.LEFT, fill=tk.BOTH, padx=(0, 5))
        
        # Right panel - Visualization
        right_panel = tk.Frame(main_frame, bg='white', relief=tk.RAISED, borderwidth=2)
        right_panel.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True, padx=(5, 0))
        
        self.create_control_panel(left_panel)
        self.create_visualization_panel(right_panel)
    
    def create_control_panel(self, parent):
        """Create control panel with all input widgets"""
        # Title
        title = tk.Label(parent, text="🚚 Route Optimizer", 
                        font=('Arial', 18, 'bold'), bg='white', fg='#2c3e50')
        title.pack(pady=10)
        
        # Notebook for tabs
        notebook = ttk.Notebook(parent)
        notebook.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)
        
        # Tab 1: Route Calculation
        route_frame = tk.Frame(notebook, bg='white')
        notebook.add(route_frame, text='  Find Route  ')
        
        # Tab 2: Network Management
        manage_frame = tk.Frame(notebook, bg='white')
        notebook.add(manage_frame, text='  Manage Network  ')
        
        self.create_route_tab(route_frame)
        self.create_manage_tab(manage_frame)
    
    def create_route_tab(self, parent):
        """Create route finding tab"""
        # Starting location
        tk.Label(parent, text="Starting Location:", bg='white', 
                font=('Arial', 10, 'bold')).pack(pady=(10, 5))
        self.start_var = tk.StringVar()
        self.start_combo = ttk.Combobox(parent, textvariable=self.start_var, 
                                       width=25, state='readonly')
        self.start_combo['values'] = list(self.graph.nodes())
        if self.start_combo['values']:
            self.start_combo.current(0)
        self.start_combo.pack(pady=5)
        
        # Delivery stops
        tk.Label(parent, text="Delivery Stops:", bg='white', 
                font=('Arial', 10, 'bold')).pack(pady=(15, 5))
        
        stops_container = tk.Frame(parent, bg='white')
        stops_container.pack(fill=tk.BOTH, expand=True, pady=5, padx=10)
        
        self.stops_listbox = tk.Listbox(stops_container, selectmode=tk.MULTIPLE,
                                       height=8, font=('Arial', 9))
        self.stops_listbox.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        
        scrollbar = tk.Scrollbar(stops_container)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.stops_listbox.config(yscrollcommand=scrollbar.set)
        scrollbar.config(command=self.stops_listbox.yview)
        
        self.update_stops_list()
        
        # Optimization criterion
        tk.Label(parent, text="Optimize By:", bg='white', 
                font=('Arial', 10, 'bold')).pack(pady=(15, 5))
        self.optimize_var = tk.StringVar(value='distance')
        
        criteria_frame = tk.Frame(parent, bg='white')
        criteria_frame.pack(pady=5)
        
        tk.Radiobutton(criteria_frame, text="Distance (km)", variable=self.optimize_var,
                      value='distance', bg='white', font=('Arial', 9)).pack(anchor=tk.W)
        tk.Radiobutton(criteria_frame, text="Time (min)", variable=self.optimize_var,
                      value='time', bg='white', font=('Arial', 9)).pack(anchor=tk.W)
        tk.Radiobutton(criteria_frame, text="Cost ($)", variable=self.optimize_var,
                      value='cost', bg='white', font=('Arial', 9)).pack(anchor=tk.W)
        
        # Calculate button
        calc_btn = tk.Button(parent, text="🔍 Calculate Optimal Route",
                           command=self.calculate_route,
                           bg='#3498db', fg='white', font=('Arial', 11, 'bold'),
                           relief=tk.RAISED, borderwidth=3, cursor='hand2')
        calc_btn.pack(pady=20, padx=20, fill=tk.X)
        
        # Results display
        tk.Label(parent, text="Route Summary:", bg='white', 
                font=('Arial', 10, 'bold')).pack(pady=(10, 5))
        
        self.result_text = scrolledtext.ScrolledText(parent, height=10, width=30,
                                                    font=('Courier', 9), wrap=tk.WORD)
        self.result_text.pack(pady=5, padx=10, fill=tk.BOTH, expand=True)
    
    def create_manage_tab(self, parent):
        """Create network management tab"""
        # Add Location section
        loc_frame = tk.LabelFrame(parent, text="Add Location", bg='white',
                                 font=('Arial', 10, 'bold'), padx=10, pady=10)
        loc_frame.pack(fill=tk.X, padx=10, pady=10)
        
        tk.Label(loc_frame, text="Name:", bg='white').grid(row=0, column=0, sticky=tk.W, pady=5)
        self.new_loc_name = tk.Entry(loc_frame, width=20)
        self.new_loc_name.grid(row=0, column=1, pady=5, padx=5)
        
        tk.Button(loc_frame, text="➕ Add Location", command=self.add_new_location,
                 bg='#27ae60', fg='white', font=('Arial', 9, 'bold')).grid(
                     row=0, column=2, padx=5)
        
        # Add Route section
        route_frame = tk.LabelFrame(parent, text="Add Route", bg='white',
                                   font=('Arial', 10, 'bold'), padx=10, pady=10)
        route_frame.pack(fill=tk.X, padx=10, pady=10)
        
        tk.Label(route_frame, text="From:", bg='white').grid(row=0, column=0, sticky=tk.W, pady=5)
        self.from_loc = ttk.Combobox(route_frame, width=15, state='readonly')
        self.from_loc['values'] = list(self.graph.nodes())
        self.from_loc.grid(row=0, column=1, pady=5, padx=5)
        
        tk.Label(route_frame, text="To:", bg='white').grid(row=1, column=0, sticky=tk.W, pady=5)
        self.to_loc = ttk.Combobox(route_frame, width=15, state='readonly')
        self.to_loc['values'] = list(self.graph.nodes())
        self.to_loc.grid(row=1, column=1, pady=5, padx=5)
        
        tk.Label(route_frame, text="Distance (km):", bg='white').grid(row=2, column=0, sticky=tk.W, pady=5)
        self.distance_entry = tk.Entry(route_frame, width=10)
        self.distance_entry.grid(row=2, column=1, sticky=tk.W, pady=5, padx=5)
        
        tk.Label(route_frame, text="Time (min):", bg='white').grid(row=3, column=0, sticky=tk.W, pady=5)
        self.time_entry = tk.Entry(route_frame, width=10)
        self.time_entry.grid(row=3, column=1, sticky=tk.W, pady=5, padx=5)
        
        tk.Label(route_frame, text="Cost ($):", bg='white').grid(row=4, column=0, sticky=tk.W, pady=5)
        self.cost_entry = tk.Entry(route_frame, width=10)
        self.cost_entry.grid(row=4, column=1, sticky=tk.W, pady=5, padx=5)
        
        tk.Button(route_frame, text="➕ Add Route", command=self.add_new_route,
                 bg='#27ae60', fg='white', font=('Arial', 9, 'bold')).grid(
                     row=5, column=0, columnspan=2, pady=10)
        
        # Remove Location section
        remove_frame = tk.LabelFrame(parent, text="Remove Location", bg='white',
                                    font=('Arial', 10, 'bold'), padx=10, pady=10)
        remove_frame.pack(fill=tk.X, padx=10, pady=10)
        
        self.remove_loc = ttk.Combobox(remove_frame, width=20, state='readonly')
        self.remove_loc['values'] = list(self.graph.nodes())
        self.remove_loc.pack(side=tk.LEFT, padx=5)
        
        tk.Button(remove_frame, text="🗑️ Remove", command=self.remove_location,
                 bg='#e74c3c', fg='white', font=('Arial', 9, 'bold')).pack(
                     side=tk.LEFT, padx=5)
    
    def create_visualization_panel(self, parent):
        """Create network visualization panel"""
        # Title
        title = tk.Label(parent, text="📊 Network Visualization", 
                        font=('Arial', 16, 'bold'), bg='white', fg='#2c3e50')
        title.pack(pady=10)
        
        # Create matplotlib figure
        self.fig = Figure(figsize=(10, 8), facecolor='white')
        self.ax = self.fig.add_subplot(111)
        
        # Create canvas
        self.canvas = FigureCanvasTkAgg(self.fig, parent)
        self.canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Initial draw
        self.draw_network()
    
    def draw_network(self, highlight_path=None):
        """Draw the network graph"""
        self.ax.clear()
        
        if len(self.graph.nodes()) == 0:
            self.ax.text(0.5, 0.5, 'No locations in network', 
                        ha='center', va='center', fontsize=14)
            self.canvas.draw()
            return
        
        # Get positions
        pos = nx.get_node_attributes(self.graph, 'pos')
        
        # Draw all edges
        nx.draw_networkx_edges(self.graph, pos, ax=self.ax, 
                              edge_color='#bdc3c7', width=2, alpha=0.6)
        
        # Highlight optimal path if provided
        if highlight_path and len(highlight_path) > 1:
            path_edges = [(highlight_path[i], highlight_path[i+1]) 
                         for i in range(len(highlight_path)-1)]
            nx.draw_networkx_edges(self.graph, pos, edgelist=path_edges,
                                  ax=self.ax, edge_color='#e74c3c', 
                                  width=4, alpha=0.9)
        
        # Draw nodes
        # Draw nodes with proper coloring
        node_colors = []
        for node in self.graph.nodes():
            if highlight_path:
                if node == highlight_path[0]:
                    node_colors.append('#27ae60')  # Green for start
                elif node == highlight_path[-1]:
                        node_colors.append('#e74c3c')  # Red for end
                elif node in highlight_path:
                    node_colors.append('#f39c12')  # Orange for intermediate
                else:
                    node_colors.append('#3498db')  # Blue for others
            else:
                node_colors.append('#3498db')  # Default blue for all nodes
       
        
        
        nx.draw_networkx_nodes(self.graph, pos, ax=self.ax, 
                              node_color=node_colors, node_size=800, alpha=0.9)
        
        # Draw labels
        nx.draw_networkx_labels(self.graph, pos, ax=self.ax, 
                               font_size=9, font_weight='bold')
        
        # Draw edge labels (distance)
        edge_labels = {}
        for u, v, data in self.graph.edges(data=True):
            edge_labels[(u, v)] = f"{data['distance']:.0f}km"
        
        nx.draw_networkx_edge_labels(self.graph, pos, edge_labels, 
                                     ax=self.ax, font_size=8)
        
        self.ax.set_xlim(-0.1, 1.1)
        self.ax.set_ylim(-0.1, 1.1)
        self.ax.axis('off')
        self.ax.set_title('Delivery Network Graph', fontsize=14, fontweight='bold')
        
        self.canvas.draw()
    
    def update_stops_list(self):
        """Update the delivery stops listbox"""
        self.stops_listbox.delete(0, tk.END)
        for node in self.graph.nodes():
            self.stops_listbox.insert(tk.END, node)
    
    def calculate_route(self):
        """Calculate optimal route based on selections"""
        start = self.start_var.get()
        if not start:
            messagebox.showwarning("Warning", "Please select a starting location!")
            return
        
        # Get selected stops
        selected_indices = self.stops_listbox.curselection()
        stops = [self.stops_listbox.get(i) for i in selected_indices]
        
        # Remove start from stops if present
        stops = [s for s in stops if s != start]
        
        if not stops:
            messagebox.showwarning("Warning", "Please select at least one delivery stop!")
            return
        
        weight_type = self.optimize_var.get()
        
        # Calculate route
        route, total_weight = self.find_multi_stop_route(start, stops, weight_type)
        
        # Calculate all metrics for the route
        total_distance = 0
        total_time = 0
        total_cost = 0
        
        for i in range(len(route) - 1):
            u, v = route[i], route[i+1]
            if self.graph.has_edge(u, v):
                edge = self.graph[u][v]
                total_distance += edge.get('distance', 0)
                total_time += edge.get('time', 0)
                total_cost += edge.get('cost', 0)
        
        # Display results
        self.result_text.delete(1.0, tk.END)
        self.result_text.insert(tk.END, "=" * 35 + "\n")
        self.result_text.insert(tk.END, "  OPTIMAL ROUTE CALCULATION\n")
        self.result_text.insert(tk.END, "=" * 35 + "\n\n")
        
        self.result_text.insert(tk.END, f"Optimization: {weight_type.upper()}\n\n")
        
        self.result_text.insert(tk.END, "Route Path:\n")
        for i, loc in enumerate(route, 1):
            self.result_text.insert(tk.END, f"  {i}. {loc}\n")
        
        self.result_text.insert(tk.END, f"\n{'─' * 35}\n")
        self.result_text.insert(tk.END, "SUMMARY:\n")
        self.result_text.insert(tk.END, f"{'─' * 35}\n")
        self.result_text.insert(tk.END, f"Total Distance: {total_distance:.1f} km\n")
        self.result_text.insert(tk.END, f"Total Time:     {total_time:.0f} min\n")
        self.result_text.insert(tk.END, f"Total Cost:     ${total_cost:.2f}\n")
        self.result_text.insert(tk.END, f"Stops Visited:  {len(stops)}\n")
        self.result_text.insert(tk.END, "=" * 35 + "\n")
        
        # Highlight route on graph
        self.draw_network(highlight_path=route)
    
    def add_new_location(self):
        """Add a new location to the network"""
        name = self.new_loc_name.get().strip()
        if not name:
            messagebox.showwarning("Warning", "Please enter a location name!")
            return
        
        if name in self.graph.nodes():
            messagebox.showwarning("Warning", "Location already exists!")
            return
        
        # Random position for new location
        import random
        pos = (random.uniform(0.1, 0.9), random.uniform(0.1, 0.9))
        
        self.add_location(name, pos)
        self.update_all_combos()
        self.draw_network()
        self.new_loc_name.delete(0, tk.END)
        
        messagebox.showinfo("Success", f"Location '{name}' added successfully!")
    
    def add_new_route(self):
        """Add a new route to the network"""
        from_loc = self.from_loc.get()
        to_loc = self.to_loc.get()
        
        if not from_loc or not to_loc:
            messagebox.showwarning("Warning", "Please select both locations!")
            return
        
        if from_loc == to_loc:
            messagebox.showwarning("Warning", "Cannot create route to same location!")
            return
        
        try:
            distance = float(self.distance_entry.get())
            time = float(self.time_entry.get())
            cost = float(self.cost_entry.get())
        except ValueError:
            messagebox.showwarning("Warning", "Please enter valid numbers for distance, time, and cost!")
            return
        
        self.add_route(from_loc, to_loc, distance, time, cost)
        self.draw_network()
        
        # Clear entries
        self.distance_entry.delete(0, tk.END)
        self.time_entry.delete(0, tk.END)
        self.cost_entry.delete(0, tk.END)
        
        messagebox.showinfo("Success", f"Route added: {from_loc} ↔ {to_loc}")
    
    def remove_location(self):
        """Remove a location from the network"""
        loc = self.remove_loc.get()
        if not loc:
            messagebox.showwarning("Warning", "Please select a location to remove!")
            return
        
        if messagebox.askyesno("Confirm", f"Remove '{loc}' and all connected routes?"):
            self.graph.remove_node(loc)
            if loc in self.locations:
                del self.locations[loc]
            
            self.update_all_combos()
            self.draw_network()
            
            messagebox.showinfo("Success", f"Location '{loc}' removed!")
    
    def update_all_combos(self):
        """Update all comboboxes with current nodes"""
        nodes = list(self.graph.nodes())
        
        self.start_combo['values'] = nodes
        self.from_loc['values'] = nodes
        self.to_loc['values'] = nodes
        self.remove_loc['values'] = nodes
        
        self.update_stops_list()


# Run the application
if __name__ == "__main__":
    root = tk.Tk()
    app = LogisticsOptimizer(root)
    root.mainloop()