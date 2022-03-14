import os


AUTH_SECRET_KEY = os.getenv('AUTH_SECRET_KEY', '')
AUTH_HOST = os.getenv('AUTH_HOST', '127.0.0.1')
AUTH_PORT = int(os.getenv('AUTH_PORT', 5000))
AUTH_TOKEN_VALIDATION_URL = 'http://{host}:{port}/auth/v1/auth_token/validation'.format(host=AUTH_HOST,
                                                                                        port=AUTH_PORT)
AUTH_PERMISSIONS_AND_TOKEN_VALIDATION_URL = \
    'http://{host}:{port}/auth/v1/users/{{user_id}}/combined_permissions/validation'.format(host=AUTH_HOST,
                                                                                            port=AUTH_PORT)

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
