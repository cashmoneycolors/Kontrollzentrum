using System;
using System.Collections.Generic;
using System.Linq;
using System.Threading.Tasks;

namespace DropshippingApp.Services
{
    public class BatchProcessor
    {
        private readonly int _batchSize = 100;
        private readonly LoggingService _logger = new();

        public async Task<List<T>> ProcessBatch<T>(List<T> items, Func<T, Task<T>> processor)
        {
            var results = new List<T>();
            for (int i = 0; i < items.Count; i += _batchSize)
            {
                var batch = items.Skip(i).Take(_batchSize).ToList();
                var tasks = batch.Select(processor).ToList();
                var processed = await Task.WhenAll(tasks);
                results.AddRange(processed);
            }
            return results;
        }

        public async Task<Dictionary<string, object>> ParallelExecute(Dictionary<string, Func<Task<object>>> tasks)
        {
            var results = new Dictionary<string, object>();
            var taskList = tasks.Select(async t => new { Key = t.Key, Value = await t.Value() }).ToList();
            var completed = await Task.WhenAll(taskList);
            foreach (var item in completed) results[item.Key] = item.Value;
            return results;
        }
    }
}
