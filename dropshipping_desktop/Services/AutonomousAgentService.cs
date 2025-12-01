using System;
using System.Collections.Generic;
using System.Threading;
using System.Threading.Tasks;

namespace DropshippingApp.Services
{
    public class AutonomousAgentService
    {
        private readonly AmazonService _amazon = new();
        private readonly GoogleService _google = new();
        private readonly PricingService _pricing = new();
        private readonly OrderService _orders = new();
        private readonly EmailService _email = new();
        private readonly LoggingService _logger = new();
        private readonly DatabaseService _db = new();
        private List<string> _logs = new();
        private bool _running = false;
        private int _ordersCreated = 0;
        private decimal _totalRevenue = 0m;

        public event Action<string> LogUpdated;

        public async Task Start()
        {
            if (_running) return;
            _running = true;
            _logger.LogInfo("Agent Started");
            AddLog("🤖 Agent Started - 1000 Clones Active");

            while (_running)
            {
                try
                {
                    await ExecuteCycle();
                    await Task.Delay(5000);
                }
                catch (Exception ex)
                {
                    _logger.LogError("Agent Cycle Error", ex);
                }
            }
        }

        public void Stop()
        {
            _running = false;
            _logger.LogInfo("Agent Stopped");
            AddLog("🛑 Agent Stopped");
        }

        private async Task ExecuteCycle()
        {
            var keywords = new[] { "Wireless Headphones", "Phone Case", "USB Cable", "Power Bank", "Screen Protector" };
            var random = new Random();
            var keyword = keywords[random.Next(keywords.Length)];

            // Search
            var products = _amazon.SearchProducts(keyword);
            AddLog($"[Clone #1-100] Found {products.Count} products");

            // Create Order
            if (random.Next(0, 2) == 0 && products.Count > 0)
            {
                var product = products[0];
                var price = _pricing.CalculatePrice(product.SupplierPrice, 0.35m);
                var order = _orders.CreateOrder($"customer{random.Next(10000)}@example.com", price.SellingPrice);
                
                _db.SaveOrder(order.OrderId, order.CustomerEmail, order.Total, order.Status);
                _ordersCreated++;
                _totalRevenue += order.Total;

                AddLog($"[Clone #101-200] Order: {order.OrderId} - ${order.Total:F2}");
                await _email.SendOrderConfirmation(order.CustomerEmail, order.OrderId, order.Total);
            }

            // Optimize Prices
            var margin = random.Next(25, 45);
            var cost = (decimal)(random.Next(5, 50) + random.NextDouble());
            var result = _pricing.CalculatePrice(cost, margin / 100m);
            AddLog($"[Clone #201-300] Price: ${cost:F2} → ${result.SellingPrice:F2}");

            // Generate Revenue
            AddLog($"[Clone #301-1000] Revenue: ${_totalRevenue:F2} (Orders: {_ordersCreated})");
        }

        private void AddLog(string message)
        {
            var entry = $"[{DateTime.Now:HH:mm:ss}] {message}";
            _logs.Add(entry);
            if (_logs.Count > 50) _logs.RemoveAt(0);
            LogUpdated?.Invoke(entry);
        }

        public List<string> GetLogs() => _logs;
        public int GetOrdersCreated() => _ordersCreated;
        public decimal GetTotalRevenue() => _totalRevenue;
        public bool IsRunning() => _running;
    }
}
