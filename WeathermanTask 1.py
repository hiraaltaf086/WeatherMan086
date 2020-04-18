import os
import itertools
from prettytable import PrettyTable


# return unique for provided index/key
def unique_func(key, data_list):
    unique_list = list(set([val['' + key + ''].split('-')[0] for val in data_list]))
    unique_list.sort(key=lambda x: int(x))
    return unique_list


# return sorted unique key data according to year
def sort_func(key, year, data_list):
    unique_list = list(set(val['' + key + ''] for val in data_list if val['PKT'].split('-')[0] == year))
    if "" in unique_list:
        unique_list.remove("")
    sort_res = sorted(unique_list, key=lambda x: int(x), reverse=True)
    return sort_res


# return hottest days
def hottest_fun(temp, data_list, year):
    mylist = []
    for val in data_list:
        if val['Max TemperatureC'] == temp[0]:
            if year in val['PKT'].split('-')[0]:
                mylist.append(val['PKT'])
    sort_res = sorted(mylist, reverse=True)
    return sort_res


def repo1_display(unique_years, max_temps, min_temps, max_humid, min_humid):
    print("\nReport 1: Displaying annual Min / Max temperatures")
    x = PrettyTable()
    x.field_names = ["Year", "Max Temp", "Min Temp", "Max Humidity", 'Min Humidity']
    for (y, a, b, c, d) in zip(unique_years, max_temps, min_temps, max_humid, min_humid):
        x.add_row([y, ', '.join(a), b, ', '.join(c), d])
    print(x)


def repo2_display(unique_years, max_temps, hottest_days):
    x = PrettyTable()
    print("\nReport 2: Displaying Hottest days of each year")
    x.field_names = ["Year","Days", "Max Temp" ]
    x.align["Days"] = "l"
    for (y, a, b) in zip(unique_years, hottest_days,max_temps ):
        x.add_row([y,  ', '.join(a),b[0]])
    print(x)


# covert all directory files into dictionary
def datadic_fuc(data_dir):
    data_dic = []
    for root, dirs, files in os.walk(data_dir):
        for file in files:
            if file.endswith('.txt'):
                with open(os.path.join(root, file), 'r') as f:
                    header = f.readlines()[1]
                    head_list = [val.strip() for val in header.split(',')]  # keys for dictionary
                    f.seek(0)
                    data = f.readlines()[2:-1]  # values for dictionary
                    for line in data:
                        data_dic.append(
                            dict(zip(head_list, (x.strip() for x in line.split(',')))))  # dictionary from key-val pair

    for val in data_dic:
        if 'PKST' in val.keys():  # change key 'PKST' to 'PKT'
            val['PKT'] = val.pop('PKST')
    return data_dic


# return reports according to user choice
def weatherman(choice, data_dic):
    max_temps = []
    min_temps = []
    max_humid = []
    min_humid = []
    hottest_days = []
    unique_years = unique_func('PKT', data_dic)

    if choice == '1':
        # calculating temp annually:
        for year in unique_years:
            max_temps.append(sort_func('Max TemperatureC', year, data_dic)[:1])  # seleting top val for each year
            min_temps.append(sort_func('Min TemperatureC', year, data_dic)[-1])  # seleting min val for each year
            max_humid.append(sort_func('Max Humidity', year, data_dic)[:1])
            min_humid.append(sort_func('Min Humidity', year, data_dic)[-1])

        # printing report 1
        repo1_display(unique_years, max_temps, min_temps, max_humid, min_humid)

    else:
        # getting max temps
        for year in unique_years:
            max_temps.append(sort_func('Max TemperatureC', year, data_dic)[:1])
        temp_count = 0

        # finding all hottest days annually
        for year in unique_years:
            hottest_days.append(hottest_fun(max_temps[temp_count], data_dic, year))
            temp_count = temp_count + 1

        # printing report 2
        repo2_display(unique_years, max_temps, hottest_days)


# main function for user choice and validation
def main():
    while True:
        try:
            print("""\n***Weather Man***\nREPORTS Available:
                    1: for annual Min/Max temperatures
                    2: for Hottest days of each year  """)
            choice, my_dir = input(" \nPlease enter your choice as [Report#] [directory]  :  ").split()
            if os.path.isdir(my_dir):
                if (choice == '1') or (choice == '2'):
                    data_dic = datadic_fuc(my_dir)
                    weatherman(choice, data_dic)
                else:
                    print("Please Enter Valid Report No. ")
            else:
                print(
                    "Dir NOT FOUND : Please check if your Directory is in same folder as file ")
                continue
        except ValueError:
            print("Usage: [Report#] [directory]")


main()
