using System;
using System.Collections.Generic;
using System.Diagnostics;
using System.Threading.Tasks;

namespace Kontrollzentrum.Monitoring
{
    public class MonitoringService
    {
        private PerformanceCounter _cpuCounter;
        private PerformanceCounter _memoryCounter;
        private List<MetricSnapshot> _metrics;

        public MonitoringService()
        {
            _cpuCounter = new PerformanceCounter("Processor", "% Processor Time", "_Total");
            _memoryCounter = new PerformanceCounter("Memory", "% Committed Bytes In Use");
            _metrics = new List<MetricSnapshot>();
        }

        public async Task<SystemMetrics> GetMetricsAsync()
        {
            var cpu = _cpuCounter.NextValue();
            var memory = _memoryCounter.NextValue();
            var process = Process.GetCurrentProcess();

            var metrics = new SystemMetrics
            {
                Timestamp = DateTime.UtcNow,
                CpuUsage = cpu,
                MemoryUsage = memory,
                ProcessMemory = process.WorkingSet64 / (1024 * 1024),
                ThreadCount = process.Threads.Count,
                HealthScore = CalculateHealthScore(cpu, memory)
            };

            _metrics.Add(new MetricSnapshot { Timestamp = DateTime.UtcNow, Metrics = metrics });
            return metrics;
        }

        public List<MetricSnapshot> GetMetricsHistory(int minutes = 60)
        {
            var cutoff = DateTime.UtcNow.AddMinutes(-minutes);
            return _metrics.FindAll(m => m.Timestamp > cutoff);
        }

        private int CalculateHealthScore(float cpu, float memory)
        {
            var score = 100;
            if (cpu > 80) score -= 20;
            else if (cpu > 60) score -= 10;
            
            if (memory > 80) score -= 20;
            else if (memory > 60) score -= 10;
            
            return Math.Max(0, score);
        }
    }

    public class SystemMetrics
    {
        public DateTime Timestamp { get; set; }
        public float CpuUsage { get; set; }
        public float MemoryUsage { get; set; }
        public long ProcessMemory { get; set; }
        public int ThreadCount { get; set; }
        public int HealthScore { get; set; }
    }

    public class MetricSnapshot
    {
        public DateTime Timestamp { get; set; }
        public SystemMetrics Metrics { get; set; }
    }
}
