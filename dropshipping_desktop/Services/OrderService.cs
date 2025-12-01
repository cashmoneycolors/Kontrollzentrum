using System;
using System.Collections.Generic;
using System.Linq;

namespace DropshippingApp.Services
{
    public class OrderService
    {
        private List<Order> _orders = new();
        private int _counter = 1000;
        private readonly LoggingService _logger = new();

        public Order CreateOrder(string email, decimal total)
        {
            if (string.IsNullOrWhiteSpace(email) || total <= 0)
            {
                _logger.LogWarning($"Invalid order: {email}, {total}");
                return null;
            }

            var order = new Order
            {
                OrderId = $"ORD-{_counter++}",
                CustomerEmail = email,
                Total = decimal.Round(total, 2),
                Status = "Pending",
                CreatedAt = DateTime.Now
            };

            _orders.Add(order);
            _logger.LogInfo($"Order created: {order.OrderId}");
            return order;
        }

        public Order UpdateStatus(string orderId, string status, string tracking = null)
        {
            var order = _orders.FirstOrDefault(o => o.OrderId == orderId);
            if (order == null)
            {
                _logger.LogWarning($"Order not found: {orderId}");
                return null;
            }

            order.Status = status;
            if (!string.IsNullOrWhiteSpace(tracking))
                order.Tracking = tracking;

            _logger.LogInfo($"Order updated: {orderId} → {status}");
            return order;
        }

        public List<Order> GetAll() => _orders;
        public List<Order> GetPending() => _orders.Where(o => o.Status == "Pending").ToList();
        public List<Order> GetShipped() => _orders.Where(o => o.Status == "Shipped").ToList();
        public Order GetById(string orderId) => _orders.FirstOrDefault(o => o.OrderId == orderId);
        public decimal GetTotalRevenue() => _orders.Sum(o => o.Total);
    }

    public class Order
    {
        public string OrderId { get; set; }
        public string CustomerEmail { get; set; }
        public decimal Total { get; set; }
        public string Status { get; set; }
        public string Tracking { get; set; }
        public DateTime CreatedAt { get; set; }
    }
}
