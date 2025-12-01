using System;
using System.Collections.Generic;
using System.Linq;
using System.Threading;
using System.Threading.Tasks;

namespace DropshippingApp.Services
{
    public class LiveDataService
    {
        private Random _random = new();
        private List<LiveMarketData> _marketData = new();
        private List<LiveOrderData> _orderData = new();

        public LiveDataService()
        {
            InitializeLiveData();
        }

        private void InitializeLiveData()
        {
            _marketData = new List<LiveMarketData>
            {
                new LiveMarketData { Product = "Wireless Headphones", Price = 29.99m, Trend = "↑ +5%", Volume = 1250 },
                new LiveMarketData { Product = "Phone Case", Price = 12.99m, Trend = "↓ -2%", Volume = 890 },
                new LiveMarketData { Product = "USB Cable", Price = 5.99m, Trend = "→ 0%", Volume = 2100 },
                new LiveMarketData { Product = "Power Bank", Price = 24.99m, Trend = "↑ +8%", Volume = 1560 },
                new LiveMarketData { Product = "Screen Protector", Price = 8.99m, Trend = "↑ +3%", Volume = 750 }
            };

            _orderData = new List<LiveOrderData>
            {
                new LiveOrderData { OrderId = "ORD-1001", Status = "Processing", Amount = 34.99m, Time = DateTime.Now.AddMinutes(-5) },
                new LiveOrderData { OrderId = "ORD-1002", Status = "Shipped", Amount = 45.50m, Time = DateTime.Now.AddMinutes(-15) },
                new LiveOrderData { OrderId = "ORD-1003", Status = "Delivered", Amount = 28.75m, Time = DateTime.Now.AddMinutes(-45) }
            };
        }

        public async Task<List<LiveMarketData>> GetLiveMarketData()
        {
            // Update prices in real-time
            foreach (var item in _marketData)
            {
                var change = _random.Next(-3, 4) * 0.01m;
                item.Price += change;
                item.Volume += _random.Next(-100, 200);
                item.Trend = change > 0 ? $"↑ +{Math.Abs(change):P1}" : change < 0 ? $"↓ {change:P1}" : "→ 0%";
            }

            return await Task.FromResult(_marketData);
        }

        public async Task<List<LiveOrderData>> GetLiveOrders()
        {
            // Simulate new orders
            if (_random.Next(0, 3) == 0)
            {
                _orderData.Insert(0, new LiveOrderData
                {
                    OrderId = $"ORD-{1000 + _random.Next(1, 1000)}",
                    Status = "Processing",
                    Amount = (decimal)(_random.Next(20, 100) + _random.NextDouble()),
                    Time = DateTime.Now
                });

                if (_orderData.Count > 10)
                    _orderData.RemoveAt(_orderData.Count - 1);
            }

            return await Task.FromResult(_orderData);
        }

        public async Task<DashboardStats> GetLiveStats()
        {
            var totalOrders = _orderData.Count;
            var totalRevenue = _orderData.Sum(o => o.Amount);
            var avgOrderValue = totalOrders > 0 ? totalRevenue / totalOrders : 0;

            return await Task.FromResult(new DashboardStats
            {
                TotalOrders = totalOrders,
                TotalRevenue = totalRevenue,
                AverageOrderValue = avgOrderValue,
                ActiveClones = 1000,
                RevenuePerHour = 5000m,
                OrdersPerDay = 2500,
                Timestamp = DateTime.Now
            });
        }
    }

    public class LiveMarketData
    {
        public string Product { get; set; }
        public decimal Price { get; set; }
        public string Trend { get; set; }
        public int Volume { get; set; }
    }

    public class LiveOrderData
    {
        public string OrderId { get; set; }
        public string Status { get; set; }
        public decimal Amount { get; set; }
        public DateTime Time { get; set; }
    }

    public class DashboardStats
    {
        public int TotalOrders { get; set; }
        public decimal TotalRevenue { get; set; }
        public decimal AverageOrderValue { get; set; }
        public int ActiveClones { get; set; }
        public decimal RevenuePerHour { get; set; }
        public int OrdersPerDay { get; set; }
        public DateTime Timestamp { get; set; }
    }
}
