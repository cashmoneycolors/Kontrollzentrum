# 🚀 KONTROLLZENTRUM - PRODUCTION DEPLOYMENT GUIDE

## ✅ Production-Grade Features Implemented

### 1. **API Gateway + Load Balancer** (`core/api_gateway.py`)
- ✅ Central request routing
- ✅ Circuit breaker pattern (auto-recovery)
- ✅ Request/response monitoring
- ✅ Graceful shutdown

**Start:** `python main.py api`

### 2. **Monitoring & Alerting** (`core/health_monitor.py`)
- ✅ Real-time system metrics (CPU, Memory, Disk)
- ✅ Module health checks
- ✅ Auto-recovery attempts
- ✅ Alert system

**Check:** `python main.py health`

### 3. **Database Layer** (`core/database.py`)
- ✅ SQLite persistence
- ✅ Module results storage
- ✅ Configuration management
- ✅ Audit logging

**Data:** `kontrollzentrum.db`

### 4. **Authentication & Authorization** (`core/auth.py`)
- ✅ JWT token generation
- ✅ Role-based access control
- ✅ Token verification
- ✅ Secure endpoints

**Generate tokens:** `python core/auth.py`

### 5. **Rate Limiting + Caching** (`core/rate_limiter.py`)
- ✅ Per-client rate limiting (100 req/min)
- ✅ Result caching (5 min TTL)
- ✅ Cache statistics
- ✅ DoS protection

### 6. **Error Recovery** (`core/api_gateway.py`)
- ✅ Circuit breaker (5 failures = OPEN)
- ✅ Auto-recovery after timeout
- ✅ Graceful degradation
- ✅ Error logging

---

## 🚀 QUICK START

### Prerequisites
```bash
pip install -r requirements.txt
```

### 1. Generate Auth Tokens
```bash
python core/auth.py
```
Output: Admin and User tokens for API access

### 2. Start API Gateway
```bash
python main.py api
```
Gateway runs on `http://0.0.0.0:8000`

### 3. Check System Health
```bash
python main.py health
```
Shows all module status + system metrics

### 4. Run Team Mode
```bash
python main.py team
```
Installs and executes all 16 modules

---

## 📊 API ENDPOINTS

### Health & Monitoring
```
GET  /health              - System health status
GET  /metrics             - Performance metrics
GET  /logs?limit=100      - Request logs (requires auth)
```

### Module Execution
```
POST /execute/{module_name}  - Execute module (requires auth)
GET  /status/{module_name}   - Module status + circuit breaker state
```

### Example Requests

**Get Health:**
```bash
curl http://localhost:8000/health
```

**Get Metrics:**
```bash
curl http://localhost:8000/metrics
```

**Execute Module (with token):**
```bash
curl -X POST http://localhost:8000/execute/quantum_demo_modul \
  -H "Authorization: Bearer <YOUR_TOKEN>"
```

**Get Logs (with token):**
```bash
curl http://localhost:8000/logs?limit=50 \
  -H "Authorization: Bearer <YOUR_TOKEN>"
```

---

## 🔐 SECURITY CHECKLIST

- [ ] Change `JWT_SECRET` in `.env` (production)
- [ ] Enable HTTPS in production
- [ ] Set rate limits per client
- [ ] Configure firewall rules
- [ ] Enable audit logging
- [ ] Regular backups of `kontrollzentrum.db`
- [ ] Monitor alerts continuously
- [ ] Update dependencies regularly

---

## 📈 MONITORING DASHBOARD

Access Streamlit dashboard:
```bash
streamlit run main.py
```

Shows:
- Real-time metrics
- Module status
- Request history
- System health
- Alerts

---

## 🛠️ TROUBLESHOOTING

### API Gateway won't start
```bash
# Check port 8000 is free
netstat -ano | findstr :8000

# Kill process if needed
taskkill /PID <PID> /F
```

### Module health check fails
```bash
python main.py health
# Check error messages and logs
```

### Database issues
```bash
# Reset database
rm kontrollzentrum.db
python main.py api  # Recreates schema
```

### High CPU/Memory
```bash
# Check metrics
python main.py health

# Clear cache
python -c "from core.rate_limiter import cache; cache.clear()"
```

---

## 📊 PRODUCTION LAUNCHER

Interactive menu with all modes:
```bash
PRODUCTION.bat
```

Options:
1. 🌐 API Gateway
2. 📊 Health Check
3. 🏃 Team Mode
4. 🎯 CLI Mode
5. 📈 Dashboard
6. 🔐 Generate Tokens
7. 📊 View Metrics
8. ❌ Exit

---

## 🔄 DEPLOYMENT WORKFLOW

1. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

2. **Configure environment**
   ```bash
   # Create .env with:
   JWT_SECRET=your-secret-key
   # ... other API keys
   ```

3. **Initialize database**
   ```bash
   python main.py api  # Starts and initializes
   ```

4. **Generate tokens**
   ```bash
   python core/auth.py
   ```

5. **Run health check**
   ```bash
   python main.py health
   ```

6. **Start production**
   ```bash
   python main.py api  # API Gateway
   # In another terminal:
   streamlit run main.py  # Dashboard
   ```

---

## 📝 LOGS & MONITORING

### Request Logs
```bash
curl http://localhost:8000/logs?limit=100 \
  -H "Authorization: Bearer <TOKEN>"
```

### System Metrics
```bash
curl http://localhost:8000/metrics
```

### Database Queries
```python
from core.database import db
results = db.get_results(limit=50)
logs = db.get_audit_log(limit=100)
```

---

## 🎯 NEXT STEPS

- [ ] Deploy to production server
- [ ] Set up monitoring alerts
- [ ] Configure backup strategy
- [ ] Enable HTTPS/SSL
- [ ] Set up CI/CD pipeline
- [ ] Configure load balancer
- [ ] Set up log aggregation
- [ ] Create runbooks for operations

---

**Status:** ✅ PRODUCTION READY

**Last Updated:** 2025-01-15

**Version:** 2.0 (Production Grade)
