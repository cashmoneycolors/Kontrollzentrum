using System;

namespace DropshippingApp.Services
{
    public class PricingService
    {
        private const decimal ShippingCost = 2.50m;
        private const decimal PlatformFee = 0.15m;
        private const decimal MinMargin = 0.15m;
        private const decimal MaxMargin = 0.60m;

        public PricingResult CalculatePrice(decimal cost, decimal targetMargin)
        {
            if (cost <= 0) return new PricingResult { Error = "Invalid cost" };

            // Validate margin
            var margin = Math.Max(MinMargin, Math.Min(MaxMargin, targetMargin));
            
            var totalCost = cost + ShippingCost + PlatformFee;
            var sellingPrice = totalCost / (1 - margin);
            var profit = sellingPrice - totalCost;
            var actualMargin = (profit / sellingPrice) * 100;

            return new PricingResult
            {
                Cost = cost,
                Shipping = ShippingCost,
                PlatformFee = PlatformFee,
                TotalCost = decimal.Round(totalCost, 2),
                SellingPrice = decimal.Round(sellingPrice, 2),
                Profit = decimal.Round(profit, 2),
                MarginPercent = decimal.Round(actualMargin, 2),
                IsValid = profit > 0
            };
        }

        public decimal GetCompetitivePrice(decimal marketPrice, int competitors = 3)
        {
            var discount = 0.02m * (competitors - 1);
            return decimal.Round(marketPrice * (1 - discount), 2);
        }

        public bool IsProfitable(PricingResult result)
        {
            return result.IsValid && result.Profit > 0 && result.MarginPercent >= 15;
        }
    }

    public class PricingResult
    {
        public decimal Cost { get; set; }
        public decimal Shipping { get; set; }
        public decimal PlatformFee { get; set; }
        public decimal TotalCost { get; set; }
        public decimal SellingPrice { get; set; }
        public decimal Profit { get; set; }
        public decimal MarginPercent { get; set; }
        public bool IsValid { get; set; }
        public string Error { get; set; }
    }
}
