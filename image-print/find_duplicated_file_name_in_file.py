#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import re
from pathlib import Path
from collections import defaultdict
import urllib.parse

INPUT_FILE = "/Users/isgeun/Library/Mobile Documents/iCloud~md~obsidian/Documents/memo/03_life/프린트/출력한 이미지 프린트물/아빠 사진.md"   # 경로 목록이 들어있는 파일 (한 줄에 한 항목; 마크다운 행 등 섞여도 OK)

# 절대 경로 추출용 정규식 (file://... 또는 /... 형태)
PAT_FILE_URL = re.compile(r'file://[^\s\)\]\|<>"]+')
PAT_ABS_PATH = re.compile(r'/(?:(?:[^\s\)\]\|<>"])+)')  # 맨 앞이 '/' 로 시작하는 절대 경로

def find_paths_in_line(line):
    """한 줄에서 절대 경로(파일 URL 또는 절대 경로)를 모두 찾아 리스트로 반환"""
    found = []

    # 1) file://... 먼저 찾기
    for m in PAT_FILE_URL.findall(line):
        # file:// 처리를 위해 그대로 추가 (디코딩은 이후에)
        found.append(m)

    # 2) /... 형태의 절대경로 (file://에 포함된 것과 중복될 수 있으니 필터)
    for m in PAT_ABS_PATH.findall(line):
        # 만약 m이 file://으로 이미 포함된 것과 동일하면 제외
        # (예: file:///Volumes/... 의 경우 file://... 패턴이 먼저 잡히므로 중복 방지)
        if not any(m in f for f in found):
            found.append(m)

    return found

def normalize_path(raw):
    """file:// 접두어 제거, URL 디코딩, 불필요한 슬래시 정리 후 반환"""
    s = raw
    if s.startswith("file://"):
        # file:// 또는 file:/// 처리 -> 로컬 절대 경로로 만들기
        s = s[len("file://"):]
        # mac/linux: file:///Volumes/... 의 경우 남는 앞의 '/'는 정상적이므로 그대로 둠

    # URL 디코딩 (예: %20 -> space)
    s = urllib.parse.unquote(s)

    # trim quotes or surrounding () if present
    s = s.strip(" '\"")

    return s

def main():
    name_to_paths = defaultdict(list)  # 파일명(stem) -> [절대경로1, 절대경로2, ...]

    with open(INPUT_FILE, "r", encoding="utf-8") as f:
        for raw_line in f:
            line = raw_line.rstrip("\n")
            if not line.strip():
                continue

            # 한 줄에서 절대 경로 후보들 찾기
            candidates = find_paths_in_line(line)

            # 만약 전혀 못 찾았고, 라인이 단순히 '파일명.확장자' 만이라면 그걸 경로로 간주
            if not candidates:
                # 파일명.확장자(예: a.txt) 형식이면 간주
                lone = re.findall(r'\b[^/\s\|]+\.[A-Za-z0-9]+$', line)
                if lone:
                    candidates = [lone[-1]]

            for raw_path in candidates:
                norm = normalize_path(raw_path)
                if not norm:
                    continue

                # Path.stem 사용: '/foo/bar/baz.txt' -> 'baz'
                try:
                    p = Path(norm)
                    stem = p.stem
                except Exception:
                    # 안전망: fallback으로 파일명 추출
                    stem = Path(norm.replace("\\", "/")).name.split(".")[0]

                # 중복된 동일 절대경로는 리스트에 중복 추가하지 않음
                if norm not in name_to_paths[stem]:
                    name_to_paths[stem].append(norm)

    # 출력: 리스트 길이 >= 2 인 것들만(중복으로 간주)
    duplicates = {name: paths for name, paths in name_to_paths.items() if len(paths) >= 2}

    if not duplicates:
        print("✅ 중복된 파일명이 없습니다.")
        return

    print("🔁 중복된 파일명과 해당 절대경로들:")
    for name, paths in sorted(duplicates.items()):
        print()
        print(name)
        for p in paths:
            print(p)

if __name__ == "__main__":
    main()
