import torch
from train import sample_data
from generator import Generator
from config import G_Config
from poem_pre_do import gen_dictionary
import argparse
import os


parser = argparse.ArgumentParser(description="Training Configuration")
parser.add_argument("--cuda", default=None, type=int, help="Set the cuda number")
parser.add_argument("--rand_seed", default=1, type=int, help="Set the random seed number")
parser.add_argument("--poem_num", default=100, type=int, help="Set the poem number to generate")
opt = parser.parse_args()

REAL_DATA_PATH = 'poem/real_data.txt'
FAKE_DATA_PATH = 'poem/fake_data.txt'
EVAL_DATA_PATH = 'poem/eval_data.txt'
ALL_DATA_PATH = 'poem/poetry.txt'
USE_DATA_PATH = 'poem/use_data.txt'
GEN_POEM_PATH = 'poem/gen_poem.txt'

if opt.cuda is not None:
    os.environ["CUDA_VISIBLE_DEVICES"] = str(opt.cuda)
print('Generating word dictionary...')
word_to_ix, ix_to_word = gen_dictionary(ALL_DATA_PATH)
word_dim = len(word_to_ix)
g_config = G_Config(dict_size=word_dim, seq_len=50)
g_config.cuda = opt.cuda
print('Loading model...')
my_model = Generator(g_config)
my_model.load_state_dict(torch.load('checkpoints/my_model.pth', map_location='cpu'))
if opt.cuda is not None:
    my_model.cuda()
print('Sampling poem data...')
sample_data(model=my_model, save_path=USE_DATA_PATH,
                sample_num=opt.poem_num, seq_len=g_config.seq_len)
print('Translating poem...')
with open(USE_DATA_PATH) as f:
    gen_poem = open(GEN_POEM_PATH, 'w')
    for line in f:
        decoded_poem = line.split(' ')
        poem = []
        for i in range(len(decoded_poem)-1):
            poem.append(ix_to_word[decoded_poem[i]])
        poem = ''.join(poem)
        gen_poem.write(poem+'\n')
    gen_poem.close()
print('Done!')