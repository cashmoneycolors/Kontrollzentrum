using System;
using System.Collections.Generic;
using System.Linq;
using System.Threading.Tasks;
using Microsoft.Data.Sqlite;

namespace DropshippingApp.Services
{
    public class QuantumDatabase
    {
        private readonly string _connectionString = "Data Source=quantum.db;Cache=Shared";
        private readonly CacheService _cache = new();
        private readonly ConnectionPool _pool = new(20);
        private readonly PerformanceOptimizer _perf = new();
        private readonly LoggingService _logger = new();
        private Dictionary<string, QueryStats> _queryStats = new();

        public QuantumDatabase() => InitializeSchema();

        private void InitializeSchema()
        {
            using (var conn = _pool.AcquireConnection())
            {
                var cmd = conn.CreateCommand();
                cmd.CommandText = @"
                    CREATE TABLE IF NOT EXISTS Orders (Id INTEGER PRIMARY KEY, OrderId TEXT UNIQUE, Email TEXT, Total REAL, Status TEXT, CreatedAt TEXT);
                    CREATE TABLE IF NOT EXISTS Products (Id INTEGER PRIMARY KEY, Asin TEXT UNIQUE, Title TEXT, Price REAL, Supplier TEXT, Margin REAL);
                    CREATE TABLE IF NOT EXISTS Users (Id INTEGER PRIMARY KEY, Email TEXT UNIQUE, PasswordHash TEXT, CreatedAt TEXT);
                    CREATE TABLE IF NOT EXISTS Transactions (Id INTEGER PRIMARY KEY, TransactionId TEXT UNIQUE, Amount REAL, Status TEXT, CreatedAt TEXT);
                    CREATE INDEX IF NOT EXISTS idx_orders_status ON Orders(Status);
                    CREATE INDEX IF NOT EXISTS idx_products_supplier ON Products(Supplier);
                    CREATE INDEX IF NOT EXISTS idx_transactions_status ON Transactions(Status);
                ";
                cmd.ExecuteNonQuery();
                _pool.ReleaseConnection(conn);
            }
        }

        public async Task<T> QueryAsync<T>(string query, Func<SqliteDataReader, T> mapper)
        {
            var cacheKey = $"query_{query.GetHashCode()}";
            var cached = _cache.Get<T>(cacheKey);
            if (cached != null) return cached;

            _perf.StartTimer(query);
            using (var conn = _pool.AcquireConnection())
            {
                var cmd = conn.CreateCommand();
                cmd.CommandText = query;
                using (var reader = cmd.ExecuteReader())
                {
                    var result = mapper(reader);
                    _cache.Set(cacheKey, result, 300);
                    _perf.EndTimer(query);
                    TrackQuery(query);
                    return result;
                }
            }
        }

        public async Task ExecuteAsync(string query, Action<SqliteCommand> parameterize = null)
        {
            _perf.StartTimer(query);
            using (var conn = _pool.AcquireConnection())
            {
                var cmd = conn.CreateCommand();
                cmd.CommandText = query;
                parameterize?.Invoke(cmd);
                cmd.ExecuteNonQuery();
                _cache.Set($"query_{query.GetHashCode()}", null, 1);
                _perf.EndTimer(query);
                TrackQuery(query);
            }
        }

        public async Task<List<T>> QueryListAsync<T>(string query, Func<SqliteDataReader, T> mapper)
        {
            var cacheKey = $"list_{query.GetHashCode()}";
            var cached = _cache.Get<List<T>>(cacheKey);
            if (cached != null) return cached;

            _perf.StartTimer(query);
            var results = new List<T>();
            using (var conn = _pool.AcquireConnection())
            {
                var cmd = conn.CreateCommand();
                cmd.CommandText = query;
                using (var reader = cmd.ExecuteReader())
                {
                    while (reader.Read()) results.Add(mapper(reader));
                }
                _cache.Set(cacheKey, results, 300);
                _perf.EndTimer(query);
                TrackQuery(query);
                return results;
            }
        }

        public Dictionary<string, QueryStats> GetQueryStats() => _queryStats;

        public void OptimizeIndexes()
        {
            var topQueries = _queryStats.OrderByDescending(x => x.Value.TotalTime).Take(5);
            foreach (var q in topQueries)
                _logger.LogInfo($"Slow query: {q.Key} - {q.Value.TotalTime}ms");
        }

        private void TrackQuery(string query)
        {
            if (!_queryStats.ContainsKey(query))
                _queryStats[query] = new QueryStats();
            _queryStats[query].Count++;
            _queryStats[query].TotalTime += _perf.GetMetrics().Values.LastOrDefault();
        }

        private class QueryStats { public int Count { get; set; } public long TotalTime { get; set; } }
    }
}
