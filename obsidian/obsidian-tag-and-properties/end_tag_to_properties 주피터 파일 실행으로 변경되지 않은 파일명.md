뭔가 파일명에 보이지 않는 문자가 있어서 제대로 작동이 안 된 건지 모르겠다. 어떨 때는 도 된다. 파일명과 폴더명을 동일한 이름으로 둘 다 바꾸다 보면 된다.

1. 모든 개발자를 위한 HTTP 웹 기본 지식
2. Abraham Silberschatz, Greg Gagne, Peter B. Galvin - Operating System Concepts - 2018, Wiley
3. Node.js로 서버 만들기
4. 쉽게 시작하는 타입스크립트
5. 그림으로 배우는 보안 구조
6. 핵심 딥러닝 입문
7. Foundations of Algorithms - Richard E. Neapolitan
8. J. Milnor, Topology from the differentiable view point
9. Real Analysis H.L. Royden · P.M. Fitzpatric

```python
import re
import os
```

```python
path = "/Users/isgeun/Library/Mobile Documents/iCloud~md~obsidian/Documents/노트/7 참고 자료"
folder_paths = [path]
not_included_folder = ["attachment"]
```

```python
while not (folder_paths == []):
    cur_folder_path = folder_paths.pop()
    cur_folder_file_name = os.path.basename(cur_folder_path) + ".md"
    
    if not cur_folder_file_name in os.listdir(cur_folder_path):
        pass
    else:
        cur_folder_file_path = cur_folder_path + "/" + cur_folder_file_name
        with open(cur_folder_file_path, "r") as f:
            file_content = f.readlines()
            file_content = "".join(file_content)
        
        end_tag_match = re.search(r"\n+((#[^ \n]+ ?)+)\n+", file_content)
        if end_tag_match == None:
            pass
        else:
            end_tag = end_tag_match.group(1); end_tag = end_tag.replace(" ",""); end_tag = end_tag[1:].split("#")
            
            file_content = file_content[:end_tag_match.start(0)] + file_content[end_tag_match.end(0):] + "\n"
            
            properties_tag = [f"  - {_}\n" for _ in end_tag]; properties_tag = "".join(properties_tag); properties_tag = properties_tag

            split_print = re.search(r"(?<=\n)---(?=\n)", file_content).start(0)
            
            if re.search(r"tags:\n(  - .+\n)+", file_content) != None:
                file_content = file_content[:split_print] + properties_tag + file_content[split_print:]
            else:
                file_content = file_content[:split_print] + "tags:\n" + properties_tag + file_content[split_print:]
            
            with open(cur_folder_file_path, "w") as f:
                f.writelines(file_content)
    
    # * 다음 탐색할 디렉토리 folder_paths에 append
    # 현재 디렉토리에 있는 하위 파일 및 디렉토리
    cur_sub_names = os.listdir(cur_folder_path)
    # 현재 디렉토리에 있는 하위 디렉토리
    cur_sub_folder_names = [_ for _ in cur_sub_names if os.path.isdir(f"{cur_folder_path}/{_}")]
    # not_included_folder에 속한 디렉토리를 제외한 현재 디렉토리에 있는 숨겨지지 않은 하위 디렉토리
    cur_sub_folder_names_without_hidden = [_ for _ in cur_sub_folder_names if _.find(".") == -1]; cur_sub_folder_names_without_hidden = [_ for _ in cur_sub_folder_names_without_hidden if _ not in not_included_folder]
    # folder_paths에 현재 디렉토리의 하위 디렉토리(current_sub_folder_names_without_hidden) 모두 넣음
    for _ in cur_sub_folder_names_without_hidden:
        folder_paths.append(f"{cur_folder_path}/{_}")
    
    print(folder_paths)

```
