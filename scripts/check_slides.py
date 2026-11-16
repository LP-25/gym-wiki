#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
scripts/check_slides.py - 投影片草稿自動化檢查腳本
依據教學型 HTML 簡報工作流規範，檢查 output/drafts/ 內的投影片：
(a) 投影片總數必須在 10 到 14 頁之間 (10 <= count <= 14)
(b) 每頁都必須包含 [來源: wiki/...] 的出處標註，且該檔案必須真實存在於 wiki/ 資料夾中
(c) 每頁正文（不含標題與來源標籤）不超過 120 個中文字，避免渲染成 HTML 時文字溢出
"""

import os
import re
import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent
DRAFTS_DIR = PROJECT_ROOT / "output" / "drafts"
WIKI_DIR = PROJECT_ROOT / "wiki"

# 正則表達式
SOURCE_TAG_PATTERN = re.compile(r'\[來源[:：]\s*([^\]]+)\]')
HEADING_PATTERN = re.compile(r'^#{1,6}\s+.*$', re.MULTILINE)
CHINESE_CHAR_PATTERN = re.compile(r'[\u4e00-\u9fa5]')

def extract_body_text(content: str) -> str:
    """提取正文：去除 Markdown 標題、來源標籤與空白行"""
    lines = []
    for line in content.splitlines():
        trimmed = line.strip()
        # 排除標題
        if trimmed.startswith('#'):
            continue
        # 排除獨立的來源標籤行
        if SOURCE_TAG_PATTERN.search(trimmed):
            # 若同一行還有其他字，去除標籤本身
            trimmed = SOURCE_TAG_PATTERN.sub('', trimmed).strip()
        if trimmed:
            lines.append(trimmed)
    return "\n".join(lines)

def check_slides():
    print("=" * 65)
    print("📋 開始檢查教學投影片草稿 (output/drafts/)...")
    print("=" * 65)

    if not DRAFTS_DIR.exists():
        print(f"❌ FAIL: 草稿目錄不存在 -> {DRAFTS_DIR}")
        print("請先執行節點 6 產出 slide-*.md 草稿。")
        return 1

    slide_files = sorted(
        DRAFTS_DIR.glob("slide-*.md"),
        key=lambda p: [int(c) if c.isdigit() else c for c in re.split(r'(\d+)', p.name)]
    )
    total_slides = len(slide_files)

    results = []
    has_errors = False
    failing_slides = []

    # 檢查項 (a): 投影片總數必須在 10 到 14 頁之間
    count_valid = (10 <= total_slides <= 14)
    if not count_valid:
        has_errors = True
        print(f"❌ [檢查項 a 失敗] 投影片總數: {total_slides} 頁 (規範要求: 10 ~ 14 頁)\n")
    else:
        print(f"✅ [檢查項 a 通過] 投影片總數: {total_slides} 頁 (符合 10 ~ 14 頁規範)\n")

    if total_slides == 0:
        print("❌ 目錄中沒有任何 slide-*.md 檔案。")
        return 1

    # 檢查每一頁 (b) 與 (c)
    print(f"{'頁數/檔名':<18} | {'字數 (<=120)':<12} | {'來源出處標註':<22} | {'狀態':<8}")
    print("-" * 65)

    for slide in slide_files:
        content = slide.read_text(encoding='utf-8')
        page_errors = []

        # 1. 檢查項 (c): 中文字數統計
        body = extract_body_text(content)
        chinese_chars = CHINESE_CHAR_PATTERN.findall(body)
        char_count = len(chinese_chars)

        if char_count > 120:
            page_errors.append(f"正文字數超標: {char_count} 字 (上限 120 字)")
            char_status = f"{char_count} 字 (❌)"
        elif char_count == 0:
            page_errors.append("正文為空 (0 字)")
            char_status = "0 字 (❌)"
        else:
            char_status = f"{char_count} 字 (✅)"

        # 2. 檢查項 (b): 來源出處檢查
        source_matches = SOURCE_TAG_PATTERN.findall(content)
        if not source_matches:
            page_errors.append("缺少 [來源: wiki/...] 標籤")
            source_status = "無來源 (❌)"
        else:
            # 驗證引用的檔案是否真實存在於 wiki/
            all_exist = True
            missing_sources = []
            valid_sources = []

            for raw_source in source_matches:
                # 支援逗號或分號分隔多個來源
                parts = [s.strip() for s in re.split(r'[,;]\s*', raw_source)]
                for part in parts:
                    if not part:
                        continue
                    # 移除錨點 #...
                    file_part = part.split('#')[0].strip()
                    # 統一相對路徑
                    if file_part.startswith("wiki/"):
                        rel_path = file_part[len("wiki/"):]
                    else:
                        rel_path = file_part

                    target_file = WIKI_DIR / rel_path
                    if not target_file.exists():
                        all_exist = False
                        missing_sources.append(file_part)
                    else:
                        valid_sources.append(part)

            if not all_exist:
                page_errors.append(f"引用不存在的檔案: {', '.join(missing_sources)}")
                source_status = f"檔案缺失 (❌)"
            elif not valid_sources:
                page_errors.append("來源路徑無效")
                source_status = "格式錯誤 (❌)"
            else:
                source_status = f"{len(valid_sources)} 個來源 (✅)"

        # 匯總單頁狀態
        if page_errors:
            has_errors = True
            failing_slides.append((slide.name, page_errors))
            page_status = "FAIL"
        else:
            page_status = "PASS"

        print(f"{slide.name:<18} | {char_status:<12} | {source_status:<22} | {page_status:<8}")

    print("-" * 65)

    # 輸出最終總結
    if not has_errors:
        print("\n" + "=" * 65)
        print("🎉 檢查結果: ALL PASS (所有投影片均通過規範！)")
        print(f"   • 頁數: {total_slides} 頁 (合規 10~14 頁)")
        print("   • 來源: 每頁皆精準引用真實 wiki/ 檔案")
        print("   • 字數: 每頁正文皆在 120 字內，無溢出風險")
        print("=" * 65)
        return 0
    else:
        print("\n" + "=" * 65)
        print(f"❌ 檢查結果: FAIL (共 {len(failing_slides)} 頁未通過規範，詳情如下)")
        print("=" * 65)
        for name, errs in failing_slides:
            print(f"  • 【{name}】:")
            for err in errs:
                print(f"      - {err}")
        if not count_valid:
            print(f"  • 【頁數問題】: 當前總數 {total_slides} 頁，必須介於 10 到 14 頁之間。")
        print("\n請依據退回機制僅修改上述未通過的頁面後重新檢查。")
        return 1

if __name__ == "__main__":
    sys.exit(check_slides())
