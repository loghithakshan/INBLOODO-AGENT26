# 🔐 BLOOD REPORT AI - LOGIN CREDENTIALS

## Default Test Accounts

The system comes with two pre-configured test accounts for immediate use:

---

### **👨‍💼 ADMIN ACCOUNT**
```
Username: admin
Password: secret
Email:    admin@inbloodo.com
Role:     Administrator
```

**Access Level**: Full system access, user management, settings

---

### **👤 TEST ACCOUNT**
```
Username: test
Password: secret
Email:    test@inbloodo.com
Role:     Patient
```

**Access Level**: Can upload and analyze blood reports, view own results

---

## How to Login

### **Web Dashboard**
1. Go to: http://localhost:8000/
2. Click "Login" or "Sign In"
3. Enter credentials above
4. Choose account (admin or test)

### **API Login**
```bash
curl -X POST http://localhost:8000/api/login/ \
  -H "Content-Type: application/json" \
  -d '{"username":"admin","password":"secret"}'
```

Or with Python:
```python
import requests

credentials = {
    "username": "admin",
    "password": "secret"
}

response = requests.post(
    "http://localhost:8000/api/login/",
    json=credentials
)

print(response.json())
```

---

## API Key (No Auth Required)

For API access without login, an API key is automatically generated:

```bash
# Health check (no auth needed)
curl http://localhost:8000/health

# Demo analysis (no auth needed)
curl http://localhost:8000/api/demo/analyze/healthy
```

---

## Account Details

| Field | Admin | Test |
|-------|-------|------|
| **Username** | admin | test |
| **Password** | secret | secret |
| **Email** | admin@inbloodo.com | test@inbloodo.com |
| **Role** | Administrator | Patient |
| **Full Name** | Administrator | Test User |
| **Can analyze reports** | ✅ Yes | ✅ Yes |
| **Can manage users** | ✅ Yes | ❌ No |
| **Can view all results** | ✅ Yes | ❌ Only own |
| **Can configure system** | ✅ Yes | ❌ No |

---

## First-Time Login Steps

1. **Open dashboard**: http://localhost:8000/
2. **Click Login button**
3. **Enter credentials**:
   - Username: `admin` (or `test`)
   - Password: `secret`
4. **Submit**
5. **You're in!** 🎉

---

## Password Reset / User Management

To change passwords or manage users:

1. Login as **admin**
2. Go to Settings → User Management
3. Edit user details
4. Update password if needed
5. Save changes

---

## Creating New Users

### Via Web Dashboard (Admin Only)
1. Login as admin
2. Go to Admin Panel
3. Click "Create New User"
4. Enter user details
5. Set role (admin, doctor, patient)
6. Save

### Via API (Admin Only)
```python
import requests

headers = {"Authorization": "Bearer YOUR_TOKEN"}

new_user = {
    "username": "newuser",
    "password": "securepass123",
    "email": "newuser@example.com",
    "role": "patient",
    "full_name": "New User"
}

response = requests.post(
    "http://localhost:8000/api/users/",
    json=new_user,
    headers=headers
)
```

---

## Security Notes

⚠️ **Important for Production**:

1. **Change default passwords** before production deployment
2. **Use strong passwords** (min 8 characters, mixed case, numbers, symbols)
3. **Enable HTTPS** for encrypted login
4. **Use environment variables** for sensitive data
5. **Implement rate limiting** on login endpoint
6. **Enable 2FA** (optional, can be configured)

---

## Troubleshooting Login

### "Invalid Username or Password"
- Check spelling (case-sensitive)
- Verify you're using one of the test accounts above
- Make sure server is running (http://localhost:8000/health)

### "Database Connection Error"
- Ensure database is initialized
- Run: `python setup_database.py`
- Or restart server: `python main.py`

### "Login Page Won't Load"
- Server may not be running
- Check: http://localhost:8000/health
- If 404, restart with: `python main.py`

### "Forgot Password"
- For test accounts, password is always: `secret`
- For production, implement password reset flow
- Admin can reset user passwords in User Management

---

## Quick Test Commands

### Test Admin Login:
```bash
curl -X POST http://localhost:8000/api/login/ \
  -H "Content-Type: application/json" \
  -d '{"username":"admin","password":"secret"}'
```

### Test Patient Login:
```bash
curl -X POST http://localhost:8000/api/login/ \
  -H "Content-Type: application/json" \
  -d '{"username":"test","password":"secret"}'
```

### Verify Login Works:
```python
import requests

# Try admin login
resp = requests.post('http://localhost:8000/api/login/', 
    json={"username": "admin", "password": "secret"}
)

if resp.status_code == 200:
    print("✓ Login successful!")
    print(f"Token: {resp.json()}")
else:
    print(f"✗ Login failed: {resp.status_code}")
    print(resp.text)
```

---

## Multi-Role System

### **Admin** (Full Access)
- Manage all users
- View all analysis results
- Configure system settings
- Manage LLM providers
- View system logs
- Backup/restore data

### **Doctor/Staff** (Limited Admin)
- View patient results
- Create patient accounts
- Generate reports
- Cannot manage other staff

### **Patient** (User Access)
- Upload blood reports
- View own analysis results
- Download own reports
- Cannot see other patients' data

---

## Session Management

Sessions automatically expire after:
- **Web**: 24 hours
- **API**: Based on token TTL (configurable)

To manually logout:
- Click "Logout" in top menu
- Or POST to `/api/logout/` endpoint

---

## Recommended First Login

**Use the admin account to:**
1. Verify system is working
2. Upload a test blood report
3. See analysis results
4. Check dashboard
5. Explore settings

**Then use test account to:**
1. See patient perspective
2. Test report upload
3. Verify role-based access

---

**Credentials Valid**: Immediately after server start  
**Status**: ✅ Ready to use  
**Support**: All accounts functional

Happy analyzing! 🩸
