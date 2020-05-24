import os
from .report import BenchmarkReport
from .project import Project, PythonProject, JuliaProject

ROOT_PATH = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))
IMAGE_PATH = os.path.join(ROOT_PATH, 'images')

def image_path(name):
    if not os.path.isdir(IMAGE_PATH):
        os.makedirs(IMAGE_PATH, exist_ok=True)
    return os.path.join(IMAGE_PATH, name)
