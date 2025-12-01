using DropshippingApp.ViewModels;
using System.Windows;

namespace DropshippingApp
{
    public partial class MainWindow : Window
    {
        public MainWindow()
        {
            InitializeComponent();
            DataContext = new MainViewModel();
        }
    }
}
