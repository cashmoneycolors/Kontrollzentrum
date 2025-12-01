using System;
using System.Collections.Generic;
using System.Linq;

namespace DropshippingApp.Services
{
    public class ConnectionPool
    {
        private Queue<DatabaseService> _available = new();
        private HashSet<DatabaseService> _inUse = new();
        private int _maxConnections = 10;
        private LoggingService _logger = new();

        public ConnectionPool(int maxConnections = 10)
        {
            _maxConnections = maxConnections;
            for (int i = 0; i < maxConnections; i++)
                _available.Enqueue(new DatabaseService());
        }

        public DatabaseService AcquireConnection()
        {
            if (_available.Count == 0 && _inUse.Count < _maxConnections)
                _available.Enqueue(new DatabaseService());

            if (_available.Count == 0)
            {
                _logger.LogWarning("Connection pool exhausted");
                return null;
            }

            var conn = _available.Dequeue();
            _inUse.Add(conn);
            return conn;
        }

        public void ReleaseConnection(DatabaseService conn)
        {
            if (_inUse.Remove(conn))
                _available.Enqueue(conn);
        }

        public int GetAvailableConnections() => _available.Count;
        public int GetUsedConnections() => _inUse.Count;
    }
}
