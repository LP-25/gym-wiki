# 知識庫維護與 Ingest 日誌 (Maintenance & Ingestion Log)

本文件依據 [AGENTS.md](../AGENTS.md) 規範，記錄「零基礎重訓與長肌肉入門知識庫」的所有資料匯入（Ingest）、版本演進與品質校驗歷程。

---

## 📅 版本紀錄與 Ingest 歷程

### Phase 2 Ingest：完整 5 篇內容擴充與全量整合 (2026-11-16)
* **處理來源檔案**：
  * `raw/02.txt` / `02.md`（營養師零基礎三個月計畫、膝蓋退化案例、飲食恢復）
  * `raw/04.txt` / `04.md`（吉米教練訪談、10大重訓常識、呼吸腹內壓、四大心態盲區）
  * `raw/05.txt` / `05.md`（新手指南、居家自重/啞鈴/壺鈴/彈力帶、9大動作庫、6-12-25法）
* **頁面更新與新建詳情**：
  * [wiki/exercises.md](exercises.md)：**全新建立**。包含深蹲、臥推、划船、肩推、硬舉、二頭彎舉、三頭伸展、棒式等完整動作步驟；自由重量 vs 固定器械深度剖析；常見代償修正手冊；45歲退化膝關節友善進階路徑。
  * [wiki/nutrition.md](nutrition.md)：**全新建立**。包含每日蛋白質計算公式（1.6～2.0 g/kg）與食物份量對照；碳水化合物角色；練前 1～2 小時與練後 30 分鐘～2 小時飲食組合；水分計算公式（體重 × 30～40 ml）；休息日與睡眠恢復原則。
  * [wiki/faq.md](faq.md)：**全新建立**。彙整 11 大高頻新手迷思與問答（膝蓋退化、金剛芭比、量體重沒變、一週練一天、呼吸腹內壓、划船手痠、在家訓練、超級組/遞減組、6-12-25法、自學請教練、新手四大錯誤）。
  * [wiki/routines.md](routines.md)：**擴充更新**。新增零基礎 12 週三階段漸進期化課表（基礎期、成長期、習慣期）；吉米教練肌耐力入門課表；6-12-25 組合法；跨 5 篇核心訓練參數全對照表。
  * [wiki/principles.md](principles.md)：**擴充更新**。補充肌肉增加與基礎代謝率（每公斤肌肉 +15~30 大卡）；30 歲後肌肉流失率（0.5%~1%）；受傷四大本質原因；呼吸與腹內壓穩定機轉；自由重量神經自主控制優勢。
  * [wiki/glossary.md](glossary.md)：**擴充更新**。新增腹內壓、超級組、遞減組、巨大組、6-12-25訓練法、自由重量、固定器械、自體重量、高腳杯深蹲、羅馬尼亞硬舉、臀推與橋式、蚌殼式等名詞定義。
  * [wiki/index.md](index.md)：**更新導航**。移除預留標籤，所有 6 大核心模組全面上線，加入 log.md 連結。
* **品質驗證**：
  * 執行 `lint_wiki.py`，檢驗通過（0 Errors, 0 Warnings），確認全圖譜零斷裂連結、零孤島頁面、量化數據 100% 標註來源出處。

---

### Phase 1 Ingest：骨架建置與科學實證初版 (2026-11-16)
* **處理來源檔案**：
  * `raw/01.txt` / `01.md`（APPI 編輯部：新手全身課表與超負荷）
  * `raw/03.txt` / `03.md`（Dr. 俊智：分部訓練 vs 全身訓練科學實證）
* **產出成果**：
  * 建立 [AGENTS.md](../AGENTS.md)（維護指南，< 12,000 字元）。
  * 建立 [lint_wiki.py](../lint_wiki.py)（自動化檢驗腳本）。
  * 建立 `wiki/index.md`、`wiki/principles.md`、`wiki/routines.md`、`wiki/glossary.md`。
  * 建立預留結構，完成第一次 Git Commit (`2e65f37`)。

---

## 📊 原始檔案 (raw/) 與知識庫頁面 (wiki/) 對應對照表

| 原始來源檔案 | 主要核心內容萃取 | 匯入對應知識庫頁面 (wiki/) |
| :--- | :--- | :--- |
| **01.txt / 01.md** | 全身課表三動作、8~12 RM 負荷、2%~10% 漸進加重模型、代償修正、熱身共識 | `principles.md`, `routines.md`, `exercises.md`, `glossary.md` |
| **02.txt / 02.md** | 12週三階段期化、45歲膝退化案例、蛋白質1.6~2g/kg、水分公式、新手四大心理錯誤、金剛芭比與體重迷思 | `principles.md`, `routines.md`, `exercises.md`, `nutrition.md`, `faq.md`, `glossary.md` |
| **03.txt / 03.md** | 統合分析增肌實證（Ramos-Campo 2024）、每週可用天數分部架構、3天/6天推拉腿課表與肌群組數 | `principles.md`, `routines.md`, `exercises.md`, `glossary.md` |
| **04.txt / 04.md** | 吉米教練10大常識、站起即重訓、橫膈膜呼吸與腹內壓、肌耐力起跑、自由重量優勢、超級組/遞減組分析 | `principles.md`, `routines.md`, `exercises.md`, `faq.md`, `glossary.md` |
| **05.txt / 05.md** | 自體重量/啞鈴/壺鈴/彈力帶挑選、6大訓練原則、9大入門動作步驟、6-12-25訓練法、安全與放鬆 | `principles.md`, `routines.md`, `exercises.md`, `nutrition.md`, `faq.md`, `glossary.md` |

---

## 🔍 品質檢驗結果紀錄 (Lint Audits)

* **最新檢驗時間**：2026-11-16
* **檢驗腳本**：`lint_wiki.py`
* **頁面總數**：8 個 Markdown 文件 (`index.md`, `principles.md`, `routines.md`, `exercises.md`, `nutrition.md`, `faq.md`, `glossary.md`, `log.md`)
* **檢驗狀態**：**PASS (0 Errors, 0 Warnings)**
  * ✅ 內部連結與錨點：100% 有效，無斷裂連結。
  * ✅ 孤島頁面偵測：所有頁面皆被 index.md 及彼此相互交叉引用。
  * ✅ 數據出處溯源：所有涉及組數、次數、頻率、加重百分比與營養克數之段落皆有 `[^raw/XX.txt]` 出處標記。
  * ✅ 術語表完整性：核心專有名詞皆收錄於 `glossary.md` 並提供雙向導覽。
