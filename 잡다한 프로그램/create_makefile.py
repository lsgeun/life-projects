from sys import argv, exit
import os

# 메인 프로그램이 아닐 경우 실행하지 않음.
if __name__ == "__main__":
    # 정확히 3개의 매개변수를 입력하지 않을 경우 안내문을 띄운 후 프로그램 종료
    if argv.__len__() != 3+1:
        print("매개변수 정확히 입력하세요.")
        print("예를 들어, python (파이썬 파일).py 123 abc 가나다")
        exit(0)

    # argv[1]은 makefile을 만드는 경로
    path_name = argv[1].replace(' ', '\ ') # 띄어쓰기가 있으면 앞에 역슬래쉬 추가
    os.system('cd ' + path_name + '; touch makefile') # makefile이 존재하지 않는다면 파일을 만든 후
    # stream = os.popen('cd ' + path_name + '; find makefile')
    # exe_result = stream.read().replace("\n", "")
    # if exe_result == "makefile": # makefile이 path_name에 이미 존재한다면
    #     print("makefile이 [" + path_name + "]에 이미 있으므로 makefile을 생성하지 않음.")
    # else: # makefile이 path_name에 존재하지 않는다면
    #     print("makefile이 [" + path_name + "]에 없으므로 makefile을 생성함.")
    print("1. path name: ", path_name)

    # argv[2]는 makefile 파일로 컴파일하고자 하는 파일 이름
    # argv[3]은 makefile에 있는 컴파일러 이름
    file_name = argv[2]
    print("2. file name: ", file_name)

    compiler_name = argv[3]
    print("3. compiler name: ", compiler_name)
    if compiler_name == "gcc":
        file_extension = "c"
    elif compiler_name == "g++":
        file_extension = "cpp"
    else:
        print("올바르지 않은 컴파일 이름, 컴파일러 이름: " + compiler_name)
        print("컴파일러를 gcc나 g++로 설정해주세요.")
        exit(0)

    makefile_contents = []
    makefile_contents.append(".PHONY:clean\n")
    makefile_contents.append(".PHONY:run\n")
    makefile_contents.append("all: " + file_name + "\n")
    makefile_contents.append("\n")
    makefile_contents.append("%.o: %." + file_extension + "\n")
    makefile_contents.append("\t"+ compiler_name + " -g $< -c -o $@\n")
    makefile_contents.append("\n")
    makefile_contents.append(file_name + ": " + file_name + ".o\n")
    makefile_contents.append("\t" + compiler_name + " -o $@ $<\n")
    makefile_contents.append("\n")
    makefile_contents.append("clean: " + file_name + " " + file_name + ".o\n")
    makefile_contents.append("\trm $^\n")
    makefile_contents.append("\n")
    makefile_contents.append("run: " + file_name + "\n")
    makefile_contents.append("\t./$<")
    
    print("4. makefile_contents:")
    for content in makefile_contents:
        print(content, end='')
    print()

    # 파이썬에서 아래의 코드로 파일을 열 때 띄어쓰기 앞에 자동으로 백슬래쉬를 붙이는 것 같아서 띄어쓰기가 포함된 원래 경로를 포함시켜야 제대로 작동함.
    # 여기서 argv[1]를 path_name이라고 생각하면 됨.
    with open(argv[1] + "/makefile", 'w') as makefile:
        for content in makefile_contents:
            makefile.write(content)
        makefile.close()