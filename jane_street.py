from random import randint
from random import sample
from random import shuffle
import numpy as np
import pprint
import concurrent.futures
import ast
from contextlib import redirect_stdout
import itertools

# storage=[]
# result = []
# perfect = []
# on = True
# # for i in range(len(square_1)):
# #     for j in range(len(square_1[i])):
# #         square_1[i][j] = randint(1,100)
# while on:
#     square_1 = np.array(sample(range(1,100),9))
#     square_1 = square_1.reshape((3,3))
#     storage.append(square_1[0][0]+square_1[0][1]+square_1[0][2])
#     storage.append(square_1[1][0]+square_1[1][1]+square_1[1][2])
#     storage.append(square_1[2][0]+square_1[2][1]+square_1[2][2])
#     storage.append(square_1[0][0]+square_1[1][0]+square_1[2][0])
#     storage.append(square_1[0][1]+square_1[1][1]+square_1[2][1])
#     storage.append(square_1[0][2]+square_1[1][2]+square_1[2][2])
#     storage.append(square_1[0][0]+square_1[1][1]+square_1[2][2])
#     storage.append(square_1[0][2]+square_1[1][1]+square_1[2][0])
#     if len(set(storage))==2:
#         result.append(square_1)
#         print(result)
#         on = False
#     if len(set(storage))==1:
#         perfect.append(square_1)
#         print(perfect)
#         on = False


def makeList():
    s=[i for i in range(1,150)]
    res = {}
    for i in range(15,150):
        temp =[]
        for index,j in enumerate(s):
            l,r = index+1, len(s)-1
            diff = i-j
            if diff < 0:
                break
            while l<r:
                if s[l]+s[r] > diff:
                    r-=1
                elif s[l]+s[r]< diff:
                    l+=1
                else:
                    temp.append([j,s[l],s[r]])
                    r-=1
        res[i]= temp    
    with open("output.txt", "w") as external_file:
        pprint.pprint(res, stream= external_file)
        external_file.close()



def perfect ():
    with open('output.txt','r') as f:
        permu_list = ast.literal_eval(f.read())
    s = permu_list[50]
    result = []
    perfect = []
    on = True
    target = 50
    while on:
        flag = False
        p = sample(range(len(s)),3)
        shuffle(s[p[0]])
        shuffle(s[p[1]])
        x = [target-s[p[0]][0]-s[p[1]][0],target-s[p[0]][1]-s[p[1]][1],target-s[p[0]][2]-s[p[1]][2]]
        for i in x:
            if i < 0:
                flag = True
        if flag == True:
            continue
        square_1 = np.array([s[p[0]],s[p[1]],x])  
        storage =[]
        storage.append(square_1[0][0]+square_1[1][0]+square_1[2][0])
        storage.append(square_1[0][1]+square_1[1][1]+square_1[2][1])
        storage.append(square_1[0][2]+square_1[1][2]+square_1[2][2])
        storage.append(square_1[0][0]+square_1[1][1]+square_1[2][2])
        storage.append(square_1[0][2]+square_1[1][1]+square_1[2][0])
        if len(set(storage))==1:
            perfect.append(square_1)



