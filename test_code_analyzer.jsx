import React, { useState, useEffect, useCallback, useMemo } from 'react';
import PropTypes from 'prop-types';
import axios from 'axios';
import './styles.css';

// Constants
const API_BASE_URL = 'https://api.example.com';
const DEFAULT_LIMIT = 10;

/**
 * A well-structured and documented React component
 * @param {Object} props - Component props
 * @returns {JSX.Element} Rendered component
 */
const TaskList = ({ userId, initialFilter }) => {
  // State management
  const [tasks, setTasks] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const [filter, setFilter] = useState(initialFilter || 'all');
  const [page, setPage] = useState(1);
  
  // Fetch tasks from API
  useEffect(() => {
    const fetchTasks = async () => {
      try {
        setLoading(true);
        const response = await axios.get(
          `${API_BASE_URL}/users/${userId}/tasks`,
          {
            params: {
              filter,
              page,
              limit: DEFAULT_LIMIT
            }
          }
        );
        
        setTasks(response.data.tasks);
        setError(null);
      } catch (err) {
        console.error('Failed to fetch tasks:', err);
        setError('Failed to load tasks. Please try again later.');
      } finally {
        setLoading(false);
      }
    };
    
    fetchTasks();
  }, [userId, filter, page]);
  
  // Memoized filtered tasks
  const filteredTasks = useMemo(() => {
    if (filter === 'all') {
      return tasks;
    }
    
    return tasks.filter(task => task.status === filter);
  }, [tasks, filter]);
  
  // Task completion handler
  const handleTaskComplete = useCallback(async (taskId) => {
    try {
      await axios.patch(`${API_BASE_URL}/tasks/${taskId}`, {
        status: 'completed'
      });
      
      // Update local state
      setTasks(prevTasks =>
        prevTasks.map(task =>
          task.id === taskId
            ? { ...task, status: 'completed' }
            : task
        )
      );
    } catch (err) {
      console.error('Failed to update task:', err);
      alert('Failed to mark task as completed');
    }
  }, []);
  
  // Render helpers
  const renderTask = (task) => (
    <div key={task.id} className="task-item">
      <h3>{task.title}</h3>
      <p>{task.description}</p>
      <div className="task-meta">
        <span className={`status status-${task.status}`}>{task.status}</span>
        <span className="due-date">Due: {new Date(task.dueDate).toLocaleDateString()}</span>
      </div>
      {task.status !== 'completed' && (
        <button 
          className="complete-button"
          onClick={() => handleTaskComplete(task.id)}
        >
          Mark as Complete
        </button>
      )}
    </div>
  );
  
  // Component rendering
  if (loading && tasks.length === 0) {
    return <div className="loading">Loading tasks...</div>;
  }
  
  if (error && tasks.length === 0) {
    return <div className="error">{error}</div>;
  }
  
  return (
    <div className="task-list-container">
      <div className="filter-controls">
        <button 
          className={filter === 'all' ? 'active' : ''} 
          onClick={() => setFilter('all')}
        >
          All
        </button>
        <button 
          className={filter === 'pending' ? 'active' : ''} 
          onClick={() => setFilter('pending')}
        >
          Pending
        </button>
        <button 
          className={filter === 'completed' ? 'active' : ''} 
          onClick={() => setFilter('completed')}
        >
          Completed
        </button>
      </div>
      
      <div className="task-list">
        {filteredTasks.length > 0 ? (
          filteredTasks.map(renderTask)
        ) : (
          <div className="no-tasks">No tasks found</div>
        )}
      </div>
      
      <div className="pagination">
        <button 
          disabled={page === 1} 
          onClick={() => setPage(p => Math.max(1, p - 1))}
        >
          Previous
        </button>
        <span className="page-info">Page {page}</span>
        <button onClick={() => setPage(p => p + 1)}>
          Next
        </button>
      </div>
    </div>
  );
};

// PropTypes for type checking
TaskList.propTypes = {
  userId: PropTypes.string.isRequired,
  initialFilter: PropTypes.oneOf(['all', 'pending', 'completed'])
};

TaskList.defaultProps = {
  initialFilter: 'all'
};

/**
 * A poorly structured React component with various issues
 */
