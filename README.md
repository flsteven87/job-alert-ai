# Job Alert AI

Job Alert AI 是一個智能職缺通知系統，能夠自動爬取指定公司的職缺頁面，分析用戶履歷與職缺的匹配度，並在發現合適職缺時通過電子郵件通知用戶。

## 專案結構

```
job-alert-ai/
├── app/                    # 主應用程序目錄
│   ├── api/                # API 路由
│   │   └── api_v1/         # API v1 版本
│   │       ├── endpoints/  # API 端點
│   │       └── api.py      # API 路由集合
│   ├── core/               # 核心配置
│   ├── db/                 # 數據庫設置
│   ├── models/             # SQLAlchemy 數據模型
│   ├── schemas/            # Pydantic 數據驗證模型
│   ├── services/           # 業務邏輯服務
│   ├── utils/              # 工具函數
│   └── main.py             # 主應用入口
├── tests/                  # 測試目錄
├── .env                    # 環境變數
├── .env.example            # 環境變數範例
├── environment.yml         # Conda 環境配置
└── PLANNING.md             # 專案規劃文檔
```

## 環境設置

此專案使用 Conda 進行環境管理。

### 使用 Conda 創建環境

```bash
# 創建 Conda 環境
conda env create -f environment.yml

# 啟動環境
conda activate job-alert-ai
```

### 設置環境變數

複製 `.env.example` 為 `.env` 並填入適當的設置值：

```bash
cp .env.example .env
# 編輯 .env 文件設置適當的值
```

## 運行應用

### 開發模式

```bash
# 啟動 FastAPI 開發伺服器
uvicorn app.main:app --reload
```

伺服器將運行在 http://localhost:8000

### API 文檔

- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

## 測試

運行測試：

```bash
pytest
```

## 專案進度

請參考 `TASK.md` 檔案了解專案任務和進度。

## 規劃文檔

詳細的系統設計和規劃請參考 `PLANNING.md` 文檔。

## 核心功能

- 🔍 **智能爬蟲**：定期爬取指定公司的職缺頁面
- 📊 **履歷分析**：解析用戶履歷，提取關鍵技能和經驗
- 🎯 **職缺匹配**：智能比對履歷與職缺的匹配度
- 📧 **即時通知**：發現匹配職缺時，立即發送郵件通知
- 🔐 **Google 登入**：簡便安全的用戶認證機制

## 技術棧

### 後端
- [FastAPI](https://fastapi.tiangolo.com/) - 高性能 API 框架
- [Supabase](https://supabase.com/) - 開源 Firebase 替代品，處理數據和認證
- [Jina AI Reader](https://jina.ai/) - 智能網頁內容轉換 API，將網頁轉為 Markdown
- Python 3.12

### 前端
- [Streamlit](https://streamlit.io/) - 數據應用快速開發框架

### 部署
- [Docker](https://www.docker.com/) - 容器化部署
- [Conda](https://docs.conda.io/) - 環境與套件管理

## 快速開始

### 環境設置
```bash
# 克隆專案
git clone https://github.com/yourusername/job-alert-ai.git
cd job-alert-ai

# 使用 Conda 創建環境
conda env create -f environment.yml
conda activate job-alert-ai

# 配置環境變量
cp .env.example .env
# 編輯 .env 文件，填入必要的 API 金鑰和設定
```

### 環境變數設定
專案使用 `.env` 文件管理所有敏感設定和 API 金鑰。主要需要配置以下項目：

1. **API 金鑰**：
   - Jina AI API 金鑰 - 用於網頁內容轉換
   - OpenAI API 金鑰 - 用於職缺分析（如需使用）

2. **Supabase 設定**：
   - 項目 URL
   - 匿名金鑰和服務金鑰

3. **Google OAuth**：
   - 客戶端 ID 和密鑰（用於用戶認證）

完整的環境變數說明請參考 `.env.example` 文件。

### 運行專案
```bash
# 啟動後端 API
uvicorn app.main:app --reload

# 啟動前端應用
streamlit run frontend/app.py
```

## 開發指南

請參閱 [PLANNING.md](PLANNING.md) 了解詳細的系統設計和架構。
開發任務和進度追蹤請查看 [TASK.md](TASK.md)。

## 貢獻

歡迎提交 Pull Request 或開 Issue 反饋問題。

## 許可證

MIT
