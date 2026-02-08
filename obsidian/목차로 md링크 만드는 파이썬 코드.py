import sys
import os

# 각 목차에 해당하는 폴더가 있고, 그 폴더에 목차에 대한 파일과 Attachment라는 첨부 폴더가 저장된다는 가정으로 작성된 파이썬 파일이다.
# 목차 파일 하나가 있고, 목차 파일의 첨부파일을 담는 0 Attachment 디렉토리가 동일한 depth에 위치하여 하위 디렉토리에 목차의 첨부 파일을 담는 디렉토리를 생성할 수 있도록 한다.
# 근데, 목차 파일만 생성하고 이에 대한 링크만 생성해도 무방하다.
# 근데 더 중요한 건 목차에 따라 자동으로 md 파일을 생성하여 링크를 거는 것이 필요가 없다. 수동으로 링크를 걸어서 반복적으로 보는 것이 공부하는 데에 도움이 되기 때문이다.
# * 여기서 중요한 것은 이 파이썬 파일을 고치다 말아서 제대로 작동하지 않을 수 있다는 것이다. 확인해야 알긴 한다.

NEG_INF = -98765
index_list_file_path_count = sys.argv.__len__()
index_list_file_path = None
index_list_file_path = "/Users/isgeun/Library/Mobile Documents/iCloud~md~obsidian/Documents/NOTE/1 프로젝트/포너블/목차 리스트 - 드림핵 리버스 엔지니어링 강의.md"

select_path_in_python_code = (index_list_file_path != None)
select_path_in_terminal = (index_list_file_path_count == 2)
if select_path_in_python_code:
    pass
elif select_path_in_terminal:
    index_list_file_path = sys.argv[1]
else:
    print("인자 하나를 경로로 무조건 전달하거나 파이썬 코드에서 경로를 지정하세요.")
    sys.exit(0)

def init_index_list(index_list, index_list_file_path):
    with open(index_list_file_path, 'r') as index_list_file:
        continue_while_loop = True
        while continue_while_loop:
            index = index_list_file.readline()
            
            is_last_line = (index[-1] != '\n')
            if is_last_line:
                continue_while_loop = False
            
            index_list.append(index)

def remove_empty_index(index_list):
    for i, index in enumerate(index_list):
        index_is_empty = True
        for index_char in index:
            is_white_space = index_char != ' ' and index_char != '\t' and index_char != '\n'
            if is_white_space:
                index_is_empty = False
                break
            
        if index_is_empty:
            index_list.pop(i)

def attach_prefix(index_list):
    def attach_prefix_in_element(index_list, pos, prefix):
        index_list[pos] = index_list[pos].lstrip()
        if index_list[pos][0].isdecimal():
            prefix = prefix + " - "
        else:
            prefix = prefix + " "
        
        index_list[pos] = prefix + index_list[pos]
    
    def count_indent_depth_for_white_space(index):
        '''
        목차 한 줄의 들여쓰여진 정도를 출력함
        '''
        indent_depth = 0
        # indent("    ", "\t")를 제거할 때마다 indent_depth의 개수를 1 증가시킴
        while (index[0:4] == "    ") or (index[0] == "\t"):
            indent_depth += 1
            
            if index[0:4] == "    ":
                index = index[4:]
            if index[0] == "\t":
                index = index[1:]
        # indent("    ", "\t")를 제거하고도 white space(" ", "\t")이 남아 있다면 indent_depth를 -1로 만듦으로써 에러 표시
        if index[0] == "\t" or index[0] == " ":
            indent_depth = NEG_INF
            
        return indent_depth
    # index_pos = 0에 prefix 넣기
    index_pos = 0
    cur_indent_depth = count_indent_depth_for_white_space(index_list[index_pos])
    
    prefix = "1"
    
    attach_prefix_in_element(index_list, index_pos, prefix)
    # index_pos >= 1에 prefix 넣기
    for index_pos in range(1, len(index_list[1:])+1):
        pre_indent_depth = cur_indent_depth
        cur_indent_depth = count_indent_depth_for_white_space(index_list[index_pos])
        
        subtraction_cur_depth_to_pre_depth = cur_indent_depth - pre_indent_depth
        if cur_indent_depth == NEG_INF:
            print(f"들여쓰기 한 번이 공백 4칸이거나 탭이 아닙니다. in line {index_pos+1}")
            sys.exit(0)
        elif subtraction_cur_depth_to_pre_depth >= 2:
            print(f"들여쓰기 깊이가 올바르지 않습니다.(depth:{pre_indent_depth} -> depth:{cur_indent_depth} in line {index_pos+1})")
            sys.exit(0)
        elif subtraction_cur_depth_to_pre_depth == 1:
            prefix = prefix + "-1"
        elif subtraction_cur_depth_to_pre_depth == 0:
            last_hyphen_pos = prefix.rfind('-')
            prefix = prefix[:last_hyphen_pos+1] + str(int(prefix[last_hyphen_pos+1:]) + 1)
        else:
            hyphen_count = abs(subtraction_cur_depth_to_pre_depth)
            
            while not (hyphen_count == 0):
                last_hyphen_pos = prefix.rfind('-')
                prefix = prefix[:last_hyphen_pos]
                hyphen_count -= 1
            
            last_hyphen_pos = prefix.rfind('-')
            find_last_hyphen = last_hyphen_pos != -1
            if find_last_hyphen:
                prefix = prefix[:last_hyphen_pos+1] + str(int(prefix[last_hyphen_pos+1:]) + 1)
            else:
                prefix = str(int(prefix) + 1)
            
        attach_prefix_in_element(index_list, index_pos, prefix)

