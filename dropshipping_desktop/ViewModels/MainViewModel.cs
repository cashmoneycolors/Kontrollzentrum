using CommunityToolkit.Mvvm.ComponentModel;
using CommunityToolkit.Mvvm.Input;
using DropshippingApp.Models;
using DropshippingApp.Services;
using System.Collections.ObjectModel;
using System.Threading.Tasks;
using System.Windows.Threading;

namespace DropshippingApp.ViewModels
{
    public partial class MainViewModel : ObservableObject
    {
        private readonly AmazonService _amazonService = new();
        private readonly PricingService _pricingService = new();
        private readonly OrderService _orderService = new();
        private readonly GoogleService _googleService = new();
        private readonly LiveDataService _liveDataService = new();
        private DispatcherTimer _liveDataTimer;

        [ObservableProperty]
        private string searchQuery = "";

        [ObservableProperty]
        private ObservableCollection<Product> products = new();

        [ObservableProperty]
        private ObservableCollection<Order> orders = new();

        [ObservableProperty]
        private ObservableCollection<GoogleSearchResult> googleResults = new();

        [ObservableProperty]
        private ObservableCollection<LiveMarketData> liveMarketData = new();

        [ObservableProperty]
        private decimal supplierPrice = 10m;

        [ObservableProperty]
        private decimal targetMargin = 35m;

        [ObservableProperty]
        private PricingResult pricingResult;

        [ObservableProperty]
        private int totalOrders = 0;

        [ObservableProperty]
        private int pendingOrders = 0;

        [ObservableProperty]
        private decimal totalRevenue = 0m;

        [ObservableProperty]
        private decimal revenuePerHour = 5000m;

        [ObservableProperty]
        private int activeClones = 1000;

        public MainViewModel()
        {
            StartLiveDataUpdates();
        }

        private void StartLiveDataUpdates()
        {
            _liveDataTimer = new DispatcherTimer();
            _liveDataTimer.Interval = System.TimeSpan.FromSeconds(2);
            _liveDataTimer.Tick += async (s, e) => await UpdateLiveData();
            _liveDataTimer.Start();
        }

        private async Task UpdateLiveData()
        {
            var marketData = await _liveDataService.GetLiveMarketData();
            LiveMarketData.Clear();
            foreach (var item in marketData)
            {
                LiveMarketData.Add(item);
            }

            var stats = await _liveDataService.GetLiveStats();
            TotalOrders = stats.TotalOrders;
            TotalRevenue = stats.TotalRevenue;
            RevenuePerHour = stats.RevenuePerHour;
            ActiveClones = stats.ActiveClones;
        }

        [RelayCommand]
        public async Task SearchProducts()
        {
            if (string.IsNullOrWhiteSpace(SearchQuery)) return;

            // Search Amazon
            var amazonResults = _amazonService.SearchProducts(SearchQuery);
            Products.Clear();
            foreach (var product in amazonResults)
            {
                Products.Add(product);
            }

            // Search Google
            var googleResults = await _googleService.SearchGoogle(SearchQuery);
            GoogleResults.Clear();
            foreach (var result in googleResults)
            {
                GoogleResults.Add(result);
            }
        }

        [RelayCommand]
        public void CalculatePrice()
        {
            if (SupplierPrice <= 0) return;
            PricingResult = _pricingService.CalculatePrice(SupplierPrice, TargetMargin / 100);
        }

        [RelayCommand]
        public void CreateOrder(string email)
        {
            if (PricingResult == null) return;
            var order = _orderService.CreateOrder(email, PricingResult.SellingPrice);
            Orders.Add(order);
            TotalOrders++;
            PendingOrders++;
            TotalRevenue += order.Total;
        }

        [RelayCommand]
        public void FulfillOrder(string orderId)
        {
            var order = _orderService.UpdateOrderStatus(orderId, "Shipped", $"TRACK-{orderId}");
            if (order != null)
            {
                PendingOrders--;
            }
        }

        public void RefreshStats()
        {
            TotalOrders = Orders.Count;
            PendingOrders = Orders.Count(o => o.Status == "Pending");
        }
    }
}
