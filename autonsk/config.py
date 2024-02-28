from flask_uploads import UploadSet, IMAGES
# конфигурация
DATABASE = '/tmp/autonsk.db'
SECRET_KEY = 'fdgfh78@#5?>gfhf89dx,v06k'
MAX_CONTENT_LENGTH = 1024 * 1024

photos = UploadSet('photos', IMAGES)