def all_digit(my_str: str):
    answer = True
    my_str = my_str.split(' ')
    my_str = ''.join(my_str)
    # print(my_str)
    for i in my_str:
        if not i.isdigit():
            answer = False
            break
    # print(answer)
    return answer
