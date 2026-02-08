import re
import os

"""
Vault의 모든 md 파일이 Vault의 md 파일만을 링크로 참조한다고 가정한다.

Obsidian의 '새로 만드는 경로 형식'을 '파일에 대한 상대 경로'로 지정하면 굳이 여기서 작성하고자 하는 파이썬 파일 완성시킬 필요가 없다. '바퀴를 재발명하지 마라'에 따르면.
하지만, Obsidian이 제공하는 위 기능을 포함하는 파이썬 코드를 작성하고자 한다면 파이썬 파일을 완성시킬 필요는 있다.
"""

root_dir = "/Users/isgeun/Library/Mobile Documents/iCloud~md~obsidian/Documents/NOTE - iCloud Drive/"
    
link_prefixs = os.listdir(root_dir); link_prefixs = [_ for _ in link_prefixs if '.' not in _]
{}
file = "/Users/isgeun/Library/Mobile Documents/iCloud~md~obsidian/Documents/NOTE - iCloud Drive/0 Unclassified/쿠폰 모음.md"

with open(file, 'r') as f:
    cur_dir = os.path.dirname(file); cur_dir = cur_dir.replace(root_dir, '')
    print(cur_dir)
    wholeline = f.readlines(); wholeline = "".join(wholeline)
    # 파일 경로를 상대 경로로 바꾸기
    for i, link_prefix in enumerate(link_prefixs):
        link_prefix = link_prefix.replace(' ', "%20")
        not_brackets_parentheses = r"[^\[\]\(\)]"
        p = re.compile(fr"!?\[{not_brackets_parentheses}*\]\(({link_prefix}{not_brackets_parentheses}*)\)")
        matchers = re.finditer(p, wholeline)
        print(i)
        for matcher in matchers:
            print(matcher.groups(), matcher.start(), matcher.end())
        
        
        