class TaskManager extends React.Component {
  constructor(props) {
    super(props);
    // Too many state variables in one component
    this.state = {
      tasks: [],
      users: [],
      projects: [],
      categories: [],
      selectedTask: null,
      selectedUser: null,
      selectedProject: null,
      selectedCategory: null,
      isLoading: false,
      error: null,
      page: 1,
      limit: 10,
      totalPages: 0,
      searchQuery: '',
      sortBy: 'dueDate',
      sortOrder: 'asc',
      showCompleted: true,
      filterByPriority: null,
      filterByDueDate: null,
      filterByStatus: null,
    };
    
    // Binding methods - verbose approach
    this.handleTaskSelect = this.handleTaskSelect.bind(this);
    this.handleUserSelect = this.handleUserSelect.bind(this);
    this.handleProjectSelect = this.handleProjectSelect.bind(this);
    this.handleCategorySelect = this.handleCategorySelect.bind(this);
    this.handleSearch = this.handleSearch.bind(this);
    this.handleSort = this.handleSort.bind(this);
    this.handlePageChange = this.handlePageChange.bind(this);
    this.handleLimitChange = this.handleLimitChange.bind(this);
    this.handleTaskStatusChange = this.handleTaskStatusChange.bind(this);
    this.handleFilterChange = this.handleFilterChange.bind(this);
    this.fetchTasks = this.fetchTasks.bind(this);
    this.fetchUsers = this.fetchUsers.bind(this);
    this.fetchProjects = this.fetchProjects.bind(this);
    this.fetchCategories = this.fetchCategories.bind(this);
  }
  
  componentDidMount() {
    // Multiple fetch calls directly in lifecycle method
    this.fetchTasks();
    this.fetchUsers();
    this.fetchProjects();
    this.fetchCategories();
  }
  
  // Excessively long method
  fetchTasks() {
    this.setState({ isLoading: true, error: null });
    
    const { page, limit, sortBy, sortOrder, searchQuery, filterByPriority, 
           filterByDueDate, filterByStatus, showCompleted, selectedUser, 
           selectedProject, selectedCategory } = this.state;
    
    // Building URL with many parameters - could be refactored
    let url = `${API_BASE_URL}/tasks?page=${page}&limit=${limit}&sortBy=${sortBy}&sortOrder=${sortOrder}`;
    
    if (searchQuery) {
      url += `&search=${encodeURIComponent(searchQuery)}`;
    }
    
    if (filterByPriority) {
      url += `&priority=${filterByPriority}`;
    }
    
    if (filterByDueDate) {
      url += `&dueDate=${filterByDueDate}`;
    }
    
    if (filterByStatus) {
      url += `&status=${filterByStatus}`;
    }
    
    if (!showCompleted) {
      url += '&hideCompleted=true';
    }
    
    if (selectedUser) {
      url += `&userId=${selectedUser}`;
    }
    
    if (selectedProject) {
      url += `&projectId=${selectedProject}`;
    }
    
    if (selectedCategory) {
      url += `&categoryId=${selectedCategory}`;
    }
    
    // Fetch logic
    fetch(url)
      .then(response => {
        if (!response.ok) {
          throw new Error('Failed to fetch tasks');
        }
        return response.json();
      })
      .then(data => {
        this.setState({
          tasks: data.tasks,
          totalPages: data.totalPages,
          isLoading: false
        });
      })
      .catch(error => {
        console.error('Error fetching tasks:', error);
        this.setState({
          error: 'Failed to fetch tasks. Please try again later.',
          isLoading: false
        });
      });
  }
  
  // More fetch methods that could be consolidated
  fetchUsers() {
    fetch(`${API_BASE_URL}/users`)
      .then(response => response.json())
      .then(data => this.setState({ users: data }))
      .catch(error => console.error('Error fetching users:', error));
  }
  
  fetchProjects() {
    fetch(`${API_BASE_URL}/projects`)
      .then(response => response.json())
      .then(data => this.setState({ projects: data }))
      .catch(error => console.error('Error fetching projects:', error));
  }
  
  fetchCategories() {
    fetch(`${API_BASE_URL}/categories`)
      .then(response => response.json())
      .then(data => this.setState({ categories: data }))
      .catch(error => console.error('Error fetching categories:', error));
  }
  
  // Event handlers - could be more consistent
  handleTaskSelect(taskId) {
    this.setState({ selectedTask: taskId });
  }
  
  handleUserSelect(e) {
    this.setState({ selectedUser: e.target.value }, this.fetchTasks);
  }
  
  handleProjectSelect(e) {
    this.setState({ selectedProject: e.target.value }, this.fetchTasks);
  }
  
