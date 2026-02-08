from matplotlib import pyplot as plt
import pandas as pd
import numpy as np

from matplotlib import font_manager, rc
font_path = "/System/Library/Fonts/Supplemental/AppleGothic.ttf"
font = font_manager.FontProperties(fname=font_path).get_name()
rc('font', family=font)

sheet = pd.read_csv("/Users/isgeun/Library/Mobile Documents/iCloud~md~obsidian/Documents/NOTE/3 리소스/사람들/엄마/병합풀기-붙임 2023학년도 사립유치원 확정원비 취합-최종 - 2023-03-28 기준/확정원비(2023)-표 1.csv")

pd.set_option('display.max_rows', None)
pd.set_option('display.max_columns', None)
# curriculum
curriculum = np.array(sheet.loc[:, ["교육과정 교육비 - 입학졸업경비(월 평균)", "교육과정 교육비(월 평균)"]])

for i in range(curriculum.shape[0]):
    curriculum[i][0] = int(curriculum[i][0].replace(",", ""))
    curriculum[i][1] = int(curriculum[i][1].replace(",", ""))

curriculum_sum = np.empty(curriculum.shape[0], dtype=int)

for i in range(curriculum.shape[0]):
    curriculum_sum[i] = curriculum[i][0] + curriculum[i][1]
# after_school
after_school = np.array(sheet.loc[:, ["방과후과정 교육비(월 평균)"]])
after_school = after_school.reshape(after_school.shape[0])

for i in range(after_school.shape[0]):
    after_school[i] = int(after_school[i].replace(",", ""))
#cram_school
cram_school = curriculum_sum + after_school

sorted_curriculum_sum = curriculum_sum.copy(); sorted_curriculum_sum.sort(); sorted_after_school = after_school.copy(); sorted_after_school.sort(); sorted_cram_school = cram_school.copy(); sorted_cram_school.sort()

money = {}; average = {}; percent = {}
# money
# west 0-37, south: 38-89, north: 90-135, dongrae: 136-179, haeundae:180-230
money["curriculum_sum"] = {}; money["curriculum_sum"]["total"] = curriculum_sum
money["curriculum_sum"]["west"] = curriculum_sum[0:38]; money["curriculum_sum"]["south"] = curriculum_sum[38:90]; money["curriculum_sum"]["north"] = curriculum_sum[90:136]; money["curriculum_sum"]["dongrae"] = curriculum_sum[136:180]; money["curriculum_sum"]["haeundae"] = curriculum_sum[180:231]

money["after_school"] = {}; money["after_school"]["total"] = after_school
money["after_school"]["west"] = after_school[0:38]; money["after_school"]["south"] = after_school[38:90]; money["after_school"]["north"] = after_school[90:136]; money["after_school"]["dongrae"] = after_school[136:180]; money["after_school"]["haeundae"] = after_school[180:231]

money["cram_school"] = {}; money["cram_school"]["total"] = cram_school
money["cram_school"]["west"] = cram_school[0:38]; money["cram_school"]["south"] = cram_school[38:90]; money["cram_school"]["north"] = cram_school[90:136]; money["cram_school"]["dongrae"] = cram_school[136:180]; money["cram_school"]["haeundae"] = cram_school[180:231]
# average
average["curriculum_sum"] = int(curriculum_sum.sum()/curriculum_sum.size); average["after_school"] = int(after_school.sum()/
after_school.size); average["cram_school"] = int(cram_school.sum()/cram_school.size)
# percent
percent["curriculum_sum"] = []; percent["curriculum_sum"].append([25,sorted_curriculum_sum[int(curriculum_sum.size/4)]]); percent["curriculum_sum"].append([50, sorted_curriculum_sum[int(sorted_curriculum_sum.size/2)]]); percent["curriculum_sum"].append([75, sorted_curriculum_sum[int(sorted_curriculum_sum.size*3/4)]]); percent["curriculum_sum"].append([100, sorted_curriculum_sum[-1]]); percent["curriculum_sum"].append([5,sorted_curriculum_sum[int(curriculum_sum.size/20)]]); percent["curriculum_sum"].append([10,sorted_curriculum_sum[int(curriculum_sum.size/10)]]); percent["curriculum_sum"].append([90,sorted_curriculum_sum[int(curriculum_sum.size*9/10)]]); percent["curriculum_sum"].append([95,sorted_curriculum_sum[int(curriculum_sum.size*19/20)]]);

