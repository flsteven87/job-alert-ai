# Job Alert AI 專案規劃

## 專案概述
Job Alert AI 是一個智能職缺通知系統，能夠自動爬取指定公司的職缺頁面，分析用戶履歷與職缺的匹配度，並在發現合適職缺時通過電子郵件通知用戶。

## 技術架構

### 後端 (Backend)
- **框架**: FastAPI
- **資料庫**: Supabase (PostgreSQL)
- **身份驗證**: Google OAuth
- **爬蟲方案**: Jina AI Reader API + LLM
- **履歷分析**: 自定義匹配算法
- **Python 版本**: 3.12

### 前端 (Frontend)
- **框架**: Streamlit
- **認證整合**: Streamlit-Auth-Component

### 部署 & 運維
- **容器化**: Docker + Docker Compose
- **環境管理**: Conda
- **雲端托管**: AWS / DigitalOcean

## 系統架構

```
┌─────────────┐      ┌─────────────┐      ┌─────────────┐
│   前端      │      │   後端      │      │   Jina AI   │
│ (Streamlit) │◄────►│  (FastAPI)  │◄────►│  Reader API │
└─────────────┘      └─────────────┘      └─────────────┘
                           ▲                     ▲
                           │                     │
                           ▼                     ▼
                     ┌─────────────┐      ┌─────────────┐
                     │   資料庫    │      │  目標網站   │
                     │ (Supabase)  │      │(Career Pages)│
                     └─────────────┘      └─────────────┘
```

## 資料模型設計

### 用戶 (Users)
- id: UUID (主鍵)
- email: String (唯一)
- full_name: String
- created_at: Timestamp
- updated_at: Timestamp
- google_id: String (外部身份)
- is_active: Boolean

### 履歷 (Resumes)
- id: UUID (主鍵)
- user_id: UUID (外鍵 -> Users)
- content: Text (經過處理的履歷內容)
- skills: Array[String]
- experience: Array[JSON]
- education: Array[JSON]
- created_at: Timestamp
- updated_at: Timestamp

### 追蹤頁面 (Tracked Pages)
- id: UUID (主鍵)
- user_id: UUID (外鍵 -> Users)
- url: String
- company_name: String
- check_frequency: String (daily/weekly)
- last_checked: Timestamp
- created_at: Timestamp
- updated_at: Timestamp

### 職缺 (Jobs)
- id: UUID (主鍵)
- tracked_page_id: UUID (外鍵 -> Tracked Pages)
- job_title: String
- job_url: String
- job_description: Text
- location: String
- department: String
- extracted_skills: Array[String]
- status: String (new/seen/notified)
- first_seen: Timestamp
- created_at: Timestamp
- updated_at: Timestamp

### 通知 (Notifications)
- id: UUID (主鍵)
- user_id: UUID (外鍵 -> Users)
- job_id: UUID (外鍵 -> Jobs)
- match_score: Float
- email_sent: Boolean
- sent_at: Timestamp
- created_at: Timestamp

## API 端點設計

### 身份驗證
- `POST /auth/google/login` - 啟動 Google 登入流程
- `GET /auth/google/callback` - 處理 Google 回調
- `POST /auth/logout` - 退出登入

### 用戶
- `GET /users/me` - 獲取當前用戶資訊
- `PUT /users/me` - 更新用戶資訊

### 履歷
- `POST /resumes` - 上傳履歷
- `GET /resumes` - 獲取履歷列表
- `GET /resumes/{id}` - 獲取特定履歷
- `PUT /resumes/{id}` - 更新履歷
- `DELETE /resumes/{id}` - 刪除履歷

### 追蹤頁面
- `POST /tracked-pages` - 添加追蹤頁面
- `GET /tracked-pages` - 獲取追蹤頁面列表
- `GET /tracked-pages/{id}` - 獲取特定追蹤頁面
- `PUT /tracked-pages/{id}` - 更新追蹤頁面
- `DELETE /tracked-pages/{id}` - 刪除追蹤頁面

### 職缺
- `GET /jobs` - 獲取職缺列表
- `GET /jobs/{id}` - 獲取特定職缺詳情

