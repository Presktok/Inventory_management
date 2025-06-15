// API Configuration
const API_BASE_URL = 'http://localhost:5000/api';

// Default fetch options for all API calls
const defaultOptions = {
    headers: {
        'Content-Type': 'application/json',
        'Accept': 'application/json'
    },
    credentials: 'include', // Include cookies in requests
    mode: 'cors' // Enable CORS
};

// Helper function to handle API responses
async function handleResponse(response) {
    if (!response.ok) {
        const error = await response.json().catch(() => ({
            message: `HTTP error! status: ${response.status}`
        }));
        throw new Error(error.message || `HTTP error! status: ${response.status}`);
    }
    const data = await response.json();
    if (data.status === 'error') {
        throw new Error(data.message || 'API request failed');
    }
    return data;
}

// Inventory API functions
const inventoryApi = {
    // Get all inventory items
    getAllItems: async () => {
        try {
            const response = await fetch(`${API_BASE_URL}/inventory`, {
                ...defaultOptions,
                method: 'GET'
            });
            const data = await handleResponse(response);
            return data;
        } catch (error) {
            console.error('Error fetching inventory:', error);
            throw error;
        }
    },

    // Get inventory item by ID
    getById: async (itemId) => {
        try {
            const response = await fetch(`${API_BASE_URL}/inventory/${itemId}`, {
                ...defaultOptions,
                method: 'GET'
            });
            const data = await handleResponse(response);
            return data;
        } catch (error) {
            console.error('Error fetching item by ID:', error);
            throw error;
        }
    },

    // Create new inventory item
    createItem: async (itemData) => {
        try {
            const response = await fetch(`${API_BASE_URL}/inventory`, {
                ...defaultOptions,
                method: 'POST',
                body: JSON.stringify(itemData)
            });
            return handleResponse(response);
        } catch (error) {
            console.error('Error creating item:', error);
            throw error;
        }
    },

    // Update inventory item
    updateItem: async (itemId, itemData) => {
        try {
            const response = await fetch(`${API_BASE_URL}/inventory/${itemId}`, {
                ...defaultOptions,
                method: 'PUT',
                body: JSON.stringify(itemData)
            });
            return handleResponse(response);
        } catch (error) {
            console.error('Error updating item:', error);
            throw error;
        }
    },

    // Delete inventory item
    deleteItem: async (itemId) => {
        try {
            const response = await fetch(`${API_BASE_URL}/inventory/${itemId}`, {
                ...defaultOptions,
                method: 'DELETE'
            });
            return handleResponse(response);
        } catch (error) {
            console.error('Error deleting item:', error);
            throw error;
        }
    }
};

// Order API functions
const orderApi = {
    // Create new order
    createOrder: async (orderData) => {
        try {
            const response = await fetch(`${API_BASE_URL}/orders`, {
                ...defaultOptions,
                method: 'POST',
                body: JSON.stringify(orderData)
            });
            return handleResponse(response);
        } catch (error) {
            console.error('Error creating order:', error);
            throw error;
        }
    },

    // Process orders
    processOrders: async (processData) => {
        try {
            const response = await fetch(`${API_BASE_URL}/orders/process`, {
                ...defaultOptions,
                method: 'POST',
                body: JSON.stringify(processData)
            });
            return handleResponse(response);
        } catch (error) {
            console.error('Error processing orders:', error);
            throw error;
        }
    },

    // Get nearby users
    getNearbyUsers: async (orderId, userId, maxDistance) => {
        try {
            const response = await fetch(
                `${API_BASE_URL}/orders/${orderId}/nearby-users?user_id=${userId}&max_distance=${maxDistance}`,
                {
                    ...defaultOptions,
                    method: 'GET'
                }
            );
            return handleResponse(response);
        } catch (error) {
            console.error('Error getting nearby users:', error);
            throw error;
        }
    },

    // Get all orders
    getAllOrders: async () => {
        try {
            const response = await fetch(`${API_BASE_URL}/orders`, {
                ...defaultOptions,
                method: 'GET'
            });
            const data = await handleResponse(response);
            return data;
        } catch (error) {
            console.error('Error fetching orders:', error);
            throw error;
        }
    }
};

// Export the API objects
window.inventoryApi = inventoryApi;
window.orderApi = orderApi; 