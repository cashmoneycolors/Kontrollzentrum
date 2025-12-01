using System;
using System.Collections.Generic;
using System.Linq;

namespace DropshippingApp.Services
{
    public class CacheService
    {
        private Dictionary<string, CacheEntry> _cache = new();
        private const int MaxCacheSize = 1000;
        private const int DefaultTTL = 300; // 5 minutes

        public void Set<T>(string key, T value, int ttl = DefaultTTL)
        {
            if (_cache.Count >= MaxCacheSize) EvictOldest();
            _cache[key] = new CacheEntry { Value = value, ExpiresAt = DateTime.Now.AddSeconds(ttl) };
        }

        public T Get<T>(string key)
        {
            if (!_cache.ContainsKey(key)) return default;
            var entry = _cache[key];
            if (DateTime.Now > entry.ExpiresAt) { _cache.Remove(key); return default; }
            return (T)entry.Value;
        }

        public T GetOrSet<T>(string key, Func<T> factory, int ttl = DefaultTTL)
        {
            var cached = Get<T>(key);
            if (cached != null) return cached;
            var value = factory();
            Set(key, value, ttl);
            return value;
        }

        private void EvictOldest()
        {
            var oldest = _cache.OrderBy(x => x.Value.ExpiresAt).First();
            _cache.Remove(oldest.Key);
        }

        private class CacheEntry { public object Value { get; set; } public DateTime ExpiresAt { get; set; } }
    }
}
