# 1. 指定基础镜像：我们用官方轻量版的 Python 3.10
FROM python:3.10-slim

# 2. 设置容器内部的工作目录
WORKDIR /app

# 3. 把本地的项目代码复制到容器里的 /app 目录
COPY . .

# 4. 安装依赖
RUN pip install --no-cache-dir -r requirements.txt

ENV PYTHONPATH=/app

# 5. 设置环境变量：防止 Python 产生 pyc 文件并让日志实时输出
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# 6. 容器启动后默认执行的命令（运行测试）
CMD ["pytest", "autotest/tests/", "-v", "-s", "--alluredir=/app/allure-results"]