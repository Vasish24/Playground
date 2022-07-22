import json

""" Assuming that json.data is the file with all the necessary information. 
Here is where we can open & read the json file """
def read_data():
    row_list = []
    with open('json_data.json') as json_file:
        data = json.load(json_file)
    for row in data:
        row_list.append(row)
    return row_list

"""Objects are created in this class """
class BMI:
    category = {
        'UnderWeight': 'UW',
        'Normal Weight': 'NW',
        'Over Weight': 'OW',
        'Moderately Obese': 'MO',
        'Severly Obese': 'SO',
        'Very Severly Obese': 'VSO',

    }
    Risk = {
        'Malnutrition Risk': 'MNR',
        'Low Risk': 'LR',
        'Enhanced Risk': 'ER',
        'Medium Risk': 'MR',
        'High Risk': 'HR',
        'Very High Risk': 'VHR',

    }

""" In this bmi calculator function, bmi is calculated by using the data (i.e) weight & height. 
And each bmi range is defined according to the bmi category and health risk """
def BMI_calculator(info):
    BMI_category = None
    Health_Risk = None
    BMI_Range = None
    height = float(info[1])
    weight = float(info[2])
    BMI = weight / ((height/100)**2)
    if BMI <= 18.4:
        BMI_Range = BMI
        BMI_category = BMI.category.get('UW')
        Health_Risk = BMI.Risk.get('MNR')
    elif BMI >= 18.5 and BMI <= 24.9:
        BMI_Range = BMI
        BMI_category = BMI.category.get('NW')
        Health_Risk = BMI.Risk.get('LR')
    elif BMI >=25 and BMI <= 29.9:
        BMI_Range = BMI
        BMI_category = BMI.category.get('OW')
        Health_Risk = BMI.Risk.get('ER')
    elif BMI >=30 and BMI <= 34.9:
        BMI_Range = BMI
        BMI_category = BMI.category.get('MO')
        Health_Risk = BMI.Risk.get('MR')
    elif BMI >= 35 and BMI <= 39.9:
        BMI_Range = BMI
        BMI_category = BMI.category.get('SO')
        Health_Risk = BMI.Risk.get('HR')
    elif BMI > 40:
        BMI_Range = BMI
        BMI_category = BMI.category.get('VSO')
        Health_Risk = BMI.Risk.get('VHR')
    bmi_list = [BMI_Range,BMI_category,Health_Risk]
    return bmi_list

""" In this bmi details function, bmi informations in each rows are satisfied with bmi calculator 
and then it will categories the person. If the information is wrong then it will show wrong details  """
def bmi_details(details):
    line_number = 0
    correct_info = []
    wrong_info = []
    for row in details:
        if line_number == 0:
            line_number = 1
        elif row[0].isalpha() == True and row[1].isnumeric() == True and row[2].isnumeric() == True:
            bmi = BMI_calculator(row)
            correct_info.append(row + bmi)
            line_number = line_number + 1
        else:
            wrong_info.append(row)
            line_number = line_number + 1
    return correct_info

if __name__ == '__main__':
    contents = read_data()
    result = bmi_details(contents)
    print(result)
