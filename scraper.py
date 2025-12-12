import json
from http.server import HTTPServer, BaseHTTPRequestHandler
from urllib.parse import urlparse, parse_qs

# Dados de exemplo - substitua isso pelo scraping real dos sites
PRODUTOS_EXEMPLO = [
    {
        "name": "iPhone 15 Pro Max",
        "model": "256GB - Titânio Natural",
        "image": "https://placeholder.svg?height=120&width=120&query=iphone+15+pro",
        "stores": [
            {"name": "Madrid Center", "price": 8499.00, "url": "https://madridcenterimportados.com/home"},
            {"name": "Atacado Connect", "price": 8299.00, "url": "https://atacadoconnect.com/"},
            {"name": "Nissei", "price": 8599.00, "url": "https://nissei.com/br/"},
            {"name": "Cell Shop", "price": 8399.00, "url": "https://cellshop.com/"},
            {"name": "Tche Loco", "price": 8199.00, "url": "https://www.tcheloco.com.py/br/"}
        ]
    },
    {
        "name": "Samsung Galaxy S24 Ultra",
        "model": "512GB - Titânio Preto",
        "image": "https://placeholder.svg?height=120&width=120&query=samsung+s24+ultra",
        "stores": [
            {"name": "Madrid Center", "price": 7299.00, "url": "https://madridcenterimportados.com/home"},
            {"name": "Atacado Connect", "price": 7199.00, "url": "https://atacadoconnect.com/"},
            {"name": "Nissei", "price": 7399.00, "url": "https://nissei.com/br/"},
            {"name": "Cell Shop", "price": 7249.00, "url": "https://cellshop.com/"},
            {"name": "Tche Loco", "price": 6999.00, "url": "https://www.tcheloco.com.py/br/"}
        ]
    },
    {
        "name": "Xiaomi 13T Pro",
        "model": "256GB - Preto",
        "image": "https://placeholder.svg?height=120&width=120&query=xiaomi+13t+pro",
        "stores": [
            {"name": "Madrid Center", "price": 3499.00, "url": "https://madridcenterimportados.com/home"},
            {"name": "Atacado Connect", "price": 3399.00, "url": "https://atacadoconnect.com/"},
            {"name": "Nissei", "price": 3599.00, "url": "https://nissei.com/br/"},
            {"name": "Cell Shop", "price": 3449.00, "url": "https://cellshop.com/"},
            {"name": "Tche Loco", "price": 3299.00, "url": "https://www.tcheloco.com.py/br/"}
        ]
    }
]

class RequestHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        parsed_path = urlparse(self.path)
        
        if parsed_path.path == '/api/search':
            query_params = parse_qs(parsed_path.query)
            search_query = query_params.get('q', [''])[0].lower()
            
            # Filtrar produtos baseado na busca
            results = [
                produto for produto in PRODUTOS_EXEMPLO
                if search_query in produto['name'].lower() or search_query in produto['model'].lower()
            ]
            
            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.send_header('Access-Control-Allow-Origin', '*')
            self.end_headers()
            self.wfile.write(json.dumps(results).encode())
        
        elif parsed_path.path == '/' or parsed_path.path == '/index.html':
            self.send_response(200)
            self.send_header('Content-type', 'text/html')
            self.end_headers()
            with open('index.html', 'rb') as f:
                self.wfile.write(f.read())
        
        elif parsed_path.path == '/style.css':
            self.send_response(200)
            self.send_header('Content-type', 'text/css')
            self.end_headers()
            with open('style.css', 'rb') as f:
                self.wfile.write(f.read())
        
        else:
            self.send_response(404)
            self.end_headers()

if __name__ == '__main__':
    port = 8000
    server = HTTPServer(('localhost', port), RequestHandler)
    print(f'Servidor rodando em http://localhost:{port}')
    print('Pressione Ctrl+C para parar')
    server.serve_forever()
