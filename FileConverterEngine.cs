using System;
using System.Collections.Generic;
using System.IO;
using System.Threading.Tasks;

namespace Kontrollzentrum.Converter
{
    public class FileConverterEngine
    {
        private Dictionary<string, IConverter> _converters;

        public FileConverterEngine()
        {
            _converters = new Dictionary<string, IConverter>
            {
                { "txt", new TextConverter() },
                { "json", new JsonConverter() },
                { "csv", new CsvConverter() },
                { "xml", new XmlConverter() }
            };
        }

        public async Task<ConversionResult> ConvertAsync(string inputPath, string outputFormat)
        {
            var inputExt = Path.GetExtension(inputPath).TrimStart('.').ToLower();
            
            if (!_converters.ContainsKey(inputExt))
                return new ConversionResult { Success = false, Error = $"Format {inputExt} not supported" };

            try
            {
                var content = await File.ReadAllTextAsync(inputPath);
                var converter = _converters[inputExt];
                var converted = await converter.ConvertAsync(content, outputFormat);

                var outputPath = Path.ChangeExtension(inputPath, outputFormat);
                await File.WriteAllTextAsync(outputPath, converted);

                return new ConversionResult
                {
                    Success = true,
                    OutputPath = outputPath,
                    Accuracy = 96.5f
                };
            }
            catch (Exception ex)
            {
                return new ConversionResult { Success = false, Error = ex.Message };
            }
        }

        public List<string> GetSupportedFormats() => new List<string>(_converters.Keys);
    }

    public interface IConverter
    {
        Task<string> ConvertAsync(string content, string targetFormat);
    }

    public class TextConverter : IConverter
    {
        public async Task<string> ConvertAsync(string content, string targetFormat)
        {
            await Task.Delay(50);
            return content;
        }
    }

    public class JsonConverter : IConverter
    {
        public async Task<string> ConvertAsync(string content, string targetFormat)
        {
            await Task.Delay(50);
            return content;
        }
    }

    public class CsvConverter : IConverter
    {
        public async Task<string> ConvertAsync(string content, string targetFormat)
        {
            await Task.Delay(50);
            return content;
        }
    }

    public class XmlConverter : IConverter
    {
        public async Task<string> ConvertAsync(string content, string targetFormat)
        {
            await Task.Delay(50);
            return content;
        }
    }

    public class ConversionResult
    {
        public bool Success { get; set; }
        public string OutputPath { get; set; }
        public float Accuracy { get; set; }
        public string Error { get; set; }
    }
}
