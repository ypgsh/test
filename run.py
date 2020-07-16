
import sys

if __name__ == '__main__':
    from app.main import create_app
    app = create_app('develop')
    app.run(host='0.0.0.0', port=5000)
    