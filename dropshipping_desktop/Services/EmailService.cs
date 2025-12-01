using System;
using System.Net;
using System.Net.Mail;
using System.Threading.Tasks;

namespace DropshippingApp.Services
{
    public class EmailService
    {
        private readonly string _gmailEmail = Environment.GetEnvironmentVariable("GMAIL_EMAIL") ?? "your_email@gmail.com";
        private readonly string _gmailPassword = Environment.GetEnvironmentVariable("GMAIL_PASSWORD") ?? "your_app_password";

        public async Task SendOrderConfirmation(string customerEmail, string orderId, decimal amount)
        {
            var subject = $"Order Confirmation - {orderId}";
            var body = $@"
Dear Customer,

Your order {orderId} has been confirmed!
Amount: ${amount:F2}

We will ship your order soon.
Tracking information will be sent to this email.

Best regards,
Dropshipping Team";

            await SendEmailAsync(customerEmail, subject, body);
        }

        public async Task SendShippingNotification(string customerEmail, string orderId, string tracking)
        {
            var subject = $"Your Order {orderId} Has Shipped!";
            var body = $@"
Dear Customer,

Your order {orderId} has been shipped!
Tracking Number: {tracking}

Track your package: https://tracking.example.com/{tracking}

Best regards,
Dropshipping Team";

            await SendEmailAsync(customerEmail, subject, body);
        }

        public async Task SendDailyReport(string adminEmail, int ordersCount, decimal revenue)
        {
            var subject = $"Daily Report - {DateTime.Now:yyyy-MM-dd}";
            var body = $@"
Daily Dropshipping Report

Orders: {ordersCount}
Revenue: ${revenue:F2}

Keep up the great work!";

            await SendEmailAsync(adminEmail, subject, body);
        }

        private async Task SendEmailAsync(string toEmail, string subject, string body)
        {
            try
            {
                using (var client = new SmtpClient("smtp.gmail.com", 587))
                {
                    client.EnableSsl = true;
                    client.Credentials = new NetworkCredential(_gmailEmail, _gmailPassword);

                    var mailMessage = new MailMessage(_gmailEmail, toEmail)
                    {
                        Subject = subject,
                        Body = body,
                        IsBodyHtml = false
                    };

                    await client.SendMailAsync(mailMessage);
                }
            }
            catch (Exception ex)
            {
                Console.WriteLine($"Email Error: {ex.Message}");
            }
        }
    }
}