  handleCategorySelect(event) {
    this.setState({ selectedCategory: event.target.value }, this.fetchTasks);
  }
  
  handleSearch(e) {
    this.setState({ searchQuery: e.target.value });
  }
  
  handleSort(sortBy) {
    const { sortOrder } = this.state;
    const newSortOrder = sortBy === this.state.sortBy && sortOrder === 'asc' ? 'desc' : 'asc';
    
    this.setState({
      sortBy,
      sortOrder: newSortOrder
    }, this.fetchTasks);
  }
  
  handlePageChange(newPage) {
    this.setState({ page: newPage }, this.fetchTasks);
  }
  
  handleLimitChange(e) {
    this.setState({ limit: parseInt(e.target.value, 10), page: 1 }, this.fetchTasks);
  }
  
  handleTaskStatusChange(taskId, newStatus) {
    fetch(`${API_BASE_URL}/tasks/${taskId}`, {
      method: 'PATCH',
      headers: {
        'Content-Type': 'application/json'
      },
      body: JSON.stringify({ status: newStatus })
    })
      .then(response => response.json())
      .then(() => {
        const updatedTasks = this.state.tasks.map(task => {
          if (task.id === taskId) {
            return { ...task, status: newStatus };
          }
          return task;
        });
        
        this.setState({ tasks: updatedTasks });
      })
      .catch(error => console.error('Error updating task status:', error));
  }
  
  handleFilterChange(filterType, value) {
    if (filterType === 'priority') {
      this.setState({ filterByPriority: value }, this.fetchTasks);
    } else if (filterType === 'dueDate') {
      this.setState({ filterByDueDate: value }, this.fetchTasks);
    } else if (filterType === 'status') {
      this.setState({ filterByStatus: value }, this.fetchTasks);
    } else if (filterType === 'showCompleted') {
      this.setState({ showCompleted: value }, this.fetchTasks);
    }
  }
  
