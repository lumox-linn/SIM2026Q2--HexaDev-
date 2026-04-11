import os
from app import create_app

app = create_app()

if __name__ == '__main__':
    # Use Railway's PORT env variable, fallback to 5000 for local
    port = int(os.getenv('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=False)