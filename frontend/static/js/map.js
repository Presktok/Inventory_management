// Map initialization
let map;
let routeLayer;
let nodesLayer;
let connectionsLayer;
let currentPath = null;

// Custom marker icons
const markerIcons = {
    Factory: L.divIcon({
        className: 'location-marker factory-marker',
        html: '<i class="fas fa-industry"></i>',
        iconSize: [30, 30],
        iconAnchor: [15, 15]
    }),
    Warehouse: L.divIcon({
        className: 'location-marker warehouse-marker',
        html: '<i class="fas fa-warehouse"></i>',
        iconSize: [30, 30],
        iconAnchor: [15, 15]
    }),
    Junction: L.divIcon({
        className: 'location-marker junction-marker',
        html: '<i class="fas fa-circle"></i>',
        iconSize: [20, 20],
        iconAnchor: [10, 10]
    })
};

// Location data with types, descriptions, and road-based connections
const locations = {
    // Main facilities
    factory1: { 
        name: 'Delhi Factory',
        type: 'Factory',
        coords: [28.6139, 77.2090],
        description: 'Main manufacturing facility',
        connections: ['jaipur_junction', 'agra_junction']
    },
    warehouse1: { 
        name: 'Mumbai Warehouse',
        type: 'Warehouse',
        coords: [19.0760, 72.8777],
        description: 'Primary distribution center',
        connections: ['pune_junction', 'nashik_junction']
    },
    warehouse2: { 
        name: 'Kolkata Warehouse',
        type: 'Warehouse',
        coords: [22.5726, 88.3639],
        description: 'Eastern regional warehouse',
        connections: ['dhanbad_junction', 'kharagpur_junction']
    },

    // Major road junctions and cities (North)
    agra_junction: {
        name: 'Agra Junction',
        type: 'Junction',
        coords: [27.1767, 78.0081],
        description: 'Major intersection near Agra',
        connections: ['factory1', 'gwalior_junction', 'kanpur_junction']
    },
    jaipur_junction: {
        name: 'Jaipur Junction',
        type: 'Junction',
        coords: [26.9124, 75.7873],
        description: 'Major intersection near Jaipur',
        connections: ['factory1', 'ajmer_junction', 'gwalior_junction']
    },
    kanpur_junction: {
        name: 'Kanpur Junction',
        type: 'Junction',
        coords: [26.4499, 80.3319],
        description: 'Major intersection near Kanpur',
        connections: ['agra_junction', 'varanasi_junction', 'nagpur_junction']
    },

    // Central India junctions
    nagpur_junction: {
        name: 'Nagpur Junction',
        type: 'Junction',
        coords: [21.1458, 79.0882],
        description: 'Central India transportation hub',
        connections: ['kanpur_junction', 'raipur_junction', 'pune_junction']
    },
    raipur_junction: {
        name: 'Raipur Junction',
        type: 'Junction',
        coords: [21.2514, 81.6296],
        description: 'Eastern corridor connection',
        connections: ['nagpur_junction', 'kharagpur_junction', 'varanasi_junction']
    },

    // Western route junctions
    pune_junction: {
        name: 'Pune Junction',
        type: 'Junction',
        coords: [18.5204, 73.8567],
        description: 'Western India hub',
        connections: ['warehouse1', 'nagpur_junction', 'hyderabad_junction']
    },
    nashik_junction: {
        name: 'Nashik Junction',
        type: 'Junction',
        coords: [19.9975, 73.7898],
        description: 'Western route connection',
        connections: ['warehouse1', 'pune_junction', 'indore_junction']
    },

    // Eastern route junctions
    varanasi_junction: {
        name: 'Varanasi Junction',
        type: 'Junction',
        coords: [25.3176, 82.9739],
        description: 'Eastern route hub',
        connections: ['kanpur_junction', 'dhanbad_junction', 'raipur_junction']
    },
    dhanbad_junction: {
        name: 'Dhanbad Junction',
        type: 'Junction',
        coords: [23.7957, 86.4304],
        description: 'Eastern industrial corridor',
        connections: ['warehouse2', 'varanasi_junction', 'kharagpur_junction']
    },
    kharagpur_junction: {
        name: 'Kharagpur Junction',
        type: 'Junction',
        coords: [22.3460, 87.2320],
        description: 'Eastern logistics hub',
        connections: ['warehouse2', 'raipur_junction', 'dhanbad_junction']
    },

    // Additional connecting junctions
    gwalior_junction: {
        name: 'Gwalior Junction',
        type: 'Junction',
        coords: [26.2183, 78.1828],
        description: 'Central route connection',
        connections: ['agra_junction', 'jaipur_junction', 'indore_junction']
    },
    indore_junction: {
        name: 'Indore Junction',
        type: 'Junction',
        coords: [22.7196, 75.8577],
        description: 'Central India connection',
        connections: ['gwalior_junction', 'nashik_junction', 'hyderabad_junction']
    },
    hyderabad_junction: {
        name: 'Hyderabad Junction',
        type: 'Junction',
        coords: [17.3850, 78.4867],
        description: 'Southern route connection',
        connections: ['pune_junction', 'indore_junction']
    },
    ajmer_junction: {
        name: 'Ajmer Junction',
        type: 'Junction',
        coords: [26.4499, 74.6399],
        description: 'Northwestern connection',
        connections: ['jaipur_junction']
    }
};

