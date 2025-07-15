// Security configuration
export const securityConfig = {
  // API configuration
  api: {
    baseURL: process.env.REACT_APP_API_URL || 'http://localhost:8000',
    timeout: 5000,
    headers: {
      'Content-Type': 'application/json',
      'Accept': 'application/json',
    },
  },

  // Session configuration
  session: {
    storageKey: 'plant_tracker_session',
    maxAge: 3600, // 1 hour
  },

  // Password requirements
  password: {
    minLength: 8,
    requireUppercase: true,
    requireLowercase: true,
    requireNumbers: true,
    requireSpecialChars: true,
  },

  // Rate limiting
  rateLimit: {
    maxRequests: 100,
    timeWindow: 60000, // 1 minute
  },

  // Input validation
  validation: {
    maxStringLength: 255,
    allowedFileTypes: ['image/jpeg', 'image/png', 'image/gif'],
    maxFileSize: 5 * 1024 * 1024, // 5MB
  },
};

// Security utility functions
export const securityUtils = {
  // Sanitize user input
  sanitizeInput: (input) => {
    if (typeof input !== 'string') return input;
    return input
      .replace(/[<>]/g, '') // Remove < and >
      .trim();
  },

  // Validate password strength
  validatePassword: (password) => {
    const { minLength, requireUppercase, requireLowercase, requireNumbers, requireSpecialChars } = securityConfig.password;
    
    if (password.length < minLength) return false;
    if (requireUppercase && !/[A-Z]/.test(password)) return false;
    if (requireLowercase && !/[a-z]/.test(password)) return false;
    if (requireNumbers && !/\d/.test(password)) return false;
    if (requireSpecialChars && !/[!@#$%^&*(),.?":{}|<>]/.test(password)) return false;
    
    return true;
  },

  // Generate CSRF token
  generateCSRFToken: () => {
    return Math.random().toString(36).substring(2) + Date.now().toString(36);
  },
}; 