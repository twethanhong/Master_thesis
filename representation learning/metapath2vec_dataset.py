import numpy as np
import random
import os

class Dataset(object):
    def __init__(self,random_walk_txt,node_type_mapping_txt,node_type_mapping_txt_1,node_type,node_type_1,window_size):
        index2token,token2index,word_and_counts,index2frequency,node_context_pairs= self.parse_random_walk_txt(random_walk_txt,window_size)
        self.window_size = window_size
        self.nodeid2index =  token2index
        self.index2nodeid = index2token
        self.index2frequency = index2frequency
        index2type,type2indices = self.parse_node_type_mapping_txt(node_type_mapping_txt,node_type_mapping_txt_1,node_type,node_type_1, self.nodeid2index)
        self.index2type = index2type
        self.type2indices = type2indices
        self.node_context_pairs= node_context_pairs
        self.prepare_sampling_dist(index2frequency,index2type,type2indices)
        self.shffule()
        self.count = 0
        self.epoch = 1

    def parse_node_type_mapping_txt(self,node_type_mapping_txt,node_type_mapping_txt_1,node_type,node_type_1,nodeid2index):
        #this method does not modify any class variables
        index2type={}
        
        with open(node_type_mapping_txt) as f:
            for line in f:
                pair = [entry for entry in line.strip().split(' ')]
                if len(pair[0])==0 or len(pair[1])==0:
                    print("something is wrong!!!")
                    print(pair)
                    continue
                if pair[0] in nodeid2index:
                    index2type[nodeid2index[pair[0]]]=node_type
        with open(node_type_mapping_txt_1) as f:
            for line in f:
                pair = [entry for entry in line.strip().split(' ')]
                if len(pair[0])==0 or len(pair[1])==0:
                    print("something is wrong!!!")
                    print(pair)
                    continue
                if pair[0] in nodeid2index:
                    index2type[nodeid2index[pair[0]]]=node_type_1

        type2indices = {}
        all_types = set(index2type.values())
        for node_type in all_types:
            type2indices[node_type]=[]

        for node_index,node_type in index2type.items():
            type2indices[node_type].append(node_index)

        #make array because it will be used with numpy later
        for node_type in all_types:
            type2indices[node_type]=np.array(type2indices[node_type])

        return index2type,type2indices

    def parse_random_walk_txt(self,random_walk_txt,window_size):
        #this method does not modify any class variables
        #this will NOT make any <UKN> so don't use for NLP.
        word_and_counts = {}
        with open(random_walk_txt) as f:
            for line in f:
                sent = [word.strip() for word in line.strip().split(' ')]
                for word in sent:       
                    if len(word) == 0:
                        continue
                    if word in word_and_counts:
                        word_and_counts[word] += 1
                    else:
                        word_and_counts[word] = 1


        print("The number of unique words:%d"%len(word_and_counts))
        index2token = dict((i, word) for i, word in enumerate(word_and_counts.keys()) )
        token2index = dict((v, k) for k, v in index2token.items())
        index2frequency = dict((token2index[word],freq) for word,freq in word_and_counts.items() )

        #word_word=scipy.sparse.lil_matrix((len(token2index), len(token2index)), dtype=np.int32)
        node_context_pairs = []#let's use naive way now

        print("window size %d"%window_size)

        with open(random_walk_txt) as f:
            for line in f:
                sent = [token2index[word.strip()] for word in line.split(' ') if word.strip() in token2index]#轉換成index
                sent_length=len(sent)#總長度
                for target_word_position,target_word_idx in enumerate(sent):#(第幾個字,index)
                    start=max(0,target_word_position-window_size)
                    end=min(sent_length,target_word_position+window_size+1)
                    context=sent[start:target_word_position]+sent[target_word_position+1:end+1]
                    for contex_word_idx in context:
                        node_context_pairs.append((target_word_idx,contex_word_idx))
                        #word_word[target_word_idx,contex_word_idx]+=1

        #word_word=word_word.tocsr()
        return index2token,token2index,word_and_counts,index2frequency,node_context_pairs

    def get_one_batch(self):
        if self.count == len(self.node_context_pairs):
            self.count=0
            self.epoch+=1
        node_context_pair = self.node_context_pairs[self.count]
        self.count+=1
        return node_context_pair

    def get_batch(self,batch_size):
        pairs = np.array([self.get_one_batch() for i in range(batch_size)])
        return pairs[:,0],pairs[:,1]

    def shffule(self):
        random.shuffle(self.node_context_pairs)

    def get_negative_samples(self,pos_index,num_negatives,care_type):
        # if care_type is True it's a heterogeneous negative sampling
        #same output format as https://www.tensorflow.org/api_docs/python/tf/nn/log_uniform_candidate_sampler
        pos_prob = self.sampling_prob[pos_index] 
        if not care_type:
            negative_samples = np.random.choice(len(self.index2nodeid),size=num_negatives,replace=False,p=self.sampling_prob)
            negative_probs = self.sampling_prob[negative_samples]
        else:
            node_type = self.index2type[pos_index]
            sampling_probs = self.type2probs[node_type]
            sampling_candidates = self.type2indices[node_type]
            negative_samples_indices = np.random.choice(len(sampling_candidates),size=num_negatives,replace=False,p=sampling_probs)
            
            negative_samples = sampling_candidates[negative_samples_indices]
            negative_probs = sampling_probs[negative_samples_indices]

        # print(negative_samples,pos_prob,negative_probs)
        return negative_samples,pos_prob.reshape((-1,1)),negative_probs

    def prepare_sampling_dist(self,index2frequency,index2type,type2indices):
        sampling_prob = np.zeros(len(index2frequency))
        for i in range(len(index2frequency)):
            sampling_prob[i]=index2frequency[i]
        sampling_prob = sampling_prob**(3.0/4.0)

        all_types = set(index2type.values())
        type2probs = {}
        for node_type in all_types:
            indicies_for_a_type = type2indices[node_type]
            type2probs[node_type] = np.array(sampling_prob[indicies_for_a_type])
            type2probs[node_type] = type2probs[node_type]/np.sum(type2probs[node_type])


        #if not careing type
        sampling_prob = sampling_prob/np.sum(sampling_prob)

        self.sampling_prob = sampling_prob
        self.type2probs = type2probs

if __name__ == '__main__':
    '''
    #test code  
    dataset=Dataset(random_walk_txt="C://Users//KDD204//Desktop//異構網路嵌入式學習//異構資料//win1//win1_cpl.txt",
                    node_type_mapping_txt="C://Users//KDD204//Desktop//異構網路嵌入式學習//異構資料//id_labevent.txt",
                    node_type_mapping_txt_1="C://Users//KDD204//Desktop//異構網路嵌入式學習//異構資料//id_chartevent.txt",
                    node_type="labevent",
                    node_type_1="chartevent",
                    window_size=1)
    print(dataset.get_batch(2))
    center,context = dataset.get_one_batch()
    print(dataset.sampling_prob)
    print(dataset.get_negative_samples(context,num_negatives=5,care_type=False))
    print(dataset.get_negative_samples(context,num_negatives=2,care_type=True))
    '''