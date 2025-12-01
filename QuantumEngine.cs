using System;
using System.Collections.Generic;
using System.Linq;
using System.Threading.Tasks;

namespace Kontrollzentrum.Quantum
{
    public class QuantumEngine
    {
        private List<Worker> _workers;
        private Queue<Operation> _operationQueue;
        private Dictionary<string, OperationResult> _results;

        public QuantumEngine(int workerCount = 8)
        {
            _workers = Enumerable.Range(0, workerCount)
                .Select(i => new Worker($"Worker-{i}"))
                .ToList();
            _operationQueue = new Queue<Operation>();
            _results = new Dictionary<string, OperationResult>();
        }

        public async Task<OperationResult> ExecuteAsync(Operation op)
        {
            var worker = _workers.FirstOrDefault(w => !w.IsBusy);
            if (worker == null)
            {
                _operationQueue.Enqueue(op);
                return await WaitForWorkerAsync(op);
            }

            return await worker.ExecuteAsync(op);
        }

        public async Task<List<OperationResult>> ExecuteParallelAsync(List<Operation> ops)
        {
            var tasks = ops.Select(op => ExecuteAsync(op)).ToList();
            var results = await Task.WhenAll(tasks);
            return results.ToList();
        }

        private async Task<OperationResult> WaitForWorkerAsync(Operation op)
        {
            while (_workers.All(w => w.IsBusy))
                await Task.Delay(10);
            
            var worker = _workers.First(w => !w.IsBusy);
            return await worker.ExecuteAsync(op);
        }

        public class Worker
        {
            public string Id { get; }
            public bool IsBusy { get; private set; }

            public Worker(string id) => Id = id;

            public async Task<OperationResult> ExecuteAsync(Operation op)
            {
                IsBusy = true;
                try
                {
                    var result = await op.ExecuteAsync();
                    return result;
                }
                finally
                {
                    IsBusy = false;
                }
            }
        }
    }

    public class Operation
    {
        public string Id { get; set; }
        public string Type { get; set; }
        public Dictionary<string, object> Parameters { get; set; }

        public async Task<OperationResult> ExecuteAsync()
        {
            await Task.Delay(100);
            return new OperationResult { Id = Id, Success = true, Duration = 100 };
        }
    }

    public class OperationResult
    {
        public string Id { get; set; }
        public bool Success { get; set; }
        public int Duration { get; set; }
        public string Error { get; set; }
    }
}
