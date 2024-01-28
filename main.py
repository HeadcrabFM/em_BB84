# BB84 - эмуляция QKD
# >> просто попробую запргать сначала что знаю юез особого вникания
# 1. просто создаем кубиты и записываем данные в ексель.
# 2. потом реализуем вывод инфы о нужном кванте по номеру.
# 3. реализовывать запутывание с другой парой?)) ну это ближе к ЕПР
# 4. непосредственно сам ББ84

import time  # таймеры?)
import random  # случайные базисы паляризации

# import pandas для сохранения в ехель

print('BB84 QKD protocol emulation\n* * * * * * * * * * * * * * * * * * * * * *')

#
# # класс создаваемых кубитов
class qubit:
    num = int
    basis = int  # 0 - вертикальный базис, 1 - наклонный базис

    def __init__(self, i):
        self.num = i

    def polarize(self):
        self.basis = random.randint(0, 1)

    def print_msg(self):
        print(f'#{self.num}  -->  qubit encoding  -->  qubit polarisation\nbasis: {self.basis}\n')


def remove_key_bin_prefix(key_bin_with_prefix):  # для удаления префикса от bin(key)
    key_bin = key_bin_with_prefix[2:]  # Создаем новую строку, исключая первый символ
    return key_bin


# функция инициализации ключа - вводим и переводим в двоичную систему
def key_init():
    key = int(input('\nВведите передаваемый закрытый ключ: '))
    key_bin = bin(key)  # бин даёт префикс в начале, поэтому убираем его.
    key_bin = remove_key_bin_prefix(key_bin)  # убираем префикс
    return key_bin


# функция отправки последовательности кубитов
# инициализация, поляризация, запись выбранных базисов в список
# выдаёт последовательность выбранных базисов
def send_sqnc(key_bin):
    #    key_bin=key_init()
    print(
        f'Закрытый ключ в двоичной форме: {key_bin}\nдлина: {len(key_bin)} бит\n\n>>   приступаем к инициализации кубитов...\n')
    sender_basis = []
    for i in range(len(key_bin)):
        q = qubit(i + 1)
        qubit.polarize(q)
        sender_basis.append(q.basis)
        qubit.print_msg(q)
    print('Базисы, выбранные отправителем:', end='   ')
    for i in range(len(sender_basis)):
        print(sender_basis[i], end=' ')
    print('\n')
    return sender_basis


# функция получения
def recieve_sqnc(key_bin, sender_basis):
    reciever_basis = []
    for i in range(len(key_bin)):
        q = qubit(i + 1)
        qubit.polarize(q)
        reciever_basis.append(q.basis)
    print('Базисы, выбранные получателем:', end='   ')
    for i in range(len(sender_basis)):
        print(reciever_basis[i], end=' ')
    print('\n')
    return reciever_basis


def compare_basis(sender_b, reciever_b, key_bin):
    print('Исходный закрытый ключ:   ', key_bin, type(key_bin))
    basis_match = []
    final_key = []
    if (len(sender_b) == len(reciever_b)):
        for i in range(len(sender_b)):
            if (sender_b[i] == reciever_b[i]):
                basis_match.append(i + 1)  # сохраняем номера базисов которые совпали
                final_key.append(key_bin[i])
    else:
        print('Something went wrong... the senders and recievers basis list length is not equal :(')
    # по идее надо тут по открытому каналу передавать руг другу выбранные базисы
    print('Номера совпавших базисов:', end='   ')
    for i in range(len(basis_match)):
        print(basis_match[i], end=' ')
    print(f'\n\n>> ИТОГОВЫЙ ЗАКРЫТЫЙ КЛЮЧ:', end='   ')
    for i in range(len(final_key)):
        print(final_key[i], end=' ')
    return final_key


# основная функция квантовой части общая, которая используется для обобщения сендер и ресивер процес
def BB84_em():
    a = 1
    while a != 0:
        key_bin = key_init()  # saving the key for further processing (both sender and reciever will need it)
        sender_basis = send_sqnc(key_bin)  # getting the list of basises randomly chosen by sender
        reciever_basis = recieve_sqnc(key_bin, sender_basis)
        print('\n. . . происходит передача списка выбранных базисов отправителю по открытому каналу . . .'
              # добавить таймер
              '\n. . . отправитель проверяет, какие базисы совпали . . .'
              '\n. . . происходит передача списка совпавших базисов получателю по открытому каналу . . .\n')
        compare_basis(sender_basis, reciever_basis, key_bin)
        a = int(input('\n\n_ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ \n'
                      'TEST COMPLETED. Для продолжения введите 1, для завершения нажмите 0\n'))
    print('* * * * * * * * * * * * * *\npress any key to exit . . .')

BB84_em()

# надо допилить чобы если пустой ключ то он реинициализировал всё.
# и чтобы если короче определенной длины тоже предупредал и заново начинал.
# доделать так чтобы был текст как закрытый ключ. то есть каждая буква кодировалась бы одинаковым количеством бит
# и тогда длина ключа была бы больше чем просто цифры. подумать как
