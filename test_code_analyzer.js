/**
 * Test file for code-analyzer.py - JavaScript version
 * This file contains a mix of good and bad code patterns for testing
 */

// Import statements
import React from 'react';
import { useState, useEffect } from 'react';
import axios from 'axios';

// Global variables - not always ideal practice
const API_URL = 'https://api.example.com/data';
let counter = 0;

/**
 * A well-documented utility function that follows best practices
 * @param {Array} numbers - Array of numbers to process
 * @param {Object} options - Configuration options
 * @param {boolean} options.ascending - Sort direction
 * @returns {Array} Processed array of numbers
 */
function processNumbers(numbers, options = { ascending: true }) {
  if (!Array.isArray(numbers)) {
    throw new Error('Input must be an array of numbers');
  }
  
  // Make a copy to avoid mutating the input
  const result = [...numbers];
  
  // Sort the array
  result.sort((a, b) => {
    return options.ascending ? a - b : b - a;
  });
  
  // Filter out non-positive numbers
  return result.filter(num => num > 0);
}

// Poorly named function with no documentation
function doStuff(x, y) {
  var z = x + y;
  if(z > 10) {
    return z * 2;
  } else {
    return z / 2;
  }
}

/**
 * A well-structured class following proper naming conventions
 */
class DataProcessor {
  /**
   * Create a new DataProcessor
   * @param {Object} config - Configuration object
   */
  constructor(config) {
    this.config = config;
    this.data = [];
    this.isProcessing = false;
  }
  
  /**
   * Load data from a source
   * @param {string} source - Data source identifier
   * @returns {Promise} Promise resolving to the loaded data
   */
  async loadData(source) {
    try {
      this.isProcessing = true;
      const response = await axios.get(`${API_URL}/${source}`);
      this.data = response.data;
      return this.data;
    } catch (error) {
      console.error('Failed to load data:', error);
      throw error;
    } finally {
      this.isProcessing = false;
    }
  }
  
  /**
   * Process the loaded data
   * @param {Function} transformFn - Data transformation function
   * @returns {Array} Processed data
   */
  processData(transformFn) {
    return this.data.map(transformFn);
  }
}

// Poorly structured class with bad naming
class badClass {
  constructor(stuff) {
    this.stuff = stuff;
  }
  
  // No documentation
  do_something() {
    var result = [];
    for(var i = 0; i < this.stuff.length; i++) {
      if(this.stuff[i] > 10) {
        result.push(this.stuff[i] * 2);
      } else {
        result.push(this.stuff[i]);
      }
    }
    return result;
  }
  
  // Inconsistent method naming style
  calculate_average() {
    var sum = 0;
    for(var i = 0; i < this.stuff.length; i++) {
      sum += this.stuff[i];
    }
    return sum / this.stuff.length;
  }
}

// Function with too many responsibilities and excessive length
function processUserData(userData) {
  // This function does too many things
  
  // Validate input
  if (!userData || typeof userData !== 'object') {
    console.error('Invalid user data');
    return null;
  }
  
  // Process name
  let fullName;
  if (userData.firstName && userData.lastName) {
    fullName = `${userData.firstName} ${userData.lastName}`;
  } else if (userData.firstName) {
    fullName = userData.firstName;
  } else if (userData.lastName) {
    fullName = userData.lastName;
  } else {
    fullName = 'Unknown';
  }
  
  // Process address
  let formattedAddress = '';
  if (userData.address) {
    if (userData.address.street) {
      formattedAddress += userData.address.street;
    }
    
    if (userData.address.city) {
      if (formattedAddress) {
        formattedAddress += ', ';
      }
      formattedAddress += userData.address.city;
    }
    
    if (userData.address.state) {
      if (formattedAddress) {
        formattedAddress += ', ';
      }
      formattedAddress += userData.address.state;
    }
    
    if (userData.address.zip) {
      if (formattedAddress) {
        formattedAddress += ' ';
      }
      formattedAddress += userData.address.zip;
    }
  } else {
    formattedAddress = 'No address provided';
  }
  
  // Calculate age
  let age = null;
  if (userData.birthDate) {
    const birthDate = new Date(userData.birthDate);
    const today = new Date();
    age = today.getFullYear() - birthDate.getFullYear();
    const monthDiff = today.getMonth() - birthDate.getMonth();
    
    if (monthDiff < 0 || (monthDiff === 0 && today.getDate() < birthDate.getDate())) {
      age--;
    }
  }
  
  // Process contact information
  let contacts = [];
  if (userData.email) {
    contacts.push({ type: 'email', value: userData.email });
  }
  
  if (userData.phone) {
    contacts.push({ type: 'phone', value: userData.phone });
  }
  
  if (userData.mobile) {
    contacts.push({ type: 'mobile', value: userData.mobile });
  }
  
  // Create and return processed data
  return {
    name: fullName,
    address: formattedAddress,
    age: age,
    contacts: contacts,
    registrationDate: new Date().toISOString(),
    status: age && age >= 18 ? 'adult' : 'minor',
    id: `user_${Math.floor(Math.random() * 10000)}`
  };
}

