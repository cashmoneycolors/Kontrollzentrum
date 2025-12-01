using DropshippingApp.Models;
using System.Collections.Generic;
using System.Linq;

namespace DropshippingApp.Services
{
    public class AmazonService
    {
        public List<Product> SearchProducts(string query)
        {
            return new List<Product>
            {
                new Product
                {
                    Asin = "B001",
                    Title = $"Premium {query} - 100% Original",
                    Price = 29.99m,
                    Rating = 4.8m,
                    Supplier = "alibaba",
                    SupplierPrice = 8.50m,
                    SellingPrice = 34.99m,
                    Profit = 23.34m,
                    Margin = 33.3m
                },
                new Product
                {
                    Asin = "B002",
                    Title = $"Budget {query} - Best Value",
                    Price = 14.99m,
                    Rating = 4.5m,
                    Supplier = "dhgate",
                    SupplierPrice = 5.00m,
                    SellingPrice = 19.99m,
                    Profit = 12.49m,
                    Margin = 37.5m
                },
                new Product
                {
                    Asin = "B003",
                    Title = $"Professional {query} - Pro Edition",
                    Price = 49.99m,
                    Rating = 4.9m,
                    Supplier = "1688",
                    SupplierPrice = 15.00m,
                    SellingPrice = 59.99m,
                    Profit = 39.99m,
                    Margin = 40.0m
                }
            };
        }

        public Product GetProductDetails(string asin)
        {
            return new Product
            {
                Asin = asin,
                Title = "Demo Product",
                Price = 29.99m,
                Rating = 4.7m,
                Supplier = "alibaba",
                SupplierPrice = 8.50m,
                SellingPrice = 34.99m,
                Profit = 23.34m,
                Margin = 33.3m
            };
        }
    }
}
