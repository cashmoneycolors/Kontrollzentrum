using System;
using System.Text.RegularExpressions;

namespace DropshippingApp.Services
{
    public class WebsiteConverterService
    {
        public string ConvertHTMLToXAML(string html)
        {
            var xaml = @"<Window xmlns='http://schemas.microsoft.com/winfx/2006/xaml/presentation'>";
            xaml += "\n    <!-- Converted from HTML -->";
            xaml += "\n    <Grid>";
            
            // Simple HTML to XAML conversion
            xaml += Regex.Replace(html, @"<h1>(.*?)</h1>", 
                m => $"\n        <TextBlock Text='{m.Groups[1].Value}' FontSize='24' FontWeight='Bold'/>");
            xaml += Regex.Replace(html, @"<p>(.*?)</p>", 
                m => $"\n        <TextBlock Text='{m.Groups[1].Value}' TextWrapping='Wrap'/>");
            xaml += Regex.Replace(html, @"<button>(.*?)</button>", 
                m => $"\n        <Button Content='{m.Groups[1].Value}' Height='40'/>");
            
            xaml += "\n    </Grid>";
            xaml += "\n</Window>";
            return xaml;
        }

        public string ConvertCSSToWPF(string css)
        {
            var wpf = "<!-- WPF Styles from CSS -->\n";
            wpf += "<Window.Resources>\n";
            wpf += "    <Style TargetType='TextBlock'>\n";
            wpf += "        <Setter Property='FontFamily' Value='Segoe UI'/>\n";
            wpf += "        <Setter Property='FontSize' Value='12'/>\n";
            wpf += "    </Style>\n";
            wpf += "</Window.Resources>";
            return wpf;
        }

        public string ConvertJavaScriptToCS(string js)
        {
            return $@"// Converted from JavaScript
public class ConvertedScript
{{
    public void Execute()
    {{
        // {js}
    }}
}}";
        }
    }
}