// Add CSS for junction markers
const style = document.createElement('style');
style.textContent = `
    .junction-marker {
        background: #FFA000;
        color: white;
        font-size: 12px;
        border: 2px solid white;
        box-shadow: 0 2px 5px rgba(0,0,0,0.2);
    }
    .junction-marker i {
        font-size: 10px;
    }
    .path-node .junction { 
        background: #fff3e0; 
        color: #f57c00; 
    }
    .connection-label {
        background-color: white;
        border: 1px solid #ccc;
        padding: 2px 6px;
        border-radius: 10px;
        font-size: 11px;
        white-space: nowrap;
        box-shadow: 0 1px 3px rgba(0,0,0,0.2);
    }
`;
document.head.appendChild(style);

function initMap() {
    console.log('Initializing map...');
    // Initialize the map centered on India
    map = L.map('routeMap').setView([22.5726, 78.9629], 5);
    
    // Add OpenStreetMap tiles
    L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
        maxZoom: 19,
        attribution: '© OpenStreetMap contributors'
    }).addTo(map);

    // Add scale control
    L.control.scale().addTo(map);

    // Initialize layers
    routeLayer = L.layerGroup().addTo(map);
    nodesLayer = L.layerGroup().addTo(map);
    connectionsLayer = L.layerGroup().addTo(map);

    console.log('Map initialized, showing nodes and connections...');
    // Show all nodes and connections
    showAllNodesAndConnections();
}

function addNodeInteractions() {
    Object.entries(locations).forEach(([id, location]) => {
        const marker = L.marker(location.coords, {
            icon: markerIcons[location.type]
        })
        .bindPopup(createNodePopup(id, location))
        .on('mouseover', function(e) {
            highlightConnections(id);
            this.openPopup();
        })
        .on('mouseout', function(e) {
            resetConnections();
            this.closePopup();
        });
        
        marker.addTo(nodesLayer);
    });
}

function createNodePopup(id, location) {
    const connections = location.connections.map(connId => 
        `<li>${locations[connId].name} (${calculateDistance(location.coords, locations[connId].coords).toFixed(1)} km)</li>`
    ).join('');

    return `
        <div class="node-popup">
            <h4>${location.name}</h4>
            <p><strong>Type:</strong> ${location.type}</p>
            <p><strong>Description:</strong> ${location.description}</p>
            <p><strong>Connected to:</strong></p>
            <ul>${connections}</ul>
        </div>
    `;
}

function showAllNodesAndConnections() {
    console.log('Showing all nodes and connections...');
    // Clear existing layers
    routeLayer.clearLayers();
    nodesLayer.clearLayers();
    connectionsLayer.clearLayers();

    // Draw all connections first (so they're behind nodes)
    drawAllConnections(false);

    // Add all nodes with interactions
    addNodeInteractions();
}

function drawAllConnections(faded = false) {
    console.log('Drawing connections, faded:', faded);
    Object.entries(locations).forEach(([sourceId, source]) => {
        source.connections.forEach(targetId => {
            if (locations[targetId]) {
                const target = locations[targetId];
                const midPoint = getMidPoint(source.coords, target.coords);
                const distance = calculateDistance(source.coords, target.coords);
                
                // Draw connection line
                const path = L.polyline(
                    [source.coords, target.coords],
                    {
                        color: faded ? '#ddd' : '#888',
                        weight: faded ? 1 : 2,
                        opacity: faded ? 0.3 : 0.6,
                        dashArray: '5, 10'
                    }
                ).addTo(connectionsLayer);

                // Add distance label
                if (!faded) {
                    L.marker(midPoint, {
                        icon: L.divIcon({
                            className: 'connection-label',
                            html: `${distance.toFixed(1)} km`,
                            iconSize: [50, 20],
                            iconAnchor: [25, 10]
                        })
                    }).addTo(connectionsLayer);
                }

                if (!faded) {
                    path.on('mouseover', function() {
                        this.setStyle({
                            color: '#FF5722',
                            weight: 3,
                            opacity: 0.8
                        });
                    }).on('mouseout', function() {
                        this.setStyle({
                            color: '#888',
                            weight: 2,
                            opacity: 0.6
                        });
                    });
                }
            }
        });
    });
}

function getMidPoint(point1, point2) {
    return [
        (point1[0] + point2[0]) / 2,
        (point1[1] + point2[1]) / 2
    ];
}

