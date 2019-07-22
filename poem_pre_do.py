def gen_dictionary(data_path):
    # file = open('poem/poetry.txt', 'r', encoding='utf-8')
    file = open(data_path, 'r', encoding='utf-8')
    word_to_ix = {}
    ix_to_word = {}
    count_dic = {}
    no_use_set = [':', '。', '（', '）', '\n']
    for line in file:
        for zi in line:
            if zi in no_use_set:
                continue
            if zi in count_dic.keys():
                count_dic[zi] += 1
            else:
                count_dic[zi] = 1

    file.close()

    ix = 0
    for k in sorted(count_dic, key=count_dic.__getitem__, reverse=True):
        word_to_ix[k] = str(ix)
        ix += 1

    ix = 0
    for k in word_to_ix.keys():
        ix_to_word[str(ix)] = k
        ix += 1

    return word_to_ix, ix_to_word


def gen_real_poem(source_path, output_path, word_to_ix, num):
    a = 0
    file = open(source_path, 'r', encoding='utf-8')
    output_file = open(output_path, 'w', encoding='utf-8')
    for line in file:
        if a >= num:
            break
        try:
            poem = line.split(':')[1]
            left_blanket = poem.find('（')
            while left_blanket != -1:
                poem = poem[:left_blanket] + poem[poem.find('）') + 1:]
                left_blanket = poem.find('（')
            poem = poem.replace('\n', '').replace('\r', '')
            for sentence in poem.split('。')[:-1]:
                ix_poem = []
                for zi in sentence:
                    ix_poem.append(word_to_ix[zi])
                output = " ".join(ix_poem)
                output_file.write(output+'\n')
                a += 1
                if a >= num:
                    break
        except:
            print('fail')
            continue

    file.close()
    output_file.close()


word_to_ix, ix_to_word = gen_dictionary('poem/poetry.txt')
gen_real_poem('poem/poetry.txt', 'poem/real_data.txt', word_to_ix, 10)