### 通知
- `GET /notifications` - 獲取通知列表
- `GET /notifications/{id}` - 獲取特定通知詳情
- `PUT /notifications/{id}/read` - 標記通知為已讀

## 爬蟲模組設計

### 爬蟲模組設計原則
- 使用 Jina AI Reader API 將職缺頁面轉換為適合 LLM 處理的 Markdown 格式
- 使用非阻塞模式爬取目標網站
- 實現智能休眠和重試機制，避免被目標網站封鎖
- 為不同網站設計專用解析器 (Parser)
- 提供通用解析器用於快速添加新網站支持

### 爬蟲流程
1. **URL獲取**: 從數據庫中獲取需要爬取的職缺頁面URL
2. **頁面轉換**: 使用 Jina AI Reader API (`r.jina.ai`) 將職缺頁面轉換為結構化的 Markdown 格式
3. **內容處理**: 將 Markdown 格式的內容傳遞給 LLM 進行職缺識別與結構化
4. **數據提取**: 使用 LLM 從頁面內容中提取職缺標題、描述、要求等信息
5. **數據存儲**: 將提取的職缺信息存儲到數據庫

### POC 階段簡化實現
- 初期使用定時腳本替代複雜的調度系統
- 使用同步處理模式簡化實現
- 專注於確保數據準確性而非系統效能
- 優先實現核心功能流程

## 匹配算法設計

### 核心功能
- 從履歷和職缺描述中提取關鍵技能和經驗
- 使用 TF-IDF 和其他 NLP 技術計算相似度
- 考慮用戶的工作經驗年限和教育背景
- 計算匹配分數並決定是否發送通知

### 匹配流程
1. 提取履歷中的技能、經驗和教育信息
2. 提取職缺描述中的技能需求和其他要求
3. 計算技能匹配度
4. 評估經驗匹配度
5. 評估教育背景匹配度
6. 計算總體匹配分數
7. 如果分數超過閾值，發送通知

## 前端頁面設計

### 主要頁面
- **登入頁面**: Google 登入入口
- **儀表板**: 概覽用戶的追蹤頁面和通知
- **履歷管理**: 上傳和管理履歷
- **追蹤頁面管理**: 添加和管理追蹤的公司職缺頁面
- **職缺瀏覽**: 查看所有匹配的職缺
- **通知設置**: 配置通知頻率和偏好

### UI/UX 設計原則
- 清晰簡潔的界面
- 響應式設計，支持移動設備
- 友好的錯誤處理和用戶反饋
- 漸進式加載大型數據集

## 安全性考量

### 資料安全
- 所有敏感數據使用 AES-256 加密存儲
- 履歷數據標準化處理後僅保留結構化信息
- 定期數據備份

### 認證與授權
- 基於 JSON Web Token (JWT) 的認證系統
- 細粒度的權限控制
- CSRF 和 XSS 防護

### 合規性
- 遵循 GDPR 和相關數據隱私法規
- 實現數據刪除和導出功能
- 用戶同意機制

## 開發流程與規範

### 代碼風格
- 使用 PEP 8 Python 代碼風格
- 使用 Black 和 isort 自動格式化代碼
- 所有函數和類必須有完整的文檔字符串 (Docstrings)

### 開發流程
- 使用 feature branches 進行開發
- 提交訊息遵循 Conventional Commits 規範
- 代碼審查流程

### 測試策略
- 單元測試覆蓋核心功能
- 集成測試確保系統組件協同工作
- 端到端測試驗證關鍵用戶流程

## 部署與監控

### 部署流程
- 使用 Docker 容器化應用
- 使用 Conda 環境管理依賴
- 分開的開發、測試和生產環境

### 監控與日誌
- 使用 Prometheus 和 Grafana 監控系統性能
- ELK Stack 處理日誌
- 自動報警系統

## 擴展性與未來計劃

### 短期可擴展功能
- 添加更多預定義的企業爬蟲
- 改進匹配算法
- 添加更多前端自定義選項

### 中長期願景
- 集成 AI 推薦系統
- 添加求職申請跟蹤功能
- 開發移動應用
- 添加高級分析和見解功能 