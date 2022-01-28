'''
Created on 25 Jan 2022

@author: daidan
'''

import math
import os
import pandas as pd


# Directory to load input.csv
# Root directory of the project
ROOT_DIR = os.getcwd()

Data_DIR = os.path.join(ROOT_DIR, "data")

'''
csvReadPath is the path of input.csv

key_form_header() select form headers that linked from the input excel, used to merge rows together

'''

def key_form_header(csvReadPath):
    inputContent=pd.read_excel(csvReadPath,sheet_name='input')
    form_header=inputContent.columns
    
    for i in range(0, len(form_header)):
        marks=False
        
        eachColumnValues=list(inputContent[form_header[i]].values)
        
        # remove the '-'
        k = 0 
        for r in range(len(eachColumnValues)):
            if eachColumnValues[k] == '-':
                eachColumnValues.pop(k)
                
            else:
                k += 1
        
        if len(eachColumnValues) != len(set(eachColumnValues)):
            continue;
        
        for j in range(i+1, len(form_header)):
            marks=False
            
            restColumnValues=list(inputContent[form_header[j]].values)
            k = 0 
            for r in range(len(restColumnValues)):
                if restColumnValues[k] == '-':
                    restColumnValues.pop(k)
                else:
                    k += 1
        
            if len(restColumnValues) != len(set(restColumnValues)):
                continue;
            
            marks=[True for value in eachColumnValues if value in restColumnValues]
            
            if marks:
                print('the link maybe {} and {}'.format(form_header[i],form_header[j]))
                


'''
csvReadPath is the path of input.csv

csv_Dic() is obtain the each row dic{key:value} based on the form header
'''

def csv_Dic(csvReadPath):
    
    inputContent=pd.read_excel(csvReadPath)
    
    wholeIndex=list(range(len(inputContent)))

    impactAssessmentDicList=[]
    cycleDicList=[]
    siteDicList=[]
    comDicList=[]
    
    form_header=inputContent.columns
    
    comValues=inputContent.loc[0]
    
    comDic={}
    for i in range(0,len(comValues)):
        comDic[form_header[i]] = comValues[i]
    comDicList.append(comDic)
    
    for eachRowIndex in wholeIndex:
        
        impactAssessmentDic={}
        cycleDic={}
        siteDic={}
        comDic={}
        
        eachRowValues=inputContent.loc[eachRowIndex]
        
        cycleSiteIdRow=eachRowValues['cycle.site.@id']
        siteIdRow=eachRowValues['site.@id']
        
        cycleIdRow=eachRowValues['cycle.@id']
        impactAssessmentCycleIdRow=eachRowValues['impactAssessment.cycle.@id']
        
        if '-' not in impactAssessmentCycleIdRow or ('-' in impactAssessmentCycleIdRow and len(impactAssessmentCycleIdRow) > 1):
            for i in range(0,len(eachRowValues)):
                impactAssessmentDic[form_header[i]] = eachRowValues[i]
            impactAssessmentDicList.append(impactAssessmentDic)
        
        if '-' not in cycleIdRow or ('-' in cycleIdRow and len(cycleIdRow) > 1):
            for c in range(0,len(eachRowValues)):
                cycleDic[form_header[c]] = eachRowValues[c]
            cycleDicList.append(cycleDic)   
                
        if '-' not in siteIdRow or ('-' in siteIdRow and len(siteIdRow) > 1):
            for s in range(0,len(eachRowValues)):
                siteDic[form_header[s]] = eachRowValues[s]
            siteDicList.append(siteDic)
            
    
    return impactAssessmentDicList, cycleDicList, siteDicList, comDicList
            
