namespace DropshippingApp.Models
{
    public class Product
    {
        public string Asin { get; set; }
        public string Title { get; set; }
        public decimal Price { get; set; }
        public decimal Rating { get; set; }
        public string Supplier { get; set; }
        public decimal SupplierPrice { get; set; }
        public decimal SellingPrice { get; set; }
        public decimal Profit { get; set; }
        public decimal Margin { get; set; }
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

    public class PricingResult
    {
        public decimal Cost { get; set; }
        public decimal Shipping { get; set; }
        public decimal PlatformFee { get; set; }
        public decimal TotalCost { get; set; }
        public decimal SellingPrice { get; set; }
        public decimal Profit { get; set; }
        public decimal MarginPercent { get; set; }
    }
}
