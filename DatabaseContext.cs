using System;
using System.Collections.Generic;
using System.Data.SqlClient;
using System.Threading.Tasks;

namespace Kontrollzentrum.Database
{
    public class DatabaseContext
    {
        private string _connectionString;
        private List<Operation> _operations;
        private List<Backup> _backups;
        private List<Metric> _metrics;

        public DatabaseContext(string connectionString)
        {
            _connectionString = connectionString;
            _operations = new List<Operation>();
            _backups = new List<Backup>();
            _metrics = new List<Metric>();
        }

        public async Task InitializeDatabaseAsync()
        {
            using (var connection = new SqlConnection(_connectionString))
            {
                await connection.OpenAsync();
                
                var commands = new[]
                {
                    CreateOperationsTable(),
                    CreateBackupsTable(),
                    CreateMetricsTable()
                };

                foreach (var cmd in commands)
                {
                    using (var command = new SqlCommand(cmd, connection))
                    {
                        await command.ExecuteNonQueryAsync();
                    }
                }
            }
        }

        public async Task<int> AddOperationAsync(Operation op)
        {
            _operations.Add(op);
            return _operations.Count;
        }

        public async Task<int> AddBackupAsync(Backup backup)
        {
            _backups.Add(backup);
            return _backups.Count;
        }

        public async Task<int> AddMetricAsync(Metric metric)
        {
            _metrics.Add(metric);
            return _metrics.Count;
        }

        public List<Operation> GetOperations() => _operations;
        public List<Backup> GetBackups() => _backups;
        public List<Metric> GetMetrics() => _metrics;

        private string CreateOperationsTable() =>
            @"IF NOT EXISTS (SELECT * FROM sys.tables WHERE name = 'Operations')
              CREATE TABLE Operations (
                  Id INT PRIMARY KEY IDENTITY(1,1),
                  OperationId NVARCHAR(MAX),
                  Type NVARCHAR(MAX),
                  Status NVARCHAR(MAX),
                  CreatedAt DATETIME,
                  CompletedAt DATETIME
              )";

        private string CreateBackupsTable() =>
            @"IF NOT EXISTS (SELECT * FROM sys.tables WHERE name = 'Backups')
              CREATE TABLE Backups (
                  Id INT PRIMARY KEY IDENTITY(1,1),
                  BackupId NVARCHAR(MAX),
                  SourcePath NVARCHAR(MAX),
                  BackupPath NVARCHAR(MAX),
                  Size BIGINT,
                  CreatedAt DATETIME
              )";

        private string CreateMetricsTable() =>
            @"IF NOT EXISTS (SELECT * FROM sys.tables WHERE name = 'Metrics')
              CREATE TABLE Metrics (
                  Id INT PRIMARY KEY IDENTITY(1,1),
                  CpuUsage FLOAT,
                  MemoryUsage FLOAT,
                  HealthScore INT,
                  Timestamp DATETIME
              )";
    }

    public class Operation
    {
        public string Id { get; set; }
        public string Type { get; set; }
        public string Status { get; set; }
        public DateTime CreatedAt { get; set; }
        public DateTime? CompletedAt { get; set; }
    }

    public class Backup
    {
        public string BackupId { get; set; }
        public string SourcePath { get; set; }
        public string BackupPath { get; set; }
        public long Size { get; set; }
        public DateTime CreatedAt { get; set; }
    }

    public class Metric
    {
        public float CpuUsage { get; set; }
        public float MemoryUsage { get; set; }
        public int HealthScore { get; set; }
        public DateTime Timestamp { get; set; }
    }
}