'''
take a CSV file and improve the format as described

Form the gen_output excel 
'''
def improveFormat(csvReadPath,csvSavePath):
    
    impactAssessmentDicList, cycleDicList, siteDicList, comDicList=csv_Dic(csvReadPath)
    
    wholeContext=[]
    
    for eachCycleDic in cycleDicList:
        
        cycleId=eachCycleDic['cycle.@id']
        
        for eachImpactAssessmentDic in impactAssessmentDicList:
            
            impactAssessment_cycleId=eachImpactAssessmentDic['impactAssessment.cycle.@id']
            
            if cycleId==impactAssessment_cycleId:
                
                for key, valules in eachImpactAssessmentDic.items():
                    
                    if '-' not in str(valules) or ('-' in str(valules) and len(str(valules)) > 1):
                        eachCycleDic[key]=valules
            
        
        cycle_siteId=eachCycleDic['cycle.site.@id']
        
        for eachsiteDic in siteDicList:
            siteId=eachsiteDic['site.@id']
            
            if cycle_siteId==siteId:
                for key, valules in eachsiteDic.items():
                    if '-' not in str(valules) or ('-' in str(valules) and len(str(valules)) > 1):
                        eachCycleDic[key]=valules
                    
        
        for comDic in comDicList:
            for key, valules in comDic.items():
                if '-' not in str(valules) or ('-' in str(valules) and len(str(valules)) > 1):
                        eachCycleDic[key]=valules   
        
        wholeContext.append(eachCycleDic)
    
    dict_all = {} 
    
    # put the values of same key into one list
    for eachCycleDic in wholeContext:
    #     dict_all.update(eachCycleDic)
        for k, v in eachCycleDic.items():
            dict_all.setdefault(k, []).append(v)
    
    # save all values into generate_excel output
    writer=pd.ExcelWriter(csvSavePath)
    df=pd.DataFrame(dict_all)
    df.to_excel(writer, index=False)
    writer.save()



'''
evaluate whether the generated excel(gen_output) is the same as the given result (output)
'''
def evelMethod(groundTruePath, generatePath):
    
    groundTrueContent=pd.read_excel(groundTruePath)
    
    generateContent=pd.read_excel(generatePath)
    
    wholeIndex=list(range(len(groundTrueContent)))
    form_header=groundTrueContent.columns
    
    groundTrueDicList=[]
    generateDicList=[]
    
    for eachRowIndex in wholeIndex:
        
        # the value of each row
        eachRow_groundTrue=groundTrueContent.loc[eachRowIndex]
        groundTrueDicList.append(list(eachRow_groundTrue))
        
        eachRow_generate=generateContent.loc[eachRowIndex]
        generateDicList.append(list(eachRow_generate))
        
    marks=True
    for each_groundTrue in groundTrueDicList:
        
        groundId=each_groundTrue[0]
        
        for each_generate in generateDicList:
            generateId=each_generate[0]
            
            if str(groundId)==str(generateId):
                # the size must be same
                if len(each_groundTrue) == len(each_generate):
                    for i in range(0, len(each_groundTrue)):
                        # there are inconsistencies in the number of decimal points of floating-point numbers in different excel
                        if isinstance(each_groundTrue[i],float):
                            values1=each_groundTrue[i]
                            values2=each_generate[i]
                            math.isclose(values1, values2, rel_tol=1e-4)
                            continue;
                        if str(each_groundTrue[i])!=str(each_generate[i]):
                            marks=False
                            print('for ID {}, the values of {} are not same \t'
                            'the generate file is {}, but ground truth is {}'
                            .format(groundId, form_header[i], each_generate[i], each_groundTrue[i]))
                
                else: 
                    print('for ID {}, the size of each row not same'.format(groundId))
    
    if marks:
        print('The generate file is same with the ground truth!')
    
    
    

if __name__ == '__main__':
    
    csvReadPath=Data_DIR+'/input.xls'
    groundTruePath=Data_DIR+'/output.xls'
    print('input file:',csvReadPath)
    
    csvSavePath=Data_DIR+'/gen_output.xls'
    
    key_form_header(csvReadPath)
    improveFormat(csvReadPath,csvSavePath)
    evelMethod(groundTruePath, csvSavePath)
    
