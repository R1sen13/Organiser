import pathlib
import hashlib
import logging
import shutil


logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

Rules = {
    "Images": [".jpg", ".jpeg", ".png", ".gif", ".bmp", ".svg", ".webp"],
    "Documents": [".pdf", ".docx", ".doc", ".txt", ".xlsx", ".xls", ".pptx", ".ppt", ".odt", ".ods"],
    "Audio": [".mp3", ".wav", ".flac", ".aac", ".ogg"],
    "Videos": [".mp4", ".avi", ".mkv", ".mov", ".wmv", ".flv"]
}

def calculate_hash(file_path, chunk_size=8192):
    hash_md5 = hashlib.md5()
    with open(file_path, "rb") as f:
        for chunk in iter(lambda: f.read(chunk_size), b""):
            hash_md5.update(chunk)
    return hash_md5.hexdigest()

def get_category(file_path):
    ext = file_path.suffix.lower()
    for category, extensions in Rules.items():
        if ext in extensions:
            return category
    return "Other"

def organize_folder(folder_path):
    current_folder = pathlib.Path(folder_path)
    if current_folder.exists():
        logger.info("Папка существует\n")

    for item in current_folder.iterdir():
        if item.is_file():
            category = get_category(item)
            dest_folder = current_folder / category
            dest_folder.mkdir(exist_ok=True)
            logger.info(f"Папка {dest_folder} создана/существует")
            dest_path = dest_folder / item.name
            if dest_path.exists():
                logger.warning(f"Файл {item.name} уже есть в {dest_folder}!")
                continue
            shutil.move(str(item), str(dest_path))
            logger.info(f"Передвинули {item.name} в {category}")

if __name__ == "__main__":
    print("Type in path of the folder that you want to organise (Example: C:/Users/Ivan/Downloads)>>")
    s = input()
    organize_folder(s)