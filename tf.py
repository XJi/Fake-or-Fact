import math
def convert_matrix(raw_matrix):
    tf = list()
    print(len(raw_matrix))
    title_amount = len(raw_matrix)
    #denominator for IDF
    '''# Compute IDF
    total_hd_for_each_word = list()
    for i in range(0,10000):
            total_hd_for_each_word.append(0)
    for row in raw_matrix:
        for i in range(0,10000):
            if i in row:
                total_hd_for_each_word[i] = total_hd_for_each_word[i]+1
    #print(total_hd_for_each_word) 
    idf = list()
    for i in range(0,10000):
        idf.append(math.log10(title_amount/(total_hd_for_each_word[i]+1)))'''
       
    title_contain_word = list()
    
    for i in range(0,len(raw_matrix)):
        title_contain_word.append(0)
    
    for row in raw_matrix:
        tf_single = list()
        for i in range(0,10000):
            tf_single.append(0)
        #print(len(row)) #number of words in one title
        for word in row:
            # number of times each word shows up in a headline
            tf_single[word] = tf_single[word]+1 
        for col in row:
            if len(row) != 0:
                tf_single[col] = tf_single[col]/len(row)
        tf.append(tf_single)
   '''#Compute TF*IDF
   single_result = list()
    result = list()
    for index, i in enumerate(tf):
        for j in i:
            single_result.append(j*idf[index])
            print(j*idf[index])
    result.append(single_result)
    print(len(result))
    return result''' 
    
    return tf
            
