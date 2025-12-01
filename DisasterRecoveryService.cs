using System;
using System.IO;
using System.Threading.Tasks;
using System.Collections.Generic;

namespace Kontrollzentrum.DisasterRecovery
{
    public class DisasterRecoveryService
    {
        private string _backupPath;
        private List<BackupMetadata> _backups;

        public DisasterRecoveryService(string backupPath = "backups")
        {
            _backupPath = backupPath;
            _backups = new List<BackupMetadata>();
            Directory.CreateDirectory(_backupPath);
        }

        public async Task<BackupResult> CreateBackupAsync(string sourcePath)
        {
            var timestamp = DateTime.UtcNow.ToString("yyyyMMdd_HHmmss");
            var backupDir = Path.Combine(_backupPath, $"backup_{timestamp}");
            
            try
            {
                Directory.CreateDirectory(backupDir);
                CopyDirectory(sourcePath, backupDir);

                var metadata = new BackupMetadata
                {
                    Id = Guid.NewGuid().ToString(),
                    Timestamp = DateTime.UtcNow,
                    SourcePath = sourcePath,
                    BackupPath = backupDir,
                    Status = "Completed",
                    Size = GetDirectorySize(backupDir)
                };

                _backups.Add(metadata);
                return new BackupResult { Success = true, BackupId = metadata.Id, Path = backupDir };
            }
            catch (Exception ex)
            {
                return new BackupResult { Success = false, Error = ex.Message };
            }
        }

        public async Task<RestoreResult> RestoreBackupAsync(string backupId, string targetPath)
        {
            var backup = _backups.Find(b => b.Id == backupId);
            if (backup == null)
                return new RestoreResult { Success = false, Error = "Backup not found" };

            try
            {
                if (Directory.Exists(targetPath))
                    Directory.Delete(targetPath, true);
                
                CopyDirectory(backup.BackupPath, targetPath);
                return new RestoreResult { Success = true, RestoredPath = targetPath };
            }
            catch (Exception ex)
            {
                return new RestoreResult { Success = false, Error = ex.Message };
            }
        }

        public List<BackupMetadata> GetBackups() => _backups;

        private void CopyDirectory(string source, string destination)
        {
            var dir = new DirectoryInfo(source);
            foreach (var file in dir.GetFiles())
                file.CopyTo(Path.Combine(destination, file.Name), true);
            
            foreach (var subdir in dir.GetDirectories())
                CopyDirectory(subdir.FullName, Path.Combine(destination, subdir.Name));
        }

        private long GetDirectorySize(string path)
        {
            var dir = new DirectoryInfo(path);
            return dir.EnumerateFiles("*", SearchOption.AllDirectories)
                .Sum(f => f.Length);
        }
    }

    public class BackupMetadata
    {
        public string Id { get; set; }
        public DateTime Timestamp { get; set; }
        public string SourcePath { get; set; }
        public string BackupPath { get; set; }
        public string Status { get; set; }
        public long Size { get; set; }
    }

    public class BackupResult
    {
        public bool Success { get; set; }
        public string BackupId { get; set; }
        public string Path { get; set; }
        public string Error { get; set; }
    }

    public class RestoreResult
    {
        public bool Success { get; set; }
        public string RestoredPath { get; set; }
        public string Error { get; set; }
    }
}