  // Large render method with mixed concerns
  render() {
    const { tasks, users, projects, categories, isLoading, error, 
           page, totalPages, selectedUser, selectedProject, selectedCategory } = this.state;
    
    // Inline styles - not ideal
    const containerStyle = {
      padding: '20px',
      backgroundColor: '#f5f5f5',
      borderRadius: '5px',
      margin: '20px',
      boxShadow: '0 2px 4px rgba(0,0,0,0.1)'
    };
    
    if (isLoading && tasks.length === 0) {
      return <div style={{ textAlign: 'center', padding: '40px' }}>Loading...</div>;
    }
    
    if (error && tasks.length === 0) {
      return <div style={{ color: 'red', textAlign: 'center', padding: '40px' }}>{error}</div>;
    }
    
    return (
      <div style={containerStyle}>
        <h1 style={{ fontSize: '24px', marginBottom: '20px' }}>Task Manager</h1>
        
        <div style={{ display: 'flex', marginBottom: '20px' }}>
          <div style={{ marginRight: '10px', flex: 1 }}>
            <label>User:</label>
            <select value={selectedUser || ''} onChange={this.handleUserSelect} style={{ width: '100%', padding: '8px' }}>
              <option value="">All Users</option>
              {users.map(user => (
                <option key={user.id} value={user.id}>{user.name}</option>
              ))}
            </select>
          </div>
          
          <div style={{ marginRight: '10px', flex: 1 }}>
            <label>Project:</label>
            <select value={selectedProject || ''} onChange={this.handleProjectSelect} style={{ width: '100%', padding: '8px' }}>
              <option value="">All Projects</option>
              {projects.map(project => (
                <option key={project.id} value={project.id}>{project.name}</option>
              ))}
            </select>
          </div>
          
          <div style={{ flex: 1 }}>
            <label>Category:</label>
            <select value={selectedCategory || ''} onChange={this.handleCategorySelect} style={{ width: '100%', padding: '8px' }}>
              <option value="">All Categories</option>
              {categories.map(category => (
                <option key={category.id} value={category.id}>{category.name}</option>
              ))}
            </select>
          </div>
        </div>
        
        <div style={{ marginBottom: '20px' }}>
          <input
            type="text"
            placeholder="Search tasks..."
            value={this.state.searchQuery}
            onChange={this.handleSearch}
            style={{ width: '100%', padding: '10px' }}
          />
          <button onClick={this.fetchTasks} style={{ marginTop: '10px', padding: '8px 16px' }}>
            Search
          </button>
        </div>
        
        <div style={{ overflowX: 'auto' }}>
          <table style={{ width: '100%', borderCollapse: 'collapse' }}>
            <thead>
              <tr>
                <th onClick={() => this.handleSort('title')} style={{ cursor: 'pointer', padding: '10px' }}>
                  Title {this.state.sortBy === 'title' && (this.state.sortOrder === 'asc' ? '↑' : '↓')}
                </th>
                <th onClick={() => this.handleSort('dueDate')} style={{ cursor: 'pointer', padding: '10px' }}>
                  Due Date {this.state.sortBy === 'dueDate' && (this.state.sortOrder === 'asc' ? '↑' : '↓')}
                </th>
                <th onClick={() => this.handleSort('status')} style={{ cursor: 'pointer', padding: '10px' }}>
                  Status {this.state.sortBy === 'status' && (this.state.sortOrder === 'asc' ? '↑' : '↓')}
                </th>
                <th onClick={() => this.handleSort('priority')} style={{ cursor: 'pointer', padding: '10px' }}>
                  Priority {this.state.sortBy === 'priority' && (this.state.sortOrder === 'asc' ? '↑' : '↓')}
                </th>
                <th style={{ padding: '10px' }}>Actions</th>
              </tr>
            </thead>
            <tbody>
              {tasks.map(task => (
                <tr key={task.id} onClick={() => this.handleTaskSelect(task.id)} style={{ cursor: 'pointer' }}>
                  <td style={{ padding: '10px' }}>{task.title}</td>
                  <td style={{ padding: '10px' }}>{new Date(task.dueDate).toLocaleDateString()}</td>
                  <td style={{ padding: '10px' }}>{task.status}</td>
                  <td style={{ padding: '10px' }}>{task.priority}</td>
                  <td style={{ padding: '10px' }}>
                    <button onClick={(e) => { 
                      e.stopPropagation(); 
                      this.handleTaskStatusChange(task.id, task.status === 'completed' ? 'pending' : 'completed'); 
                    }}
                    style={{ padding: '5px 10px' }}>
                      {task.status === 'completed' ? 'Mark Incomplete' : 'Mark Complete'}
                    </button>
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
        
        <div style={{ marginTop: '20px', display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
          <div>
            <select value={this.state.limit} onChange={this.handleLimitChange} style={{ padding: '5px' }}>
              <option value="5">5 per page</option>
              <option value="10">10 per page</option>
              <option value="20">20 per page</option>
              <option value="50">50 per page</option>
            </select>
          </div>
          
          <div>
            <button
              disabled={page === 1}
              onClick={() => this.handlePageChange(page - 1)}
              style={{ padding: '5px 10px', marginRight: '10px' }}
            >
              Previous
            </button>
            
            <span>
              Page {page} of {totalPages}
            </span>
            
            <button
              disabled={page === totalPages}
              onClick={() => this.handlePageChange(page + 1)}
              style={{ padding: '5px 10px', marginLeft: '10px' }}
            >
              Next
            </button>
          </div>
        </div>
      </div>
    );
  }
}

// Component without PropTypes
const QuickAddTask = ({ onAdd }) => {
  const [title, setTitle] = useState('');
  const [dueDate, setDueDate] = useState('');
  
  const handleSubmit = (e) => {
    e.preventDefault();
    if (!title.trim()) return;
    
    const newTask = {
      title,
      dueDate: dueDate || new Date().toISOString().split('T')[0],
      status: 'pending',
      priority: 'medium'
    };
    
    onAdd(newTask);
    setTitle('');
    setDueDate('');
  };
  
  return (
    <form onSubmit={handleSubmit} style={{ margin: '20px 0', padding: '15px', border: '1px solid #ddd' }}>
      <h3>Quick Add Task</h3>
      <div>
        <input
          type="text"
          value={title}
          onChange={e => setTitle(e.target.value)}
          placeholder="Task title"
          style={{ width: '100%', padding: '8px', marginBottom: '10px' }}
        />
      </div>
      <div>
        <input
          type="date"
          value={dueDate}
          onChange={e => setDueDate(e.target.value)}
          style={{ width: '100%', padding: '8px', marginBottom: '10px' }}
        />
      </div>
      <button type="submit" style={{ padding: '8px 16px', backgroundColor: '#4CAF50', color: 'white', border: 'none' }}>
        Add Task
      </button>
    </form>
  );
};

export { TaskList, TaskManager, QuickAddTask };
export default TaskList; 