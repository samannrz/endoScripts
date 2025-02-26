import pickle
from scipy.stats import brunnermunzel, mannwhitneyu


N_BATCH_COMBINE = 4
# batches = [3,4,5,6,7,8,9,10,11]
batches = [21,22,23,24,25,26,27,28,29,210]
dict = {'nicolas':2, 'jean':11, 'giuseppe':5, 'filippo':8, 'ervin':14, 'ebbe':17}
annotator = 'giuseppe'

annotator_treat_final = []
annotator_check_final = []
for i in range(0,len(batches),N_BATCH_COMBINE):
    b= batches[i]
    j=0
    annotator_treat = []
    annotator_check = []
    for j in range(N_BATCH_COMBINE):
        if b==30:
            b=210
        if b+j == 30:
            b=209
        if b+j == 12 or (b+j)>210:
            break
        with open('pkl_files/c_batch'+str(b+j)+'.pkl', 'rb') as file:
            data = pickle.load(file)
            # print(b+j)
            # print(data.iloc[:,14])
            # break
            #print(data.iloc[:, dict[annotator]+0])
            annotator_treat.extend(data.iloc[:, dict[annotator]].tolist())
            annotator_check.extend(data.iloc[:, dict[annotator]+1].tolist())
    annotator_treat_final.append(annotator_treat)
    annotator_check_final.append(annotator_check)
print((annotator_treat_final[0]))
######################################################
def remove_zeros(input_list):
    #return [item for item in input_list if item != 0]
    #return [item for item in input_list if item != 0 and item != 100]
    return input_list

####### TESTS #############################################

print('Treat:')
statistic, p_value = mannwhitneyu(remove_zeros(annotator_treat_final)[0],remove_zeros(annotator_treat_final)[1], alternative= 'less' )
print(f"P-value: {p_value}")
statistic, p_value = mannwhitneyu(remove_zeros(annotator_treat_final)[1],remove_zeros(annotator_treat_final)[2], alternative='less')
print(f"P-value: {p_value}")
statistic, p_value = mannwhitneyu(remove_zeros(annotator_treat_final)[0],remove_zeros(annotator_treat_final)[2], alternative='less')
print(f"P-value: {p_value}")
# statistic, p_value = mannwhitneyu(remove_zeros(annotator_treat_final)[0],remove_zeros(annotator_treat_final)[4], alternative='less')
# print(f"P-value: {p_value}")
# statistic, p_value = mannwhitneyu(remove_zeros(annotator_treat_final)[0],remove_zeros(annotator_treat_final)[3], alternative='less')
# print(f"P-value: {p_value}")

print('check:')
statistic, p_value = mannwhitneyu(remove_zeros(annotator_check_final)[0],remove_zeros(annotator_check_final)[1], alternative= 'less' )
print(f"P-value: {p_value}")
statistic, p_value = mannwhitneyu(remove_zeros(annotator_check_final)[1],remove_zeros(annotator_check_final)[2], alternative='less')
print(f"P-value: {p_value}")
statistic, p_value = mannwhitneyu(remove_zeros(annotator_check_final)[0],remove_zeros(annotator_check_final)[2], alternative='less')
print(f"P-value: {p_value}")
# statistic, p_value = mannwhitneyu(remove_zeros(annotator_check_final)[0],remove_zeros(annotator_check_final)[3], alternative='less')
# print(f"P-value: {p_value}")
# statistic, p_value = mannwhitneyu(remove_zeros(annotator_check_final)[0],remove_zeros(annotator_check_final)[3], alternative='less')
# print(f"P-value: {p_value}")

