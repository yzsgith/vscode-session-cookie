import os
import shutil
from typing import List

project_structure = [
    # app/ 目录结构
    "app/__init__.py",
    "app/main.py",

    # app/api/ 目录结构
    "app/api/__init__.py",
    "app/api/dependencies.py",

    # app/api/endpoints/ 目录结构
    "app/api/endpoints/__init__.py",
    "app/api/endpoints/inference.py",
    "app/api/endpoints/models.py",
    "app/api/endpoints/auth.py",
    "app/api/endpoints/health.py",

    # app/core/ 目录结构
    "app/core/__init__.py",
    "app/core/config.py",
    "app/core/security.py",
    "app/core/exceptions.py",
    "app/core/middleware.py",

    # app/services/ 目录结构
    "app/services/__init__.py",
    "app/services/inference.py",
    "app/services/model_manager.py",
    "app/services/cache.py",
    "app/services/auth.py",
    "app/services/queue.py",

    # app/models/ 目录结构
    "app/models/__init__.py",
    "app/models/schemas.py",
    "app/models/database.py",
    "app/models/user.py",

    # app/utils/ 目录结构
    "app/utils/__init__.py",
    "app/utils/file_utils.py",
    "app/utils/monitoring.py",
    "app/utils/helpers.py",

    # workers/ 目录结构
    "workers/__init__.py",
    "workers/inference_worker.py",
    "workers/model_loader.py",
    "workers/task_processor.py",

    # frontend/ 目录结构
    "frontend/package.json",

    # frontend/public/ 目录（空目录）
    "frontend/public/",

    # frontend/src/ 目录结构
    "frontend/src/components/",
    "frontend/src/pages/",
    "frontend/src/services/",

    # tests/ 目录结构
    "tests/__init__.py",
    "tests/test_api.py",
    "tests/test_services.py",
    "tests/test_models.py",

    # docker/ 目录结构
    "docker/Dockerfile",
    "docker/docker-compose.yml",

    # docker/nginx/ 目录结构
    "docker/nginx/nginx.conf",

    # docs/ 目录结构
    "docs/api.md",
    "docs/deployment.md",
    "docs/development.md",

    # scripts/ 目录结构
    "scripts/setup.sh",
    "scripts/deploy.sh",
    "scripts/monitor.py",

    # 根目录文件
    "requirements.txt",
    "README.md",
    ".env.example",
    ".gitignore",
    "pyproject.toml",
    "setup.py"
]

def creatFilesOrDirectorys(pathNames: List[str]) -> None:
    """
    根据提供的路径列表创建文件或目录

    参数:
        pathNames: 路径字符串列表，如果路径以分隔符结尾则创建目录，否则创建文件

    注意:
        - 以函数所在位置为起始目录
        - 如果路径已存在，会先删除再重建
        - 支持创建多级嵌套目录
    """
    # 获取函数所在文件的目录作为基准路径
    base_dir = os.path.dirname(os.path.abspath(__file__))

    for path_name in pathNames:
        # 构建完整路径
        full_path = os.path.join(base_dir, path_name)

        # 检查路径是否已存在
        if os.path.exists(full_path):
            try:
                if os.path.isfile(full_path):
                    os.remove(full_path)  # 删除文件
                    print(f"已删除文件: {full_path}")
                else:
                    shutil.rmtree(full_path)  # 删除目录及其内容
                    print(f"已删除目录: {full_path}")
            except Exception as e:
                print(f"删除 {full_path} 时出错: {e}")
                continue  # 跳过此项，继续处理下一个

        # 判断是创建文件还是目录
        # 如果路径以路径分隔符结尾，则创建目录
        if path_name.endswith(os.sep) or path_name.endswith('/') or path_name.endswith('\\'):
            try:
                os.makedirs(full_path, exist_ok=True)
                print(f"已创建目录: {full_path}")
            except Exception as e:
                print(f"创建目录 {full_path} 时出错: {e}")
        else:
            # 创建文件，确保父目录存在
            parent_dir = os.path.dirname(full_path)
            if parent_dir and not os.path.exists(parent_dir):
                try:
                    os.makedirs(parent_dir, exist_ok=True)
                except Exception as e:
                    print(f"创建父目录 {parent_dir} 时出错: {e}")
                    continue

            # 创建文件
            try:
                with open(full_path, 'w') as f:
                    pass  # 创建空文件
                print(f"已创建文件: {full_path}")
            except Exception as e:
                print(f"创建文件 {full_path} 时出错: {e}")


# 示例使用
if __name__ == "__main__":
    test=[
        "app.js",
        "launch.json",
        "test/session.test.js",
        "package.json",
        "memory-store.js"
    ]
    # 测试用例
    test_paths = [
        "test_dir/",  # 创建目录
        "test_file.txt",  # 创建文件
        "nested/dir/structure/",  # 创建嵌套目录
        "nested/file/in/deep/path.txt",  # 在深层路径中创建文件
    ]

    print("开始创建文件和目录...")
    # creatFilesOrDirectorys(project_structure)
    creatFilesOrDirectorys(test)
