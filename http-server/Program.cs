using System;
using System.Collections.Generic;
using System.IO;
using System.Net;
using System.Net.Sockets;
using System.Text;

namespace http_server
{
    class Program
    {
        static void Main(string[] args)
        {
            new HttpServer("127.0.0.1", 5555, 0).Run();
        }
    }

    class HttpServer
    {
        private string host;
        private int port;
        private int backlog;
        private readonly string PROTOCOL_VERSION = "HTTP1.1";
        public HttpServer(string host, int port, int backlog)
        {
            this.host = host;
            this.port = port;
            this.backlog = backlog;
        }

        public void Run()
        {
            IPAddress ipAddress = IPAddress.Parse(host);
            IPEndPoint endPoint = new IPEndPoint(ipAddress, port);
            Socket listener = new Socket(ipAddress.AddressFamily, SocketType.Stream, ProtocolType.Tcp);
            listener.Bind(endPoint);
            listener.Listen(this.backlog);

            Console.WriteLine("Accepting connections at " + endPoint.ToString());
            while (true)
            {
                Socket handler = listener.Accept();
                Connection conn = new Connection(handler);
                Request request = Request.ReadFrom(conn);
                byte[] response = this.Process(request);
                handler.Send(response);
                handler.Shutdown(SocketShutdown.Both);
                handler.Close();
            }
        }

        private byte[] Process(Request req)
        {
            string response = string.Empty;
            string path = Directory.GetCurrentDirectory() + req.path;
            if (File.Exists(path))
            {
                string content = File.ReadAllText(path);
                response = string.Format("{0} 200 Ok\r\n", this.PROTOCOL_VERSION);
                response += "Content-Type: text/html; charset=us-ascii\r\n";
                response += "Content-Length: " + content.Length + "\r\n\r\n";
                response += content;
            }
            else
            {
                response = string.Format("{0} 404 NotFound\r\n\r\n", this.PROTOCOL_VERSION);
            }

            return Encoding.ASCII.GetBytes(response);
        }
    }

    class Connection
    {
        private Socket socket;
        private byte[] buffer;
        private int bufferSize = 0;
        public Connection(Socket s)
        {
            this.socket = s;
            this.buffer = new byte[8];
        }

        public string ReadLine()
        {
            string data = string.Empty;
            if (this.bufferSize > 0)
            {
                data = Encoding.ASCII.GetString(this.buffer, 0, this.bufferSize);
            }

            while (!data.Contains("\r\n"))
            {
                int bytesRec = this.socket.Receive(this.buffer);
                data += Encoding.ASCII.GetString(this.buffer, 0, bytesRec);
            }

            string[] pieces = data.Split("\r\n", 2);
            byte[] bytesLeft = Encoding.ASCII.GetBytes(pieces[1]);
            this.bufferSize = bytesLeft.Length;
            for (int i = 0; i < this.bufferSize; i++)
            {
                buffer[i] = bytesLeft[i];
            }
            return pieces[0];
        }
    }

    class Request
    {
        public string method;
        public string path;
        public Dictionary<string, string> headers;

        public static Request ReadFrom(Connection conn)
        {
            string[] requestLinePieces = conn.ReadLine().Split(' ');
            var _headers = new Dictionary<string, string>();

            string line = null;
            while ((line = conn.ReadLine()) != string.Empty)
            {
                string[] headerPieces = line.Split(": ", 2);
                _headers.Add(headerPieces[0], headerPieces[1]);
            }

            return new Request
            {
                method = requestLinePieces[0],
                path = requestLinePieces[1],
                headers = _headers,
            };
        }
    }
}
