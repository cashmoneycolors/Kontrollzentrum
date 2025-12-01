using System;
using System.Collections.Generic;
using System.Linq;
using System.Net.Http;
using System.Threading.Tasks;
using Newtonsoft.Json.Linq;

namespace DropshippingApp.Services
{
    public class GoogleService
    {
        private readonly string _apiKey = Environment.GetEnvironmentVariable("GOOGLE_API_KEY") ?? "demo";
        private readonly string _searchEngineId = Environment.GetEnvironmentVariable("GOOGLE_SEARCH_ENGINE_ID") ?? "demo";
        private readonly HttpClient _client = new();
        private readonly LoggingService _logger = new();

        public async Task<List<GoogleSearchResult>> SearchGoogle(string query)
        {
            if (string.IsNullOrWhiteSpace(query)) return new();

            try
            {
                if (_apiKey == "demo") return GetDemoResults(query);

                var url = $"https://www.googleapis.com/customsearch/v1?q={query}&key={_apiKey}&cx={_searchEngineId}";
                var response = await _client.GetAsync(url);
                
                if (!response.IsSuccessStatusCode) return GetDemoResults(query);

                var json = await response.Content.ReadAsStringAsync();
                var data = JObject.Parse(json);
                var items = data["items"] as JArray;

                return items?.Select(item => new GoogleSearchResult
                {
                    Title = item["title"]?.ToString() ?? "",
                    Url = item["link"]?.ToString() ?? "",
                    Snippet = item["snippet"]?.ToString() ?? "",
                    Price = ExtractPrice(item["snippet"]?.ToString() ?? "")
                }).ToList() ?? new();
            }
            catch (Exception ex)
            {
                _logger.LogError("Google Search Error", ex);
                return GetDemoResults(query);
            }
        }

        public async Task<List<GoogleTrendData>> GetTrends(string category)
        {
            return await Task.FromResult(new List<GoogleTrendData>
            {
                new() { Keyword = "Wireless Headphones", Volume = 15000, Growth = 25 },
                new() { Keyword = "Phone Case", Volume = 12000, Growth = 18 },
                new() { Keyword = "USB Cable", Volume = 8000, Growth = 12 }
            });
        }

        private List<GoogleSearchResult> GetDemoResults(string query)
        {
            return new()
            {
                new() { Title = $"Amazon - {query}", Url = $"https://amazon.com/s?k={query}", Snippet = $"Find {query} on Amazon", Price = 29.99m },
                new() { Title = $"eBay - {query}", Url = $"https://ebay.com/sch/i.html?_nkw={query}", Snippet = $"Buy {query} on eBay", Price = 24.99m },
                new() { Title = $"Alibaba - {query}", Url = $"https://alibaba.com/trade/search", Snippet = $"Wholesale {query}", Price = 8.50m }
            };
        }

        private decimal ExtractPrice(string text)
        {
            var match = System.Text.RegularExpressions.Regex.Match(text, @"\$(\d+\.?\d*)");
            return match.Success ? decimal.Parse(match.Groups[1].Value) : 0m;
        }
    }

    public class GoogleSearchResult
    {
        public string Title { get; set; }
        public string Url { get; set; }
        public string Snippet { get; set; }
        public decimal Price { get; set; }
    }

    public class GoogleTrendData
    {
        public string Keyword { get; set; }
        public int Volume { get; set; }
        public int Growth { get; set; }
    }
}
