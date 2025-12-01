using System.Collections.ObjectModel;
using System.Threading.Tasks;
using Kontrollzentrum.Services;

namespace Kontrollzentrum.ViewModels
{
    public class ModulesViewModel : ViewModelBase
    {
        private readonly ModuleService _service;
        private bool _isBusy;

        public ObservableCollection<string> Modules { get; } = new();

        public bool IsBusy
        {
            get => _isBusy;
            set => SetProperty(ref _isBusy, value);
        }

        public ModulesViewModel(ModuleService service)
        {
            _service = service;
            LoadModules();
        }

        private void LoadModules()
        {
            Modules.Add("✅ apikey_manager");
            Modules.Add("✅ auto_distribute");
            Modules.Add("✅ beispiel_modul");
            Modules.Add("✅ dashboard_modul");
            Modules.Add("✅ data_import");
            Modules.Add("✅ dropshipping_modul");
            Modules.Add("✅ grafik_design_modul");
            Modules.Add("✅ ki_integration_modul");
            Modules.Add("✅ ki_modul");
            Modules.Add("✅ nft_manager");
            Modules.Add("✅ nft_modul");
            Modules.Add("✅ payment");
            Modules.Add("✅ self_heal");
            Modules.Add("✅ TEMPLATE_modul");
            Modules.Add("✅ wetter_modul");
        }

        public async Task RunAllAsync()
        {
            if (IsBusy) return;
            IsBusy = true;
            try
            {
                await _service.RunModuleAsync("all");
            }
            finally
            {
                IsBusy = false;
            }
        }
    }
}
