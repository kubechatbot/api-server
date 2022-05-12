chat = {
    "내일 날씨" : "화창합니다",
    "구내식당 메뉴" : "돌솥비빔밥"
}


def ret_dic(command):
    if chat.get(command):
        return chat[command]
    else:
        print("등록되지 않은 명령어입니다.")

while True:
    print("명령어를 입력해주세요! 종료하시려면 q를 입력해주세요.")
    comm = input()
    if comm == "q":
        break
    else:
        print(ret_dic(comm))