// React component with good practices
const UserProfile = ({ userId, onUpdate }) => {
  const [user, setUser] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  
  useEffect(() => {
    const fetchUser = async () => {
      try {
        setLoading(true);
        const response = await axios.get(`${API_URL}/users/${userId}`);
        setUser(response.data);
      } catch (err) {
        setError('Failed to load user data');
        console.error(err);
      } finally {
        setLoading(false);
      }
    };
    
    fetchUser();
  }, [userId]);
  
  const handleNameUpdate = (newName) => {
    setUser(prevUser => ({
      ...prevUser,
      name: newName
    }));
    
    if (onUpdate) {
      onUpdate({ id: userId, name: newName });
    }
  };
  
  if (loading) return <div>Loading...</div>;
  if (error) return <div>Error: {error}</div>;
  if (!user) return <div>No user found</div>;
  
  return (
    <div className="user-profile">
      <h2>{user.name}</h2>
      <div className="user-details">
        <p>Email: {user.email}</p>
        <p>Age: {user.age}</p>
        {user.address && <p>Address: {user.address}</p>}
      </div>
      <button onClick={() => handleNameUpdate(prompt('Enter new name:'))}>
        Update Name
      </button>
    </div>
  );
};

// Poorly formatted React component
function BadComponent(props) {
    const [count,setCount]=useState(0);
    
    // No dependency array in useEffect
    useEffect(() => {
        console.log('Count changed:', count);
    })
    
    function incrementCounter() {
        setCount(count+1);
    }
    
    // Inconsistent indentation and formatting
  return (
    <div>
        <h3>Bad Component</h3>
    <p>Count: {count}</p>
      <button onClick={incrementCounter}>
        Increment
        </button>
    </div>
  );
}

// Function with repetitive code - violates DRY principle
function calculatePrices(products) {
  const results = {};
  
  for (const product of products) {
    if (product.type === 'book') {
      // Calculate book price
      const basePrice = product.price;
      const discount = product.isOnSale ? 0.2 : 0;
      const tax = 0.05;
      const finalPrice = basePrice * (1 - discount) * (1 + tax);
      results[product.id] = finalPrice;
    }
    
    if (product.type === 'electronics') {
      // Calculate electronics price
      const basePrice = product.price;
      const discount = product.isOnSale ? 0.1 : 0;
      const tax = 0.08;
      const finalPrice = basePrice * (1 - discount) * (1 + tax);
      results[product.id] = finalPrice;
    }
    
    if (product.type === 'clothing') {
      // Calculate clothing price
      const basePrice = product.price;
      const discount = product.isOnSale ? 0.15 : 0;
      const tax = 0.06;
      const finalPrice = basePrice * (1 - discount) * (1 + tax);
      results[product.id] = finalPrice;
    }
  }
  
  return results;
}

// Export the components and functions
export {
  processNumbers,
  doStuff,
  DataProcessor,
  badClass,
  processUserData,
  UserProfile,
  BadComponent,
  calculatePrices
};

// Default export
export default UserProfile; 