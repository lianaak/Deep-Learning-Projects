from preprocess import pre_process_sentence
import numpy as np
from numpy import random
from collections import Counter

from itertools import islice, chain


        
class TextLoader():
    
    def __init__(self , text_list , min_count = 10):
        
        if isinstance(text_list, list):
            self.data = text_list
        
        self.min_count = min_count
        self.vocab = {}
        self.voc_to_idx = []
        self.vocab_inverse = {}
        self._vocab(self.data)
        self._vocab_inverse()
       
    
        
    def _preprocess(self , text_chunk ):
        return pre_process_sentence(text_chunk)
    
    
    

    def get_batch(self,batch_size):
        sourceiter = iter(self.data)
        if len(self.data) % batch_size == 0:
            iterations = len(self.data) / batch_size
        else:
            iterations = int(len(self.data) / batch_size) + 1
        for i in range(iterations):
            batch_data = islice(sourceiter, batch_size)
            yield chain([next(batch_data)], batch_data)
            

    def make_cum_table(self, power=0.75, domain=2**31 - 1):
        """
        Create a cumulative-distribution table using stored vocabulary word counts for
        drawing random words in the negative-sampling training routines.

        To draw a word index, choose a random integer up to the maximum value in the
        table (cum_table[-1]), then finding that integer's sorted insertion point
        (as if by bisect_left or ndarray.searchsorted()). That insertion point is the
        drawn index, coming up in proportion equal to the increment at that slot.

        Called internally from 'build_vocab()'.
        """
        vocab_size = len(self.index2word)
        self.cum_table = np.zeros(vocab_size, dtype=uint32)
        # compute sum of all power (Z in paper)
        train_words_pow = float(sum([self.vocab[word].count**power for word in self.vocab]))
        cumulative = 0.0
        for word_index in range(vocab_size):
            cumulative += self.vocab[self.index2word[word_index]].count**power / train_words_pow
            self.cum_table[word_index] = round(cumulative * domain)
        if len(self.cum_table) > 0:
            assert self.cum_table[-1] == domain


    def _vocab(self , chunks ):
        
        count = 0
        self.data_index = []
        self.temp_store = []
        for text_ in iter(self.data):
            preprocessed = self._preprocess(text_)
            if preprocessed:
                self.data_index.append(count)
                count += 1
                self.temp_store.extend(preprocessed)

        counter = Counter(self.temp_store)
        words = [k for k, v in counter.items() if v > self.min_count]
        self.vocab = dict(zip(words , range(len(words))))
        self.temp_store = [] 
        

    def _vocab_inverse(self):

        self.vocab_inverse = {k:v for (v, k) in self.vocab.items()}
        self.index2word = self.vocab_inverse

    def _bag_of_words(self , chunk_data , vocab_size = None):
        
        self.voc_to_idx = voc_to_idx = self._vocab_to_idx(chunk_data)
        self.bow = []
        self.dow = []
        if vocab_size is None:
            vocab_size = len(self.vocab)
        self.bow = [np.bincount(idx , minlength=vocab_size) for idx in voc_to_idx]
        self.bow = np.array(self.bow)
        self.dow = self.bow.copy()
        self.dow[self.dow > 0] = 1 
        self.negative_mask = self.dow.copy()
        self.negative_mask[self.negative_mask == 0] = -1
        # self.index_positions = self.get_matrix_position(self.voc_to_idx)

        return self.bow , self.dow , self.negative_mask 

    def get_matrix_position(self, mat_idx):
    
        mat_idx_full_ = []
        for i in range(2):
            temp_list = []
            for elem in mat_idx[i]:
                temp_list.append([i, elem])
            mat_idx_full_.extend(temp_list)
        return mat_idx_full_
        
    def _vocab_to_idx(self , chunk_data):
        
        voc_to_idx = []
        preprocessed_data = map(self._preprocess, chunk_data)
        
        for chunks in preprocessed_data:
            if chunks:
                voc_to_temp = [self.vocab[w] for w in chunks if w in self.vocab]
                voc_to_idx.append(voc_to_temp)
        voc_to_idx = np.array(voc_to_idx)
        return voc_to_idx
                

                
        


if __name__ == "__main__":

    import cPickle
    from sklearn.datasets import fetch_20newsgroups
    twenty_train = fetch_20newsgroups(subset='train')   
    data_ = twenty_train.data
    print("Download 20 news group data completed")
    A = TextLoader(data_ , min_count = 27)
    prin(len(A.vocab))
    batch_size = 100
    batch_data = A.get_batch(batch_size)

    for batch_ in batch_data:
        collected_data = [chunks for chunks in batch_]
        bow , dow , negative_mask  = A._bag_of_words(collected_data)

        print(bow.shape , dow.shape , negative_mask.shape)
        print(bow)
        print(dow)
        print(negative_mask)

        print(bow.max() , dow.max() , negative_mask.max())
        print("Successful")
        break