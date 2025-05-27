from typing import List, Dict, Any


def find_files(path: str = '.', file_pattern: str = '*',
               recursive: bool = False) -> List[Dict[str, Any]]:
    """
    在指定路径下查找匹配模式的文件，并返回文件信息列表。

    Args:
        path (str, optional): 要搜索的目录路径。默认为当前目录（'.'）。
            支持以下格式：
            - 相对路径（如 './docs'）
            - 绝对路径（如 '/home/user/files'）
            - 用户目录（如 '~/Documents'）
        file_pattern (str, optional): 文件名匹配模式（支持通配符）。默认为 '*'（所有文件）。
            示例：
            - '*.txt' 匹配所有文本文件
            - 'data_??.csv' 匹配如 data_01.csv 的文件
        recursive (bool, optional): 是否递归搜索子目录。默认为 False。

    Returns:
        List[Dict[str, Any]]: 文件信息字典列表，每个字典包含：
            - 'name': 文件名（str）


    Raises:
        FileNotFoundError: 当指定路径不存在时
        Exception: 其他错误（如权限不足）

    Examples:
        # 示例1：查找当前目录下所有.py文件
         py_files = find_files(file_pattern='*.py')
         for file in py_files:
        ...     print(file['name'], file['path'])

         # 示例2：递归查找用户Documents目录下所有.txt文件
         txt_files = find_files(
        ...     path='~/Documents',
        ...     file_pattern='*.txt',
        ...     recursive=True
        ... )
         for file in txt_files:
        ...     print(f"{file['name']} ({file['size']} bytes)")

         # 示例3：查找特定目录下无扩展名的文件
        no_ext_files = find_files(
        ...     path='/var/log',
        ...     file_pattern='*.',
        ...     recursive=False
        ... )
    """
    results = []

    try:
        search_path = Path(path).expanduser().resolve()

        if not search_path.exists():
            raise FileNotFoundError(f"路径不存在: {path}")

        if recursive:
            pattern = f"**/{file_pattern}"
            files = search_path.glob(pattern)
        else:
            files = search_path.glob(file_pattern)

        for file_path in files:
            if file_path.is_file():
                file_info = {
                    #'path': str(file_path),
                    'name': file_path.name,
                    #'size': file_path.stat().st_size,
                    #'modified': datetime.fromtimestamp(file_path.stat().st_mtime).isoformat(),
                    #'type': file_path.suffix.lower() if file_path.suffix else 'no_extension'
                }
                results.append(file_info)

        return sorted(results, key=lambda x: x['name'])

    except Exception as e:
        raise Exception(f"文件查找失败: {str(e)}")


from pathlib import Path
from typing import Dict, Any


def count_files(path: str = '.', file_pattern: str = '*',
                recursive: bool = False) -> Dict[str, Any]:
    """
    统计指定路径下匹配模式的文件数量。

    Args:
        path (str, optional): 要统计的目录路径。默认为当前目录（'.'）。
            支持以下格式：
            - 相对路径（如 './docs'）
            - 绝对路径（如 '/home/user/files'）
            - 用户目录（如 '~/Documents'）
        file_pattern (str, optional): 文件名匹配模式（支持通配符）。默认为 '*'（所有文件）。
            示例：
            - '*.txt' 统计所有文本文件
            - 'data_??.csv' 统计如 data_01.csv 的文件
        recursive (bool, optional): 是否递归统计子目录。默认为 False。

    Returns:
        Dict[str, Any]: 返回统计结果字典，包含：
            - 'total': 文件总数（int）
            - 'path': 统计的绝对路径（str）
            - 'pattern': 使用的匹配模式（str）
            - 'sample_files': 示例文件列表（前5个文件，用于验证）

    Raises:
        FileNotFoundError: 当指定路径不存在时
        Exception: 其他错误（如权限不足）

    Examples:
         # 示例1：统计当前目录下所有.py文件数量
         py_stats = count_files(file_pattern='*.py')
         print(f"找到 {py_stats['total']} 个Python文件")

         # 示例2：递归统计用户Documents目录下所有.txt文件
         txt_stats = count_files(
        ...     path='~/Documents',
        ...     file_pattern='*.txt',
        ...     recursive=True
        ... )
         print(f"在 {txt_stats['path']} 中找到 {txt_stats['total']} 个文本文件")

         # 示例3：统计特定目录下无扩展名的文件
        no_ext_stats = count_files(
        ...     path='/var/log',
        ...     file_pattern='*.',
        ...     recursive=False
        ... )
    """
    try:
        search_path = Path(path).expanduser().resolve()
        if not search_path.exists():
            raise FileNotFoundError(f"路径不存在: {path}")

        count = 0
        sample_files = []

        if recursive:
            pattern = f"**/{file_pattern}"
            files = search_path.glob(pattern)
        else:
            files = search_path.glob(file_pattern)

        for file_path in files:
            if file_path.is_file():
                count += 1
                if len(sample_files) < 5:  # 保留前5个文件作为示例
                    sample_files.append(str(file_path))

        return {
            'total': count,
            'path': str(search_path),
            'pattern': file_pattern,
            'sample_files': sample_files
        }

    except Exception as e:
        raise Exception(f"文件统计失败: {str(e)}")


if __name__=="__main__":
    #files = find_files("~/Documents", file_pattern="*")
    files = count_files("~/Documents", file_pattern="*")
    print(files)