def nearlyPerfect ():
    with open('output.txt','r') as f:
        permu_list = ast.literal_eval(f.read())
    s = permu_list[117]
    perfect = []
    on = True
    target = 117
    while on:
        flag = False
        p = sample(range(len(s)),3)
        shuffle(s[p[0]])
        shuffle(s[p[1]])
        x = [target-s[p[0]][0]-s[p[1]][0],target-s[p[0]][1]-s[p[1]][1],target-s[p[0]][2]-s[p[1]][2]]
        for i in x:
            if i < 0:
                flag = True
        if flag == True:
            continue

        square_1 = np.array([s[p[0]],s[p[1]],x])  
        
        storage =[]
        storage.append(square_1[2][0]+square_1[2][1]+square_1[2][2])
        storage.append(square_1[0][0]+square_1[1][0]+square_1[2][0])
        storage.append(square_1[0][1]+square_1[1][1]+square_1[2][1])
        storage.append(square_1[0][2]+square_1[1][2]+square_1[2][2])
        storage.append(square_1[0][0]+square_1[1][1]+square_1[2][2])
        storage.append(square_1[0][2]+square_1[1][1]+square_1[2][0])

        if len(set(storage))==1: #or (len(set(storage))==2 and abs(list(set(storage))[0]-list(set(storage))[1]) == 1):
            perfect.append(square_1)
            
        else:
            continue



        #start of second square
        linear=square_1.flatten()
        if len(set(linear)) != len(linear):
            continue
        if 0 in linear:
            continue
        
        # match_specific = left_top of the number
        square_2_ref_1 = int(square_1[2][0])
        square_2_ref_2 = int(square_1[2][1])
        match = 0
        
        flag_3 = True
        for i in range(16,len(permu_list)):
            for j in permu_list[i]: 
                if square_2_ref_1 in j:
                    if square_2_ref_2 in j:
                        match = j
                        match_specific = match.copy()
                        match_specific.remove(square_2_ref_1)
                        match_specific.remove(square_2_ref_2)
                        if match_specific not in linear and (match_specific[0]>int(square_1[2][0]) or match_specific[0]>int(square_1[2][1])):
                            flag_3 = False
                            square_2_target = i
                            break
            if flag_3 == False:
                break
        if flag_3 == True:
            continue
        square_2_s = permu_list[square_2_target]
        flag_2 = False
        #add first row to linear
        linear = np.append(linear,match_specific[0])
        #check for duplicate in the second row
        x = 0
        for z in permu_list[square_2_target]:
            if len(linear.tolist()+z) ==  len(set(linear.tolist()+z)):
                square_2_secondrow = z
                for m in list(itertools.permutations(square_2_secondrow)):
                    if len(m) != 3:
                        continue
                    square_2_x = [square_2_target-match_specific[0]-m[0],square_2_target-int(square_1[2][0])-m[1],square_2_target-int(square_1[2][1])-m[2]]
                    #check for duplicates and negative
                    # with open('out_2.txt', 'a') as f:
                    #     with redirect_stdout(f):
                    #         print(square_2_target,square_2_secondrow,linear,square_2_x)
                    flag = False
                    for i in square_2_x:
                        if i <= 0:
                            flag = True
                            break
                        if i in linear:
                            flag = True
                            break
                    if flag == False:

                        square_2 = np.array([[match_specific[0],square_1[2][0],square_1[2][1]],m,square_2_x])
                        #print(square_2_target,square_1,square_2)
                        #starts to filter for right last row
                        sqaure_2_storage =[]
                        sqaure_2_storage.append(square_2[2][0]+square_2[2][1]+square_2[2][2])
                        sqaure_2_storage.append(square_2[0][0]+square_2[1][0]+square_2[2][0])
                        sqaure_2_storage.append(square_2[0][1]+square_2[1][1]+square_2[2][1])
                        sqaure_2_storage.append(square_2[0][2]+square_2[1][2]+square_2[2][2])
                        sqaure_2_storage.append(square_2[0][0]+square_2[1][1]+square_2[2][2])
                        sqaure_2_storage.append(square_2[0][2]+square_2[1][1]+square_2[2][0])
                        
                        if len(set(sqaure_2_storage))==1 or (len(set(sqaure_2_storage))==2 and abs(list(set(sqaure_2_storage))[0]-list(set(sqaure_2_storage))[1]) == 1):
                            perfect.append(square_2)
                        else:
                            continue
                        linear = np.append(linear,m)
                        linear = np.append(linear,square_2_x)
                        linear = linear.flatten()
                        if len(set(linear)) != len(linear):
                            continue
                        if 0 in linear:
                            continue
                        #finish on second square
                        square_3_ref_1 = int(square_2[1][2])
                        square_3_ref_2 = int(square_2[2][2])


                        #find top left for square_3
                        flag_4 = True
                        for i in range(16,len(permu_list)):
                            for j in permu_list[i]: 
                                if square_3_ref_1 in j:
                                    if square_3_ref_2 in j:
                                        match = j
                                        match_specific = match.copy()
                                        match_specific.remove(square_3_ref_1)
                                        match_specific.remove(square_3_ref_2)
                                        if len(match_specific) != 1: 
                                            continue
                                        if match_specific not in linear and (match_specific[0]>square_3_ref_1 or match_specific[0]>square_3_ref_2):
                                            flag_4 = False
                                            square_3_target = i
                                            break
                            if flag_4 == False:
                                break
                        linear = np.append(linear,match_specific[0])
                        for z in permu_list[square_3_target]:
                            if len(linear.tolist()+z) ==  len(set(linear.tolist()+z)):
                                square_3_secondrow = z
                                for j in list(itertools.permutations(square_3_secondrow)):
                                    if len(j) != 3:
                                        continue
                                    square_3_x = [square_3_target-match_specific[0]-j[0],square_3_target-square_3_ref_2-j[1],square_3_target-square_3_ref_1-j[2]]
                                    #check for duplicates and negative
                                    # with open('out_2.txt', 'a') as f:
                                    #     with redirect_stdout(f):
                                    #         print(square_2_target,square_2_secondrow,linear,square_2_x)
                                    flag = False
                                    for i in square_3_x:
                                        if i <= 0:
                                            flag = True
                                            break
                                        if i in linear:
                                            flag = True
                                            break
                                    if flag == False:

                                        square_3 = np.array([[match_specific[0],square_2[2][2],square_2[1][2]],j,square_3_x])

                                        #print(square_2_target,square_1,square_2)
                                        #starts to filter for right last row
                                        sqaure_3_storage =[]
                                        sqaure_3_storage.append(square_3[2][0]+square_3[2][1]+square_3[2][2])
                                        sqaure_3_storage.append(square_3[0][0]+square_3[1][0]+square_3[2][0])
                                        sqaure_3_storage.append(square_3[0][1]+square_3[1][1]+square_3[2][1])
                                        sqaure_3_storage.append(square_3[0][2]+square_3[1][2]+square_3[2][2])
                                        sqaure_3_storage.append(square_3[0][0]+square_3[1][1]+square_3[2][2])
                                        sqaure_3_storage.append(square_3[0][2]+square_3[1][1]+square_3[2][0])

                                        if len(set(sqaure_3_storage))==1: #or (len(set(sqaure_3_storage))==2 and abs(list(set(sqaure_3_storage))[0]-list(set(sqaure_3_storage))[1]) == 1):
                                            perfect.append(square_3)
                                            
                                        else:
                                            continue
                                        linear = np.append(linear,j)
                                        linear = np.append(linear,square_3_x)
                                        linear = linear.flatten()
                                        if len(set(linear)) != len(linear):
                                            continue
                                        if 0 in linear:
                                            continue
                                        # print(sum(linear))
                                        # print(square_1,"\n", square_2, "\n", square_3)
                                        #end of the thrid square
                                        # square_4_target = int(square_1[1][2])+int(square_1[2][2])+int(square_3[1][2])
                                        
                                        # for k in permu_list[square_4_target]:
                                        #     if int(square_3[2][2]) in k:
                                        #         #+1 is to compensate for square_3[2][2] which was already appearing in linear
                                        #         if len(linear.tolist()+k) ==  len(set(linear.tolist()+k))+1:

                                        #             square_4_secondrow = k
                                        #             square_4_secondrow_without = square_4_secondrow.copy()
                                        #             square_4_secondrow.remove(int(square_3[2][2]))
                                        #             for l in list(itertools.permutations(square_4_secondrow_without)):
                                        #                 square_4_x = [square_4_target-int(square_3[1][2])-int(square_3[2][2]),square_4_target-int(square_1[1][2])-l[0],square_4_target-int(square_1[2][2])-l[1]] 
                                        #                 flag = False
                                        #                 for i in square_4_x:
                                        #                     if i <= 0:
                                        #                         flag = True
                                        #                         break
                                        #                     if i in linear:
                                        #                         flag = True
                                        #                         break
                                        #                 if flag == False:
                                        #                     square_4 = np.array([[square_3[1][2],square_1[2][2],square_1[1][2]],[square_3[2][2],l[0],l[1]],square_4_x])

                                        #                     #starts to filter for right last row
                                        #                     sqaure_4_storage =[]
                                        #                     sqaure_4_storage.append(square_4[2][0]+square_4[2][1]+square_4[2][2])
                                        #                     sqaure_4_storage.append(square_4[0][0]+square_4[1][0]+square_4[2][0])
                                        #                     sqaure_4_storage.append(square_4[0][1]+square_4[1][1]+square_4[2][1])
                                        #                     sqaure_4_storage.append(square_4[0][2]+square_4[1][2]+square_4[2][2])
                                        #                     sqaure_4_storage.append(square_4[0][0]+square_4[1][1]+square_4[2][2])
                                        #                     sqaure_4_storage.append(square_4[0][2]+square_4[1][1]+square_4[2][0])

                                        #                     if len(set(sqaure_4_storage))==1 or (len(set(sqaure_4_storage))==2 and abs(list(set(sqaure_4_storage))[0]-list(set(sqaure_4_storage))[1]) == 1):
                                        #                         perfect.append(square_4)
                                                                
                                        #                     else:
                                        #                         continue
                                        #                     linear = np.append(linear,square_4_secondrow_without)
                                        #                     linear = np.append(linear,square_4_x)
                                        #                     linear = linear.flatten()
                                                            
                                        #                     if len(set(linear)) != len(linear):
                                        #                         continue
                                        #                     if 0 in linear:
                                        #                         continue
                                        square_4_target = int(square_1[1][2])+int(square_1[2][2])+int(square_3[1][2])
                                        square_4  = [[square_3[1][2],square_1[2][2],square_1[1][2]],[square_3[2][2]],[square_4_target-int(square_3[1][2])-square_3[2][2]]]
                                        square_4[1].append(square_4_target-int(square_1[1][2])-square_4[2][0])
                                        linear = np.append(linear, square_4[1][1])
                                        linear = np.append(linear, square_4[2][0])
                                        print(square_4)
                                        if len(set(linear.tolist())) == len(linear.tolist()):

                                            print("1 \n", square_1, "2 \n", square_2, "3 \n", square_3, "4 \n", square_4)
                                            on = False
                                        else:
                                            continue
                                        #print("1 \n", square_1, "2 \n", square_2, "3 \n", square_3, "4 \n", square_4)










def main():
    with concurrent.futures.ProcessPoolExecutor() as executor:
        results = [executor.submit(nearlyPerfect) for _ in range(8)]
        for f in concurrent.futures.as_completed(results):
            print(f.result())
if __name__ == '__main__':
    main()
