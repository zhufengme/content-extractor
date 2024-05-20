# 内容提取器 (Content Extractor)

该项目提供了一个用于从网页或HTML内容中提取正文和图像的RESTful API。该服务使用Flask构建，并可以使用Docker进行容器化。

## 功能

- 从给定的URL或原始HTML中提取主要内容文本。
- 从主要内容区域中提取第一张图像。
- 支持多种语言，包括中文和日文。
- 使用Docker进行容器化，方便部署。
- 提供健康检查端点以便监控。

## 快速开始

### 前提条件

- Python 3.8
- Docker

### 安装

1. 克隆仓库：

    ```bash
    git clone https://github.com/zhufengme/content-extractor.git
    cd content-extractor
    ```

2. 安装依赖项（用于本地开发）：

    ```bash
    pip install -r requirements.txt
    ```

### 配置

该项目无需额外的配置。

### 本地运行服务

1. 运行Flask应用：

    ```bash
    python app.py
    ```

### 使用Docker构建和运行

1. 构建Docker镜像：

    ```bash
    docker build -t content-extractor .
    ```

2. 运行Docker容器：

    ```bash
    docker run -d -p 5001:5001 --name content-extractor content-extractor
    ```

### 从DockerHub运行

你可以从DockerHub拉取镜像并直接运行。

1. 拉取Docker镜像：

    ```bash
    docker pull andiezhu/content-extractor
    ```

2. 运行Docker容器：

    ```bash
    docker run -d -p 5001:5001 --name content-extractor andiezhu/content-extractor
    ```

### API使用说明

#### 端点

- `POST /`

#### 请求体

- `url`（字符串，可选）：要提取内容的网页URL。
- `html`（字符串，可选）：要提取内容的原始HTML。
- `language`（字符串，可选）：指定内容的语言。如果未指定，将自动检测。

#### 示例请求

```bash
curl -X POST http://localhost:5001/ \
     -H "Content-Type: application/json" \
     -d '{
           "url": "http://example.com"
         }'
```

或者

```bash
curl -X POST http://localhost:5001/ \
     -H "Content-Type: application/json" \
     -d '{
           "html": "<html><body><h1>示例</h1><p>这是一个示例。</p><img src=\"//example.com/image.jpg\" /></body></html>"
         }'
```

### 健康检查

该服务提供了一个健康检查端点：

- `GET /health`

#### 示例请求

```bash
curl http://localhost:5001/health
```

### 日志记录

默认情况下，日志记录到控制台。

#### 查看日志

要查看日志，可以使用`docker logs`命令：

```bash
docker logs -f content-extractor
```

## 许可证

此项目使用MIT许可证。详情请参阅[LICENSE](LICENSE)文件。

## 鸣谢

- [Flask](https://flask.palletsprojects.com/)
- [Requests](https://docs.python-requests.org/)
- [BeautifulSoup](https://www.crummy.com/software/BeautifulSoup/)
- [Goose3](https://github.com/goose3/goose3)
- [jieba](https://github.com/fxsjy/jieba)
- [janome](https://github.com/mocobeta/janome)
- [langdetect](https://github.com/Mimino666/langdetect)
- [langid](https://github.com/saffsd/langid.py)
