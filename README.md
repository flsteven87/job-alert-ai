# Job Alert AI

Job Alert AI 是一個智能職缺配對與通知系統，幫助用戶自動追蹤指定公司的職缺發布，並根據用戶履歷智能匹配合適的職位。

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

## 專案結構
```
job-alert-ai/
├── app/                    # 後端 API
│   ├── api/                # API 路由
│   ├── core/               # 核心設置
│   ├── crud/               # 數據庫操作
│   ├── db/                 # 數據庫模型
│   ├── schemas/            # Pydantic 模型
│   ├── services/           # 業務邏輯
│   │   ├── crawler/        # 爬蟲服務
│   │   ├── matcher/        # 匹配算法
│   │   └── notifier/       # 通知服務
│   └── main.py             # 應用入口
├── frontend/               # Streamlit 前端
├── tests/                  # 測試目錄
├── .env.example            # 環境變量示例
├── docker-compose.yml      # Docker 配置
├── Dockerfile              # Docker 構建文件
├── environment.yml         # Conda 環境配置
├── PLANNING.md             # 專案規劃文檔
├── TASK.md                 # 任務清單
└── README.md               # 專案說明
```

## 開發指南

請參閱 [PLANNING.md](PLANNING.md) 了解詳細的系統設計和架構。
開發任務和進度追蹤請查看 [TASK.md](TASK.md)。

## 貢獻

歡迎提交 Pull Request 或開 Issue 反饋問題。

## 許可證

MIT