percent["after_school"] = []; percent["after_school"].append([25,sorted_after_school[int(after_school.size/4)]]); percent["after_school"].append([50, sorted_after_school[int(sorted_after_school.size/2)]]); percent["after_school"].append([75, sorted_after_school[int(sorted_after_school.size*3/4)]]); percent["after_school"].append([100, sorted_after_school[-1]]); percent["after_school"].append([5,sorted_after_school[int(after_school.size/20)]]); percent["after_school"].append([10,sorted_after_school[int(after_school.size/10)]]); percent["after_school"].append([90,sorted_after_school[int(after_school.size*9/10)]]); percent["after_school"].append([95,sorted_after_school[int(after_school.size*19/20)]]);

percent["cram_school"] = []; percent["cram_school"].append([25,sorted_cram_school[int(cram_school.size/4)]]); percent["cram_school"].append([50, sorted_cram_school[int(sorted_cram_school.size/2)]]); percent["cram_school"].append([75, sorted_cram_school[int(sorted_cram_school.size*3/4)]]); percent["cram_school"].append([100, sorted_cram_school[-1]]); percent["cram_school"].append([5,sorted_cram_school[int(cram_school.size/20)]]); percent["cram_school"].append([10,sorted_cram_school[int(cram_school.size/10)]]); percent["cram_school"].append([90,sorted_cram_school[int(cram_school.size*9/10)]]); percent["cram_school"].append([95,sorted_cram_school[int(cram_school.size*19/20)]]);

