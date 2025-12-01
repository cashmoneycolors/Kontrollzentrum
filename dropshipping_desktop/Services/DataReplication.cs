using System;
using System.Collections.Generic;
using System.Threading.Tasks;

namespace DropshippingApp.Services
{
    public class DataReplication
    {
        private readonly QuantumDatabase _primary;
        private readonly List<QuantumDatabase> _replicas = new();
        private readonly LoggingService _logger = new();

        public DataReplication(QuantumDatabase primary)
        {
            _primary = primary;
        }

        public void AddReplica(QuantumDatabase replica)
        {
            _replicas.Add(replica);
            _logger.LogInfo($"Replica added. Total replicas: {_replicas.Count}");
        }

        public async Task ReplicateAsync(string query)
        {
            var tasks = _replicas.Select(r => Task.Run(() => r.ExecuteAsync(query)));
            await Task.WhenAll(tasks);
            _logger.LogInfo($"Replicated to {_replicas.Count} replicas");
        }

        public QuantumDatabase GetReadReplica()
        {
            if (_replicas.Count == 0) return _primary;
            var random = new Random();
            return _replicas[random.Next(_replicas.Count)];
        }
    }
}