function highlightConnections(nodeId) {
    connectionsLayer.clearLayers();
    const node = locations[nodeId];
    
    node.connections.forEach(targetId => {
        const target = locations[targetId];
        const midPoint = getMidPoint(node.coords, target.coords);
        const distance = calculateDistance(node.coords, target.coords);

        // Draw highlighted connection
        L.polyline(
            [node.coords, target.coords],
            {
                color: '#FF5722',
                weight: 3,
                opacity: 0.8
            }
        ).addTo(connectionsLayer);

        // Add distance label
        L.marker(midPoint, {
            icon: L.divIcon({
                className: 'connection-label',
                html: `${distance.toFixed(1)} km`,
                iconSize: [50, 20],
                iconAnchor: [25, 10]
            })
        }).addTo(connectionsLayer);
    });
}

function resetConnections() {
    connectionsLayer.clearLayers();
    drawAllConnections(false);
}

function findShortestPath(start, end) {
    console.log('Finding shortest path from', start, 'to', end);
    const distances = {};
    const previous = {};
    const unvisited = new Set();
    
    // Initialize distances
    Object.keys(locations).forEach(node => {
        distances[node] = Infinity;
        previous[node] = null;
        unvisited.add(node);
    });
    distances[start] = 0;

    while (unvisited.size > 0) {
        // Find the unvisited node with minimum distance
        let current = null;
        let minDistance = Infinity;
        unvisited.forEach(node => {
            if (distances[node] < minDistance) {
                minDistance = distances[node];
                current = node;
            }
        });

        if (current === null || current === end) break;

        unvisited.delete(current);

        // Update distances to neighbors
        const currentLocation = locations[current];
        if (currentLocation && currentLocation.connections) {
            currentLocation.connections.forEach(neighbor => {
                if (!unvisited.has(neighbor)) return;
                
                const distance = calculateDistance(
                    currentLocation.coords,
                    locations[neighbor].coords
                );
                const totalDistance = distances[current] + distance;

                if (totalDistance < distances[neighbor]) {
                    distances[neighbor] = totalDistance;
                    previous[neighbor] = current;
                }
            });
        }
    }

    // Reconstruct path
    const path = [];
    let current = end;
    while (current !== null) {
        path.unshift(current);
        current = previous[current];
    }

    console.log('Found path:', path);
    return path.length > 1 ? path : null;
}

function showShortestPath(source, dest) {
    console.log('Showing shortest path from', source, 'to', dest);
    // Clear previous path
    routeLayer.clearLayers();

    // Show all connections in faded style
    drawAllConnections(true);

    // Find the shortest path
    const pathNodes = findShortestPath(source, dest);
    
    if (!pathNodes) {
        console.log('No path found');
        document.getElementById('routeInfo').innerHTML = `
            <strong>No Path Found</strong><br>
            Could not find a path between ${locations[source].name} and ${locations[dest].name}
        `;
        return;
    }

    console.log('Drawing path segments...');
    // Draw the path segments
    const pathCoords = [];
    for (let i = 0; i < pathNodes.length - 1; i++) {
        const currentNode = locations[pathNodes[i]];
        const nextNode = locations[pathNodes[i + 1]];
        
        pathCoords.push(currentNode.coords);
        
        // Draw this segment of the path
        const pathSegment = L.polyline(
            [currentNode.coords, nextNode.coords],
            {
                color: '#FF5722',
                weight: 4,
                opacity: 0.8
            }
        ).addTo(routeLayer);
    }
    pathCoords.push(locations[pathNodes[pathNodes.length - 1]].coords);

    // Fit map to show the entire path
    const bounds = L.latLngBounds(pathCoords);
    map.fitBounds(bounds, { padding: [50, 50] });

    // Calculate total distance
    let totalDistance = 0;
    for (let i = 0; i < pathNodes.length - 1; i++) {
        totalDistance += calculateDistance(
            locations[pathNodes[i]].coords,
            locations[pathNodes[i + 1]].coords
        );
    }

    // Update route info
    document.getElementById('routeInfo').innerHTML = `
        <strong>Shortest Path Found</strong><br>
        From: ${locations[source].name}<br>
        To: ${locations[dest].name}<br>
        Total Distance: ${totalDistance.toFixed(2)} km<br>
        Number of stops: ${pathNodes.length}
    `;

    // Update path details with all stops
    document.getElementById('pathDetails').innerHTML = `
        <h3>Path Details</h3>
        ${pathNodes.map((nodeId, index) => `
            <div class="path-node">
                <span class="node-type ${locations[nodeId].type.toLowerCase()}">${locations[nodeId].type}</span>
                <strong>${locations[nodeId].name}</strong>
                <span>${index === 0 ? 'Start' : index === pathNodes.length - 1 ? 'End' : 'Via'}</span>
            </div>
        `).join('')}
    `;

    // Highlight nodes along the path
    pathNodes.forEach(nodeId => {
        const node = locations[nodeId];
        L.circleMarker(node.coords, {
            color: '#FF5722',
            fillColor: '#FF5722',
            fillOpacity: 0.3,
            radius: 12,
            weight: 2
        }).addTo(routeLayer);
    });
}

function calculateDistance(point1, point2) {
    return map.distance(point1, point2) / 1000; // Convert to kilometers
}

// Initialize map when the page loads
document.addEventListener('DOMContentLoaded', initMap); 