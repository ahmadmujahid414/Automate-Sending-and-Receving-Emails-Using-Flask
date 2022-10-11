class Config():
    SECRET_KEY = '\xd1\x81\x9a0\x99\xb6\x91?$\x11U\x86RG\xc6\x98\x1a\x10\x01\x9f2\xb2\xee\xf0Gba\xa1\xdaD\xf3O'
    MAIL_SERVER = 'smtp.gmail.com'
    MAIL_PORT = 465
    MAIL_USE_TLS = False
    MAIL_USE_SSL = True
    MAIL_USERNAME = 'techdiv07@gmail.com'
    MAIL_PASSWORD = '$mak123456'
    SQLALCHEMY_DATABASE_URI = "sqlite:///database.db"
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    
    def mail_username():
        return MAIL_USERNAME
        
    def mail_password():
        return MAIL_PASSWORD

