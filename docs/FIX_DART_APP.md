# 🔧 Fixing Your Dart App - Complete Guide

## 🚨 Current Issues

From the logs, I can see:
1. **401 error on login** - Authentication failed
2. **400 error on registration** - Bad request
3. **Wrong API URL** - Dart app is hitting HTML pages instead of your Flask API

## 🔍 Step 1: Find Your Correct API URL

### Check Your Render Dashboard
1. Go to [render.com](https://render.com)
2. Sign in and go to your dashboard
3. Look for your web service
4. **Copy the exact URL** from the dashboard

### Common URL Patterns:
- `https://remindly-api.onrender.com`
- `https://remindly.onrender.com` 
- `https://task-manager-api.onrender.com`
- `https://your-username-remindly.onrender.com`

## 🔧 Step 2: Test Your API URL

### Test with curl:
```bash
# Test the root endpoint
curl https://YOUR_ACTUAL_API_URL.onrender.com/

# Test registration
curl -X POST https://YOUR_ACTUAL_API_URL.onrender.com/api/register \
  -H "Content-Type: application/json" \
  -d '{"username": "testuser", "email": "test@example.com", "password": "password123"}'

# Test login
curl -X POST https://YOUR_ACTUAL_API_URL.onrender.com/api/login \
  -H "Content-Type: application/json" \
  -d '{"username": "testuser", "password": "password123"}'
```

### Expected Responses:
- **Root endpoint**: JSON with API information
- **Registration**: 201 status with user data
- **Login**: 200 status with JWT token

## 📱 Step 3: Fix Your Dart App

### Update the Base URL
Replace the current URL in your Dart app with the correct one:

```dart
class ApiService {
  // Update this to your actual API URL from Render dashboard
  static const String baseUrl = 'https://YOUR_ACTUAL_API_URL.onrender.com';
  
  // ... rest of your code
}
```

### Fix the Authentication Flow

```dart
import 'dart:convert';
import 'package:http/http.dart' as http;
import 'package:shared_preferences/shared_preferences.dart';

class ApiService {
  static const String baseUrl = 'https://YOUR_ACTUAL_API_URL.onrender.com';
  
  // Step 1: Register user
  static Future<bool> register(String username, String email, String password) async {
    try {
      final response = await http.post(
        Uri.parse('$baseUrl/api/register'),
        headers: {'Content-Type': 'application/json'},
        body: jsonEncode({
          'username': username,
          'email': email,
          'password': password,
        }),
      );
      
      print('Registration status: ${response.statusCode}');
      print('Registration response: ${response.body}');
      
      return response.statusCode == 201;
    } catch (e) {
      print('Registration error: $e');
      return false;
    }
  }
  
  // Step 2: Login to get JWT token
  static Future<String?> login(String username, String password) async {
    try {
      final response = await http.post(
        Uri.parse('$baseUrl/api/login'),
        headers: {'Content-Type': 'application/json'},
        body: jsonEncode({
          'username': username,
          'password': password,
        }),
      );
      
      print('Login status: ${response.statusCode}');
      print('Login response: ${response.body}');
      
      if (response.statusCode == 200) {
        final data = jsonDecode(response.body);
        final token = data['access_token'];
        
        // Store token
        final prefs = await SharedPreferences.getInstance();
        await prefs.setString('jwt_token', token);
        
        return token;
      }
    } catch (e) {
      print('Login error: $e');
    }
    return null;
  }
  
  // Step 3: Use JWT token for authenticated requests
  static Future<List<dynamic>> getTasks({bool? completed}) async {
    try {
      final prefs = await SharedPreferences.getInstance();
      final token = prefs.getString('jwt_token');
      
      if (token == null) {
        throw Exception('No JWT token found. Please login first.');
      }
      
      final queryParams = completed != null ? {'completed': completed.toString()} : {};
      final uri = Uri.parse('$baseUrl/api/tasks').replace(queryParameters: queryParams);
      
      final response = await http.get(
        uri,
        headers: {
          'Content-Type': 'application/json',
          'Authorization': 'Bearer $token', // This fixes the 422 errors!
        },
      );
      
      print('Tasks status: ${response.statusCode}');
      print('Tasks response: ${response.body}');
      
      if (response.statusCode == 200) {
        final data = jsonDecode(response.body);
        return data['tasks'] ?? [];
      } else {
        throw Exception('Failed to load tasks: ${response.statusCode}');
      }
    } catch (e) {
      print('Get tasks error: $e');
      rethrow;
    }
  }
  
  // Step 4: Get notifications with authentication
  static Future<List<dynamic>> getNotifications() async {
    try {
      final prefs = await SharedPreferences.getInstance();
      final token = prefs.getString('jwt_token');
      
      if (token == null) {
        throw Exception('No JWT token found. Please login first.');
      }
      
      final response = await http.get(
        Uri.parse('$baseUrl/api/notifications/due'),
        headers: {
          'Content-Type': 'application/json',
          'Authorization': 'Bearer $token', // This fixes the 422 errors!
        },
      );
      
      print('Notifications status: ${response.statusCode}');
      print('Notifications response: ${response.body}');
      
      if (response.statusCode == 200) {
        final data = jsonDecode(response.body);
        return data['notifications'] ?? [];
      } else {
        throw Exception('Failed to load notifications: ${response.statusCode}');
      }
    } catch (e) {
      print('Get notifications error: $e');
      rethrow;
    }
  }
}
```

## 🧪 Step 4: Test Your Fix

### Test the Complete Flow:

```dart
void testApi() async {
  // 1. Register a user
  final registered = await ApiService.register('testuser', 'test@example.com', 'password123');
  print('Registration: $registered');
  
  // 2. Login to get token
  final token = await ApiService.login('testuser', 'password123');
  print('Login token: ${token != null ? "Success" : "Failed"}');
  
  // 3. Get tasks (should work now)
  if (token != null) {
    try {
      final tasks = await ApiService.getTasks();
      print('Tasks: ${tasks.length} found');
    } catch (e) {
      print('Tasks error: $e');
    }
  }
}
```

## 🔍 Step 5: Debug Common Issues

### Issue 1: 404 Errors
**Problem**: Wrong API URL
**Solution**: Check Render dashboard for correct URL

### Issue 2: 401 Errors
**Problem**: Wrong credentials or user doesn't exist
**Solution**: Register user first, then login

### Issue 3: 400 Errors
**Problem**: Bad request data
**Solution**: Check JSON format and required fields

### Issue 4: 422 Errors
**Problem**: Missing JWT token
**Solution**: Add `Authorization: Bearer <token>` header

## 📋 Checklist

- [ ] **Find correct API URL** from Render dashboard
- [ ] **Test API manually** with curl
- [ ] **Update base URL** in Dart app
- [ ] **Add debug logging** to see responses
- [ ] **Test registration** first
- [ ] **Test login** to get JWT token
- [ ] **Add Authorization header** to all requests
- [ ] **Test authenticated endpoints**

## 🎯 Expected Results

After fixing:
- ✅ **Registration**: 201 status
- ✅ **Login**: 200 status with JWT token
- ✅ **Tasks**: 200 status with task data
- ✅ **Notifications**: 200 status with notification data

## 🆘 Still Having Issues?

1. **Check Render logs** for deployment issues
2. **Verify environment variables** are set correctly
3. **Test API locally** first
4. **Check network connectivity** from your device

**Your API is working - we just need to connect to the right URL!** 🚀 