using System;
using System.Collections.Generic;
using System.Linq;
using Microsoft.Data.Sqlite;

namespace DropshippingApp.Services
{
    public class DatabaseService
    {
        private const string ConnectionString = "Data Source=dropshipping.db";

        public DatabaseService()
        {
            InitializeDatabase();
        }

        private void InitializeDatabase()
        {
            using (var connection = new SqliteConnection(ConnectionString))
            {
                connection.Open();
                var command = connection.CreateCommand();
                command.CommandText = @"
                    CREATE TABLE IF NOT EXISTS Orders (
                        Id INTEGER PRIMARY KEY,
                        OrderId TEXT UNIQUE,
                        CustomerEmail TEXT,
                        Total REAL,
                        Status TEXT,
                        Tracking TEXT,
                        CreatedAt TEXT
                    );
                    CREATE TABLE IF NOT EXISTS Products (
                        Id INTEGER PRIMARY KEY,
                        Asin TEXT UNIQUE,
                        Title TEXT,
                        Price REAL,
                        Supplier TEXT,
                        SupplierPrice REAL,
                        SellingPrice REAL,
                        Profit REAL,
                        Margin REAL
                    );
                    CREATE TABLE IF NOT EXISTS Users (
                        Id INTEGER PRIMARY KEY,
                        Email TEXT UNIQUE,
                        PasswordHash TEXT,
                        CreatedAt TEXT
                    );
                ";
                command.ExecuteNonQuery();
            }
        }

        public void SaveOrder(string orderId, string email, decimal total, string status)
        {
            using (var connection = new SqliteConnection(ConnectionString))
            {
                connection.Open();
                var command = connection.CreateCommand();
                command.CommandText = "INSERT OR REPLACE INTO Orders (OrderId, CustomerEmail, Total, Status, CreatedAt) VALUES (@id, @email, @total, @status, @date)";
                command.Parameters.AddWithValue("@id", orderId);
                command.Parameters.AddWithValue("@email", email);
                command.Parameters.AddWithValue("@total", total);
                command.Parameters.AddWithValue("@status", status);
                command.Parameters.AddWithValue("@date", DateTime.Now.ToString("o"));
                command.ExecuteNonQuery();
            }
        }

        public List<dynamic> GetAllOrders()
        {
            var orders = new List<dynamic>();
            using (var connection = new SqliteConnection(ConnectionString))
            {
                connection.Open();
                var command = connection.CreateCommand();
                command.CommandText = "SELECT * FROM Orders";
                using (var reader = command.ExecuteReader())
                {
                    while (reader.Read())
                    {
                        orders.Add(new
                        {
                            OrderId = reader["OrderId"],
                            Email = reader["CustomerEmail"],
                            Total = reader["Total"],
                            Status = reader["Status"]
                        });
                    }
                }
            }
            return orders;
        }

        public void SaveUser(string email, string passwordHash)
        {
            using (var connection = new SqliteConnection(ConnectionString))
            {
                connection.Open();
                var command = connection.CreateCommand();
                command.CommandText = "INSERT OR REPLACE INTO Users (Email, PasswordHash, CreatedAt) VALUES (@email, @hash, @date)";
                command.Parameters.AddWithValue("@email", email);
                command.Parameters.AddWithValue("@hash", passwordHash);
                command.Parameters.AddWithValue("@date", DateTime.Now.ToString("o"));
                command.ExecuteNonQuery();
            }
        }

        public bool UserExists(string email)
        {
            using (var connection = new SqliteConnection(ConnectionString))
            {
                connection.Open();
                var command = connection.CreateCommand();
                command.CommandText = "SELECT COUNT(*) FROM Users WHERE Email = @email";
                command.Parameters.AddWithValue("@email", email);
                return (long)command.ExecuteScalar() > 0;
            }
        }
    }
}
