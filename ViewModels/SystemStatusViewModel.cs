using System.Collections.ObjectModel;
using System.Threading.Tasks;
using Kontrollzentrum.Services;

namespace Kontrollzentrum.ViewModels
{
    public class SystemStatusViewModel : ViewModelBase
    {
        private readonly ModuleService _service;
        private string _lastRun = string.Empty;
        private bool _isBusy;

        public ObservableCollection<string> Entries { get; } = new();

        public string LastRun
        {
            get => _lastRun;
            set => SetProperty(ref _lastRun, value);
        }

        public bool IsBusy
        {
            get => _isBusy;
            set => SetProperty(ref _isBusy, value);
        }

        public SystemStatusViewModel(ModuleService service)
        {
            _service = service;
        }

        public async Task RefreshAsync()
        {
            if (IsBusy) return;
            IsBusy = true;
            try
            {
                var status = await _service.GetStatusAsync().ConfigureAwait(false);
                await App.Current.Dispatcher.InvokeAsync(() =>
                {
                    Entries.Clear();
                    foreach (var entry in status.Entries)
                    {
                        Entries.Add(entry);
                    }
                });
                LastRun = status.LastRun;
            }
            finally
            {
                IsBusy = false;
            }
        }
    }
}