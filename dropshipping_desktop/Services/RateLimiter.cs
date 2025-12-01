using System;
using System.Collections.Generic;

namespace DropshippingApp.Services
{
    public class RateLimiter
    {
        private Dictionary<string, List<DateTime>> _requests = new();
        private int _maxRequests = 100;
        private int _windowSeconds = 60;

        public bool IsAllowed(string key)
        {
            if (!_requests.ContainsKey(key))
                _requests[key] = new List<DateTime>();

            var now = DateTime.Now;
            var window = now.AddSeconds(-_windowSeconds);
            _requests[key].RemoveAll(t => t < window);

            if (_requests[key].Count >= _maxRequests)
                return false;

            _requests[key].Add(now);
            return true;
        }

        public int GetRemainingRequests(string key)
        {
            if (!_requests.ContainsKey(key)) return _maxRequests;
            var now = DateTime.Now;
            var window = now.AddSeconds(-_windowSeconds);
            var count = _requests[key].FindAll(t => t >= window).Count;
            return Math.Max(0, _maxRequests - count);
        }
    }
}
