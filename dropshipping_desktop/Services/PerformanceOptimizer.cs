using System;
using System.Collections.Generic;
using System.Diagnostics;
using System.Linq;

namespace DropshippingApp.Services
{
    public class PerformanceOptimizer
    {
        private Dictionary<string, PerformanceMetric> _metrics = new();
        private LoggingService _logger = new();

        public void StartTimer(string key) => _metrics[key] = new PerformanceMetric { StartTime = DateTime.Now };

        public long EndTimer(string key)
        {
            if (!_metrics.ContainsKey(key)) return 0;
            var metric = _metrics[key];
            metric.Duration = (long)(DateTime.Now - metric.StartTime).TotalMilliseconds;
            if (metric.Duration > 1000) _logger.LogWarning($"Slow operation: {key} - {metric.Duration}ms");
            return metric.Duration;
        }

        public Dictionary<string, long> GetMetrics() => _metrics.ToDictionary(x => x.Key, x => x.Value.Duration);

        public void OptimizeQuery<T>(List<T> items, Func<T, bool> predicate)
        {
            var sw = Stopwatch.StartNew();
            var result = items.Where(predicate).ToList();
            sw.Stop();
            if (sw.ElapsedMilliseconds > 100) _logger.LogWarning($"Slow query: {sw.ElapsedMilliseconds}ms");
        }

        private class PerformanceMetric { public DateTime StartTime { get; set; } public long Duration { get; set; } }
    }
}
