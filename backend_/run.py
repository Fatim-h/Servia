from app import create_app

app = create_app()

if __name__ == '__main__':
    print("Starting Servia Backend Server...")
    print("Server URL: http://localhost:5000")
    print("")
    print("AVAILABLE ENDPOINTS:")
    print("   GET  /                    - Server status")
    print("   GET  /api/test            - Test endpoint") 
    print("   GET  /api/health          - Health check")
    print("   GET  /api/ngos            - Get all NGOs")
    print("   GET  /api/categories      - Get categories")
    print("   POST /api/register        - User registration")
    print("   POST /api/login           - User login")
    print("   POST /admin/login         - Admin login")
    print("")
    app.run(debug=True, port=5000)