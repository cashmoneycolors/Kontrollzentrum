using System;
using System.IO;

namespace DropshippingApp.Services
{
    public class LoggingService
    {
        private readonly string _logFile = "logs.txt";

        public void Log(string message)
        {
            var timestamp = DateTime.Now.ToString("yyyy-MM-dd HH:mm:ss");
            var logEntry = $"[{timestamp}] {message}";
            
            try
            {
                File.AppendAllText(_logFile, logEntry + Environment.NewLine);
            }
            catch { }
        }

        public void LogError(string message, Exception ex)
        {
            Log($"ERROR: {message} - {ex.Message}");
        }

        public void LogInfo(string message)
        {
            Log($"INFO: {message}");
        }

        public void LogWarning(string message)
        {
            Log($"WARNING: {message}");
        }
    }
}
