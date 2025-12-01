using System;
using System.Security.Cryptography;
using System.Text;

namespace DropshippingApp.Services
{
    public class AuthService
    {
        private readonly DatabaseService _db = new();
        private string _currentUser = null;

        public bool Register(string email, string password)
        {
            if (_db.UserExists(email)) return false;
            
            var hash = HashPassword(password);
            _db.SaveUser(email, hash);
            return true;
        }

        public bool Login(string email, string password)
        {
            if (!_db.UserExists(email)) return false;
            
            _currentUser = email;
            return true;
        }

        public void Logout()
        {
            _currentUser = null;
        }

        public string GetCurrentUser() => _currentUser;

        public bool IsLoggedIn() => _currentUser != null;

        private string HashPassword(string password)
        {
            using (var sha256 = SHA256.Create())
            {
                var hashedBytes = sha256.ComputeHash(Encoding.UTF8.GetBytes(password));
                return Convert.ToBase64String(hashedBytes);
            }
        }
    }
}
