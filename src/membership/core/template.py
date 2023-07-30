from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

from membership.core.config import settings

htemplate = Jinja2Templates(directory=settings.TEMPLATE_DIR)
stemplate = StaticFiles(directory=settings.STATIC_DIR)