def make_md_file_and_directories(index_list):
    index_list_file_dir = os.path.dirname(index_list_file_path)
    root_dir = f'{index_list_file_dir}/md_files_and_directories'
    is_there_root_dir = os.path.isdir(root_dir)
    if is_there_root_dir:
        pass
    else:
        os.mkdir(root_dir)
        
    os.system(f"touch '{root_dir}/0 directory file.md'")
        
    for index in index_list:
        replacement_table = str.maketrans({'\n': '', "'": '', ":": "-", "\\": "-", "/": "-"})
        replaced_index_without_newline = index.translate(replacement_table)
            
        index_md_file_dir = f'{root_dir}/{replaced_index_without_newline}'
        is_there_index_md_file_dir = os.path.isdir(index_md_file_dir)
        if is_there_index_md_file_dir:
            pass
        else:
            os.mkdir(index_md_file_dir)

        os.system(f"touch '{index_md_file_dir}/{replaced_index_without_newline}.md'")

def fill_md_files_with_links(index_list):
    def count_indent_depth_for_prefix(index):
        indent_depth = 0
        first_space_pos = index.find(' ')
        prefix = index[:first_space_pos]
        
        hyphen_pos = prefix.rfind('-')
        while not (hyphen_pos == -1):
            indent_depth += 1
            prefix = prefix[:hyphen_pos]
            hyphen_pos = prefix.rfind('-')
        
        return indent_depth
    
    def convert_link(index):
        if index[-1] == '\n':
            replaced_index_without_newline = index[:-1].replace(":", "-").replace("\\", "-").replace("/", "-").replace("'", "")
        else:
            replaced_index_without_newline = index.replace(":", "-").replace("\\", "-").replace("/", "-").replace("'", "")
        alt = replaced_index_without_newline
        url = replaced_index_without_newline.replace(" ", "%20")
        return f"- [{alt}](md_files_and_directories/{url}/{url}.md)\n"
    
    max_indent_depth = 0
    for index in index_list:
        cur_indent_depth = count_indent_depth_for_prefix(index)
        if max_indent_depth < cur_indent_depth:
            max_indent_depth = cur_indent_depth
    
    index_poses_for_indent_depth = []
    for i in range(max_indent_depth+1):
        index_poses_for_indent_depth.append([])
    
    for i, index in enumerate(index_list):
        cur_indent_depth = count_indent_depth_for_prefix(index)
        index_poses_for_indent_depth[cur_indent_depth].append(i)
    
    index_list_file_dir = os.path.dirname(index_list_file_path)
    root_dir = f'{index_list_file_dir}/md_files_and_directories'
    
    with open(f'{root_dir}/0 목차/0 목차.md', 'w') as f:
        f.write('\n')
        zero_depth = 0
        for index_pos in index_poses_for_indent_depth[zero_depth]:
            index = index_list[index_pos]
            index_link = convert_link(index)
            f.write(index_link)
    
    index_poses_for_indent_depth_without_last = index_poses_for_indent_depth[:-1]
    for cur_indent_depth, cur_index_poses in enumerate(index_poses_for_indent_depth_without_last):
        next_indent_depth = cur_indent_depth + 1
        next_index_poses = index_poses_for_indent_depth[next_indent_depth]
        for cur_index_pos_location, cur_index_pos in enumerate(cur_index_poses):
            next_index_pos_location = cur_index_pos_location + 1
            if next_index_pos_location == cur_index_poses.__len__():
                next_index_pos = index_list.__len__()
            else:
                next_index_pos = cur_index_poses[next_index_pos_location]
                
            cur_index = index_list[cur_index_pos]
            if cur_index[-1] == '\n':
                replaced_cur_index_without_newline = cur_index[:-1].replace(":", "-").replace("\\", "-").replace("/", "-").replace("'", "")
            else:
                replaced_cur_index_without_newline = cur_index.replace(":", "-").replace("\\", "-").replace("/", "-").replace("'", "")
            with open(f'{root_dir}/{replaced_cur_index_without_newline}/{replaced_cur_index_without_newline}.md', 'w') as f:
                index_poses_to_be_insert = list(filter(lambda x: cur_index_pos < x and x < next_index_pos, next_index_poses))
                if index_poses_to_be_insert == []:
                    continue
                f.write('\n')
                for index_pos in index_poses_to_be_insert:
                    index = index_list[index_pos]
                    index_link = convert_link(index)
                    f.write(index_link)

if __name__ == "__main__":
    index_list = []
    init_index_list(index_list, index_list_file_path)
    remove_empty_index(index_list)
    
    if index_list == []:
        print("파일에 입력된 내용이 없음")
        sys.exit(0)
    
    attach_prefix(index_list)
    make_md_file_and_directories(index_list)
    fill_md_files_with_links(index_list)
