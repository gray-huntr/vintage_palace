class Config(object):
    Debug = False

    SECRET_KEY = "CRLKKX&u`&s*jCF"
    # Details of the database
    DB_HOST = "localhost"
    DB_USERNAME = "root"
    DB_PASSWORD = ""
    DB_NAME = "vintage_palace"

    # Details of file uploads
    ALLOWED_EXTENSIONS = {'pdf', 'png', 'jpg', 'jpeg', 'gif','webp'}

    UPLOAD_FOLDER = 'C:/Users/DELL/PycharmProjects/vintage_palace/app/static/images'