# plt
for key in money.keys():
    plt.figure(figsize=(14,7))
    slice_count = 40

    slice_interval = (money[key]["total"].max() - money[key]["total"].min()) / slice_count
    slice = {}; slice["money"] = []; slice["frequence"] = []
    for i in range(slice_count):
        slice_i = money[key]["total"].min() + i*slice_interval; slice_i_plus_1 = slice_i + slice_interval
        slice_money = (slice_i_plus_1 + slice_i)/2
        slice["money"].append(slice_money)
        slice_mask = np.logical_and(slice_i <= money[key]["total"], money[key]["total"] < slice_i_plus_1)
        slice_frequnce = money[key]["total"][slice_mask].size
        if i == slice_count-1:
            slice["frequence"].append(slice_frequnce+1)
        else:
            slice["frequence"].append(slice_frequnce)

    yticks_array = [freq for freq in slice["frequence"]]

    plt.plot(slice["money"], slice["frequence"], linestyle="-")
    # guideline
    for ele in yticks_array:
        plt.plot([min(slice["money"]), max(slice["money"])], [ele, ele],linestyle="--", color="gray", alpha=0.3)
    # average
    plt.plot([average[key], average[key]], [min(slice["frequence"]), max(slice["frequence"])], color="orange", marker= 'o', linestyle="--", label="평균")
    plt.text(average[key], max(slice["frequence"]), color="orange", s=f"{average[key]}원")

    for percent_ele in percent[key]:
        percent_number = percent_ele[0]
        percent_money = percent_ele[1]
        if percent_number%25 == 0:
            plt.plot([percent_money, percent_money], [min(slice["frequence"])-3, min(slice["frequence"])-3], color="red", marker="^", linestyle="--", label=f"{percent_number}%", alpha=percent_number/100)
        else:
            if percent_number == 5:
                plt.plot([percent_money, percent_money], [min(slice["frequence"]), max(slice["frequence"])], color="green", marker="o", linestyle="--", label=f"{percent_number}%", alpha=0.5)
                plt.text(percent_money, max(slice["frequence"])*9/10 + min(slice["frequence"])*1/10, color="green", s=f"{percent_money}원")
            elif percent_number == 10:
                plt.plot([percent_money, percent_money], [min(slice["frequence"]), max(slice["frequence"])], color="blue", marker="o", linestyle="--", label=f"{percent_number}%", alpha=0.5)
                plt.text(percent_money, max(slice["frequence"]), color="blue", s=f"{percent_money}원")
            elif percent_number == 90:
                plt.plot([percent_money, percent_money], [min(slice["frequence"]), max(slice["frequence"])], color="purple", marker="o", linestyle="--", label=f"{percent_number}%", alpha=0.5)
                plt.text(percent_money, max(slice["frequence"])*9/10 + min(slice["frequence"])*1/10, color="purple", s=f"{percent_money}원")
            else:
                plt.plot([percent_money, percent_money], [min(slice["frequence"]), max(slice["frequence"])], color="black", marker="o", linestyle="--", label=f"{percent_number}%", alpha=0.5)
                plt.text(percent_money, max(slice["frequence"]), color="black", s=f"{percent_money}원")
            
    for south_ele in money[key]["south"]:
        plt.plot([south_ele, south_ele], [min(slice["frequence"])-0.5, min(slice["frequence"])-0.5], color="blue", marker="o", markersize=1, alpha=0.3)
    plt.plot([south_ele, south_ele], [min(slice["frequence"])-0.5, min(slice["frequence"])-0.5], color="blue", label="남부", alpha=1)

    for west_ele in money[key]["west"]:
        plt.plot([west_ele, west_ele], [min(slice["frequence"])-1, min(slice["frequence"])-1], color="purple", marker="o", markersize=1, alpha=0.3)
    plt.plot([west_ele, west_ele], [min(slice["frequence"])-1, min(slice["frequence"])-1], color="purple", label="서부", alpha=1)

    for north_ele in money[key]["north"]:
        plt.plot([north_ele, north_ele], [min(slice["frequence"])-1.5, min(slice["frequence"])-1.5], color="green", marker="o", markersize=1, alpha=0.3)
    plt.plot([north_ele, north_ele], [min(slice["frequence"])-1.5, min(slice["frequence"])-1.5], color="green", label="북부", alpha=1)

    for dongrae_ele in money[key]["dongrae"]:
        plt.plot([dongrae_ele, dongrae_ele], [min(slice["frequence"])-2, min(slice["frequence"])-2], color="black", marker="o", markersize=1, alpha=0.3)
    plt.plot([dongrae_ele, dongrae_ele], [min(slice["frequence"])-2, min(slice["frequence"])-2], color="black", label="동래", alpha=1)

    for haeundae_ele in money[key]["haeundae"]:
        plt.plot([haeundae_ele, haeundae_ele], [min(slice["frequence"])-2.5, min(slice["frequence"])-2.5], color="gray", marker="o", markersize=1, alpha=0.3)
    plt.plot([haeundae_ele, haeundae_ele], [min(slice["frequence"])-2.5, min(slice["frequence"])-2.5], color="gray", label="해운대", alpha=1)

    if key == "curriculum_sum":
        plt.title("교육과정 교육비")
    elif key == "after_school":
        plt.title("방과후과정 교육비")
    else:
        plt.title("원비")
    plt.yticks(yticks_array)
    plt.ylabel("유치원수(개수)")
    plt.xlabel("금액(원)")
    plt.legend(loc='upper left', bbox_to_anchor=(1, 1))
    plt.savefig(f"/Users/isgeun/Library/Mobile Documents/iCloud~md~obsidian/Documents/NOTE/3 리소스/사람들/엄마/병합풀기-붙임 2023학년도 사립유치원 확정원비 취합-최종 - 2023-03-28 기준/{key}.png")

# print(money)
# print(average)
# print(percent)
