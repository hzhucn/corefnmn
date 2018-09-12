"""Copyright (c) Facebook, Inc. and its affiliates.
All rights reserved.

This source code is licensed under the license found in the
LICENSE file in the root directory of this source tree.

Portions of the source code are from the n2nmn project which
notice below and in LICENSE.n2nmn in the root directory of
this source tree.

Copyright (c) 2017, Ronghang Hu
All rights reserved.
"""

import re, pdb

SENTENCE_SPLIT_REGEX = re.compile(r'(\W+)')
def tokenize(sentence):
    tokens = SENTENCE_SPLIT_REGEX.split(sentence.lower())
    tokens = [t.strip() for t in tokens if len(t.strip()) > 0]
    return tokens

def load_str_list(fname):
    with open(fname) as f:
        lines = f.readlines()
    lines = [l.strip() for l in lines]
    return lines

class VocabDict:
    def __init__(self, vocab_file):
        self.word_list = load_str_list(vocab_file)
        self.word2idx_dict = {w:n_w for n_w, w in enumerate(self.word_list)}
        self.num_vocab = len(self.word_list)
        self.UNK_idx = self.word2idx_dict['<unk>'] \
                                    if '<unk>' in self.word2idx_dict else None

    def idx2word(self, n_w):
        return self.word_list[n_w]

    def word2idx(self, w):
        if w in self.word2idx_dict:
            return self.word2idx_dict[w]
        elif self.UNK_idx is not None:
            return self.UNK_idx
        else:
            raise ValueError('word %s not in dictionary ' + \
                            '(while dictionary does not contain <unk>)' % w);

    def tokenize_and_index(self, sentence):
        inds = [self.word2idx(w) for w in tokenize(sentence)]
        return inds

    # add new tokens for decoding
    def addNewTokens(self, newTokenList):
        for newToken in newTokenList:
            if newToken in self.word_list:
                print('%d already exists in vocabulary!' % newToken);
                continue;

            print('Adding %s to vocabulary' % newToken)
            self.word2idx_dict[self.num_vocab] = newToken;
            self.num_vocab += 1;
