using System;
using System.Collections.Generic;
using System.Linq;
using System.Threading.Tasks;

namespace DropshippingApp.Services
{
    public class AutonomousOptimizer
    {
        private readonly QuantumDatabase _db;
        private readonly PerformanceOptimizer _perf;
        private readonly LoggingService _logger = new();
        private Timer _optimizationTimer;

        public AutonomousOptimizer(QuantumDatabase db, PerformanceOptimizer perf)
        {
            _db = db;
            _perf = perf;
            StartAutoOptimization();
        }

        private void StartAutoOptimization()
        {
            _optimizationTimer = new Timer(_ => OptimizeAsync(), null, TimeSpan.Zero, TimeSpan.FromMinutes(5));
        }

        private async Task OptimizeAsync()
        {
            try
            {
                var stats = _db.GetQueryStats();
                var slowQueries = stats.Where(x => x.Value.TotalTime > 1000).ToList();
                
                if (slowQueries.Any())
                {
                    _logger.LogWarning($"Found {slowQueries.Count} slow queries");
                    _db.OptimizeIndexes();
                }

                var metrics = _perf.GetMetrics();
                var avgLatency = metrics.Values.Average();
                if (avgLatency > 100)
                    _logger.LogWarning($"High latency detected: {avgLatency}ms");

                _logger.LogInfo("Auto-optimization completed");
            }
            catch (Exception ex)
            {
                _logger.LogError("Optimization Error", ex);
            }
        }

        public void Stop() => _optimizationTimer?.Dispose();
    }
}
