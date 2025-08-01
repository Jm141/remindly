# 🔧 Fixing 422 Errors in Dart/Flutter App

## 🚨 The Problem

Your API logs show **422 errors** from a Dart app:
```
127.0.0.1 - - [31/Jul/2025:03:27:22 +0000] "GET /api/tasks?completed=false HTTP/1.1" 422 40 "-" "Dart/3.8 (dart:io)"
127.0.0.1 - - [31/Jul/2025:03:27:25 +0000] "GET /api/notifications/due HTTP/1.1" 422 40 "-" "Dart/3.8 (dart:io)"
```

**422 Error = Unprocessable Entity** = Missing JWT Authentication Token

## ✅ The Solution

Your Dart/Flutter app needs to include the JWT token in the Authorization header.

### Step 1: Login to Get JWT Token

First, your app needs to login to get a JWT token:

```dart
// Login request
final loginResponse = await http.post(
  Uri.parse('https://your-api-url.onrender.com/api/login'),
  headers: {'Content-Type': 'application/json'},
  body: jsonEncode({
    'username': 'your_username',
    'password': 'your_password',
  }),
);

if (loginResponse.statusCode == 200) {
  final loginData = jsonDecode(loginResponse.body);
  final jwtToken = loginData['access_token']; // Save this token
  
  // Store the token securely (SharedPreferences, secure storage, etc.)
  await prefs.setString('jwt_token', jwtToken);
}
```

### Step 2: Use JWT Token in All API Requests

For all authenticated endpoints, include the Authorization header:

```dart
// Get the stored JWT token
final jwtToken = await prefs.getString('jwt_token');

// Make authenticated requests
final response = await http.get(
  Uri.parse('https://your-api-url.onrender.com/api/tasks?completed=false'),
  headers: {
    'Content-Type': 'application/json',
    'Authorization': 'Bearer $jwtToken', // Add this line!
  },
);
```

### Step 3: Complete Example

Here's a complete example of how your Dart code should look:

```dart
import 'dart:convert';
import 'package:http/http.dart' as http;
import 'package:shared_preferences/shared_preferences.dart';

class ApiService {
  static const String baseUrl = 'https://your-api-url.onrender.com';
  
  // Login method
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
  
  // Get tasks with authentication
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
          'Authorization': 'Bearer $token', // This is the key!
        },
      );
      
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
  
  // Get notifications with authentication
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
          'Authorization': 'Bearer $token', // This is the key!
        },
      );
      
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

## 🔍 Testing Your Fix

### Test the API Manually:

```bash
# 1. Login to get token
curl -X POST https://your-api-url.onrender.com/api/login \
  -H "Content-Type: application/json" \
  -d '{"username": "testuser", "password": "password123"}'

# 2. Use the token to access protected endpoints
curl -X GET https://your-api-url.onrender.com/api/tasks \
  -H "Authorization: Bearer YOUR_JWT_TOKEN_HERE" \
  -H "Content-Type: application/json"
```

### Expected Results:
- **Before fix**: 422 errors
- **After fix**: 200 OK responses with data

## 🚀 Quick Fix Checklist

- [ ] **Login first** to get JWT token
- [ ] **Store token** securely in your app
- [ ] **Add Authorization header** to all API requests
- [ ] **Use correct format**: `Bearer <token>`
- [ ] **Handle token expiration** (refresh when needed)

## 📱 Flutter/Dart Dependencies

Make sure you have these in your `pubspec.yaml`:

```yaml
dependencies:
  http: ^1.1.0
  shared_preferences: ^2.2.2
  # or use flutter_secure_storage for better security
  flutter_secure_storage: ^9.0.0
```

## 🎯 Summary

The 422 errors are happening because your Dart app is making requests to authenticated endpoints without providing the JWT token. Once you add the `Authorization: Bearer <token>` header to your requests, the 422 errors will disappear and you'll get proper responses from your API.

Your API is working correctly - it's just enforcing authentication as it should! 🔐 