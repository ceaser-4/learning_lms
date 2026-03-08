import yaml
from pathlib import Path

def load_yaml_data(file_path):
    """
    读取 YAML 文件并返回列表数据
    """
    root_path = Path(__file__).resolve().parent.parent.parent
    full_path = root_path / "data" / file_path

    with open(full_path, encoding='utf-8') as f:
        return yaml.safe_load(f)