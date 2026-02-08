import os
import re

save_dir =  "/Users/isgeun/Library/Mobile Documents/iCloud~md~obsidian/Documents/NOTE - iCloud Drive/0 Inbox/"

paths = []
hackers_voca_dir = "/Users/isgeun/Library/Mobile Documents/iCloud~md~obsidian/Documents/NOTE - iCloud Drive/1 Project/Language - English - 해커스 토익 보카 공부하기/0 Attachment/0 해커스 토익 기출 보카/"
hackers_voca_file_name_list = os.listdir(hackers_voca_dir)

for hackers_voca_file_name in hackers_voca_file_name_list:
    paths.append(hackers_voca_dir + hackers_voca_file_name)

reading_voca_dir = "/Users/isgeun/Library/Mobile Documents/iCloud~md~obsidian/Documents/NOTE - iCloud Drive/1 Project/Language - English - 해커스 토익 Reading 공부하기/2 VOCABULARY PART 5, 6/"
reading_voca_file_name_list = os.listdir(reading_voca_dir)

for reading_voca_file_name in reading_voca_file_name_list:
    if "핵심 단어 리스트" in reading_voca_file_name:
        paths.append(reading_voca_dir + reading_voca_file_name)

word_means_dict = {}

# 디렉토리 하위 파일에서 단어와 뜻 모으기
for path in paths:
    with open(path, "r") as f:
        whole_line = f.readlines()
        whole_line = "".join(whole_line)

        p = re.compile(r""" ((?=\s*)\#+\s*)([a-zA-Z]+[^\n]*)(\n+) #word가 포함된 문자열
                            (.+?) # mean가 포함된 문자열
                            (?=\s*\#+) # 탐색 종료를 알려주는 문자열
                            """, re.VERBOSE | re.DOTALL)
        
        found_tuple_list = re.findall(p, whole_line)
            
        for found_tuple in found_tuple_list:
            # found_tuple[1]이 단어, found_tuple[3]이 뜻임
            word = found_tuple[1]
            means = found_tuple[3]; means = re.sub(r"\n+", "; ", means)
            
            if word in word_means_dict:
                word_means_dict[word] = word_means_dict[word] + "; " + means
            else:
                word_means_dict[word] = means
# 중복된 뜻 삭제하기
delete_count = 0
for word in word_means_dict.keys():
    means = word_means_dict[word]
    # means ';'로 분할
    means = means.split('; ')
    # means_depth1(means의 depth1인 원소) ','로 분할(괄호 안의 ',' 무시)
    for i, means_depth1 in enumerate(means):
        means[i] = []
        is_closed = True
        means_depth2_start = 0; means_depth2_end = -1
        
        for means_depth1_ele_idx, means_depth1_ele in enumerate(means_depth1):
            if means_depth1_ele == '(':
                is_closed = False
            elif means_depth1_ele == ')':
                is_closed = True
            
            if is_closed and means_depth1_ele == ',':
                means_depth2_end = means_depth1_ele_idx
                means[i].append(means_depth1[means_depth2_start:means_depth2_end])
                means_depth2_start = means_depth1_ele_idx + 2
            
            if means_depth1_ele_idx == len(means_depth1)-1:
                means[i].append(means_depth1[means_depth2_start:])
    # 딕셔너리를 이용해서 중복된 문자열 삭제
    word_dict = {}
    print
    for i, means_depth1 in enumerate(means):
        for j, means_depth2 in enumerate(means_depth1):
            if means_depth2 in word_dict:
                word_dict[means_depth2].append((i,j))
            else:
                word_dict[means_depth2] = [(i,j)]
    
    for key, idx_2d_list in word_dict.items():
        if len(idx_2d_list) < 2:
            continue
        
        for idx_2d in idx_2d_list[1:]:
            depth1_idx = idx_2d[0]; depth2_idx = idx_2d[1]; 
            means[depth1_idx][depth2_idx] = ""
            delete_count += 1
    # 분할된 문자열 합치기
    for i, means_depth1 in enumerate(means):
        means[i] = ', '.join(means[i])
    means = '; '.join(means)
    # 중복된 단어를 삭제하면서 생긴 공백 삭제, 순서 중요
    means = re.sub(r"(, ){2,}", ', ', means);
    means = re.sub(r"(, ; )+", '; ', means); means = re.sub(r"(; , )+", '; ', means)
    means = re.sub(r"(; ){2,}", '; ', means)
    ## 문자열 마지막에 위치한  ", "와 "; " 삭제
    means = re.sub(r"(; )+$", '', means); means = re.sub(r"(, )+$", '', means)
    
    word_means_dict[word] = means
word
print(f"중복된 뜻이 {delete_count}개 삭제됨")
# 파일로 저장하기
with open(save_dir + "all_word_means.md", "w") as f:
    sorted_words = []
    for word in word_means_dict.keys():
        sorted_words.append(word)
    sorted_words.sort()
    
    for word in sorted_words:
        f.write(word + ": " + word_means_dict[word] + "\n")
    