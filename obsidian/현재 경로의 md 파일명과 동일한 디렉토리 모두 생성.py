import os

'''
이건 Folder Note과 비슷하게 '파일' 하나당 '그 파일을 포함하는 폴더'를 만든 후 그 폴더에 '첨부 파일 디렉토리'를 또 만들어서 그 '첨부 파일 디렉토리'에 파일에 첨부된 파일을 넣는 방식을 취할 때 필요한 파이썬 파일이다.
'''

path = "/Users/isgeun/Library/Mobile Documents/iCloud~md~obsidian/Documents/NOTE/1 프로젝트/토익/해커스 토익 Reading"

cur_path_file_dir_names =  os.listdir(path)

md_file_names = []
for file_name in cur_path_file_dir_names:
    file_type_is_md = file_name.find(".md") != -1
    first_char_is_digit = file_name[0].isdigit()
    if file_type_is_md and first_char_is_digit:
        md_file_names.append(file_name)

md_file_names_without_extension = [file_name[:-3] for file_name in md_file_names]
md_file_names_without_extension.sort()

# md 파일과 이름이 같은 디렉토리 간에 이름이 각각 정확히 일치하지 않을 때

# attachment_dir_names = os.listdir(f"{path}/첨부파일")
# attachment_dir_names.sort()
# attachment_dir_names.remove('.DS_Store')

# for i in range(min(md_file_names_without_extension.__len__(), attachment_dir_names.__len__())):
#     print(i, md_file_names_without_extension[i])
#     if md_file_names_without_extension[i] != attachment_dir_names[i]:
#         break

# print('-'*100)

# for j in range(i+1, min(md_file_names_without_extension.__len__(), attachment_dir_names.__len__())):
#     print(j, md_file_names_without_extension[j], attachment_dir_names[j])

# print('-'*100)

# if md_file_names_without_extension.__len__() < attachment_dir_names.__len__():
#     print("-" * 20 + "attachment_dir_names" + "-" * 20)
#     for k in range(j+1, attachment_dir_names.__len__()):
#         print(k, attachment_dir_names[k])
# elif md_file_names_without_extension.__len__() > attachment_dir_names.__len__():
#     print("-" * 20 + "md_file_names_without_extension" + "-" * 20)
#     for k in range(j+1, md_file_names_without_extension.__len__()):
#         print(k, md_file_names_without_extension[k])
# else:
#     pass

# print(md_file_names_without_extension.__len__(), attachment_dir_names.__len__())

os.system(f'mkdir "{path}/첨부파일"')

for md_file_name_without_extension in md_file_names_without_extension:
    os.system(f'mkdir "{path}/첨부파일/{md_file_name_without_extension}"')