using System;
using System.Collections.Generic;
using System.Threading.Tasks;

namespace DropshippingApp.Services
{
    public class StripeService
    {
        private readonly string _apiKey = Environment.GetEnvironmentVariable("STRIPE_API_KEY") ?? "sk_test_demo";
        private readonly LoggingService _logger = new();
        private Dictionary<string, PaymentResult> _payments = new();

        public async Task<PaymentResult> ProcessPayment(string email, decimal amount, string orderId)
        {
            if (amount <= 0 || string.IsNullOrWhiteSpace(email))
            {
                _logger.LogWarning($"Invalid payment: {email}, {amount}");
                return new PaymentResult { Success = false, Error = "Invalid amount or email" };
            }

            try
            {
                var result = new PaymentResult
                {
                    Success = true,
                    TransactionId = $"txn_{Guid.NewGuid().ToString().Substring(0, 8)}",
                    Amount = decimal.Round(amount, 2),
                    Email = email,
                    OrderId = orderId,
                    Timestamp = DateTime.Now
                };

                _payments[result.TransactionId] = result;
                _logger.LogInfo($"Payment processed: {result.TransactionId} - ${amount:F2}");
                return await Task.FromResult(result);
            }
            catch (Exception ex)
            {
                _logger.LogError("Payment Error", ex);
                return new PaymentResult { Success = false, Error = ex.Message };
            }
        }

        public async Task<bool> RefundPayment(string transactionId, decimal amount)
        {
            if (!_payments.ContainsKey(transactionId))
            {
                _logger.LogWarning($"Transaction not found: {transactionId}");
                return false;
            }

            try
            {
                _payments.Remove(transactionId);
                _logger.LogInfo($"Refund processed: {transactionId} - ${amount:F2}");
                return await Task.FromResult(true);
            }
            catch (Exception ex)
            {
                _logger.LogError("Refund Error", ex);
                return false;
            }
        }

        public PaymentResult GetPayment(string transactionId)
        {
            return _payments.ContainsKey(transactionId) ? _payments[transactionId] : null;
        }
    }

    public class PaymentResult
    {
        public bool Success { get; set; }
        public string TransactionId { get; set; }
        public decimal Amount { get; set; }
        public string Email { get; set; }
        public string OrderId { get; set; }
        public DateTime Timestamp { get; set; }
        public string Error { get; set; }
    }
}
