import os
import yaml

def get_h5ad_paths_from_config(tissue=None, config_path="data_config.yaml"):
    """
    根据组织名称从 data_config.yaml 中获取 h5ad 文件的完整路径列表
    
    参数:
        tissue (str or None): 组织名称，如 'Lung', 'Brain'。若为 None，则使用 default_tissue
        config_path (str): 配置文件路径
    
    返回:
        List[str]: 完整的 h5ad 文件路径列表
    """
    with open(config_path, 'r') as f:
        config = yaml.safe_load(f)
    
    data_root = config['global']['data_root']
    default_tissue = config['global'].get('default_tissue', 'lung')
    
    # 如果没指定 tissue，用默认
    if tissue is None:
        tissue = default_tissue
    
    # 规范化 tissue 名称：首字母大写（因为 YAML 中是 Lung, Brain 等）
    tissue = tissue.capitalize()
    
    if tissue not in config['datasets']:
        available = list(config['datasets'].keys())
        raise ValueError(f"组织 '{tissue}' 未在配置文件中找到。可用组织: {available}")
    
    file_names = config['datasets'][tissue]['h5ad_files']
    full_paths = [os.path.join(data_root,tissue, fname) for fname in file_names]
    
    # 可选：检查文件是否存在
    missing = [p for p in full_paths if not os.path.exists(p)]
    if missing:
        print(f"警告: 以下文件不存在:\n" + "\n".join(missing))
    
    return full_paths