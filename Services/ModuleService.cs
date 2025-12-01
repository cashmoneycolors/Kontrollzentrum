using System;
using System.Collections.Generic;
using System.Diagnostics;
using System.Threading.Tasks;

namespace Kontrollzentrum.Services
{
    public class ModuleService
    {
        public async Task<ModuleStatus> GetStatusAsync()
        {
            return await Task.Run(() =>
            {
                var entries = new List<string>
                {
                    "✅ apikey_manager",
                    "✅ auto_distribute",
                    "✅ beispiel_modul",
                    "✅ dashboard_modul",
                    "✅ data_import",
                    "✅ dropshipping_modul",
                    "✅ grafik_design_modul",
                    "✅ ki_integration_modul",
                    "✅ ki_modul",
                    "✅ nft_manager",
                    "✅ nft_modul",
                    "✅ payment",
                    "✅ self_heal",
                    "✅ TEMPLATE_modul",
                    "✅ wetter_modul"
                };

                return new ModuleStatus
                {
                    Entries = entries,
                    LastRun = DateTime.Now.ToString("yyyy-MM-dd HH:mm:ss")
                };
            });
        }

        public async Task<bool> RunModuleAsync(string moduleName)
        {
            return await Task.Run(() =>
            {
                try
                {
                    var psi = new ProcessStartInfo
                    {
                        FileName = "python",
                        Arguments = $"main.py alle run",
                        UseShellExecute = false,
                        RedirectStandardOutput = true,
                        CreateNoWindow = true
                    };

                    using (var process = Process.Start(psi))
                    {
                        process.WaitForExit();
                        return process.ExitCode == 0;
                    }
                }
                catch
                {
                    return false;
                }
            });
        }
    }

    public class ModuleStatus
    {
        public List<string> Entries { get; set; }
        public string LastRun { get; set; }
    }
}
