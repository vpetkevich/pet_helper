
def get_age(message):
    len_message = len(message)
    integers = 0
    counter = 0
    while counter < len_message:
        number = ''
        current_number = message[counter]
        while '0' <= current_number <= '9':
            number += current_number
            counter += 1
            if counter < len_message:
                current_number = message[counter]
            else:
                break
        counter += 1
        if number != '':
            integers = int(number)
    return integers
