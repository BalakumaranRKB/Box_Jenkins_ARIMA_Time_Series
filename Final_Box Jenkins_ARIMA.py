""" Time Series ARIMA
Calculations:
1.ACF
2.PACF
3.Normality
4.Seasonality
5.p and q values
6. AIC values
Author : Balakumaran Kannan(Team 6) Time Series - Box – Jenkins: ARIMA Modelling
"""


#importing values from excel and converting it to data frame
import pandas as pd
import matplotlib.pyplot as plt
from pylab import rcParams
from statsmodels.tsa.stattools import pacf
import math
from scipy.stats import pearsonr

from statistics_1 import Statistics

from linear_regression_1 import LinearRegression



file3 = ('C:/Users/Kumar/OneDrive/Desktop/CCE IISc/Assignment 8/Non-seasonal_Time_series.xlsx')
df = pd.read_excel(file3)
no_of_Users= df.Users
number_of_users = list(no_of_Users)

#making pairs
def pairs(list_main):
    d = dict() 
    string = 'Lag'
    for i in range(1,26):
        list_1 = list_main[i:len(list_main)]
        list_2 = list_main[0:len(list_main)-i]
        d[string + str(i)] = list_1,list_2
        #d[string + str(i)] = list_2
    return d

def plot_ACF_graph(list_to_plot):
    #import matplotlib.pyplot as plt
    #from pylab import rcParams
    rcParams['figure.figsize'] = 15, 10
    left =  list()
    j = 0
    for i in range(0,len(list_to_plot)):
        j = j + 1
        left.append(j)
    String = 'Lag'
    tick_label = list()
    for i in range(0,len(list_to_plot)):
        tick_label.append(String +str(i+1))
    plt.bar(left,list_to_plot,tick_label = tick_label, width = 0.1)
    plt.title('ACF bar chart')
    plt.xlabel('x - axis')
    plt.ylabel('y - axis')
    
    plt.show()

def PACF_values(data_list):
    n = int(input('Enter the number of lags you wish for the PACF :'))
    y = list()
    d = dict()
    stringo = 'PACF'
    for i in range(1,n+1):
        y.append(pacf(data_list, nlags=i)[i])
        d[stringo + str(i)] = pacf(data_list, nlags=i)[i]
    print(d)
    return y  


def ACF(user_values):
    acf_container = list()
    for i in user_values:
        acf_values = Statistics.covariance(user_values[i][0],user_values[i][1])[1]
        acf_container.append(acf_values)

    return acf_container

def plot_PACF_graph(list2_to_plot):
    rcParams['figure.figsize'] = 15, 10
    left =  list()
    j = 0
    for i in range(0,len(list2_to_plot)):
        j = j + 1
        left.append(j)
    String = 'Lag'
    tick_label = list()
    for i in range(0,len(left)):
        tick_label.append(String +str(i+1))
    try:
        plt.title('PACF bar chart')
        plt.xlabel('x - axis')
        plt.ylabel('y - axis')
        plt.bar(left,list2_to_plot,tick_label = tick_label, width = 0.5)
    except ValueError:
        pass
    
    plt.show()

#Final change
def normal_difference(listo):
    print('before normal differencing/n',listo)
    count = 0
    while (count<2):
        b = []
        for i in range(0,len(listo)-1):
            b.append(listo[i+1]-listo[i])
        print('proceeding after validation check')
        print('the normal_differenced_list is  and its length is :',b,len(b))

        print('The ACF & PACF calculations are as follows:')
        pair_list = pairs(b)
        acf_values = correls(pair_list)
        pacf_values = PACF_values(b)
        plot_PACF_graph(pacf_values)
        plot_ACF_graph(acf_values)
        
        y = p_or_q_value(acf_values,b)
        print('p value is ',y)
        
        x = p_or_q_value(acf_values,b)
        print('q value is',x)

        option = input('Do you wish to conduct normal differencing again:')
        listo = b
        if option == 'Yes':
            count = count + 1
            continue
        elif option == 'No':
            print('You chose not to , so its fine by me')
            break
    else:
        print('You only get 2 times limit to do a difference')
    return b

def seasonal_difference(listo):
    print('\n\nbefore differencing\n',listo)
    count = 0
    while (count<2):
        seasonal_difference = int(input('Enter the seasonal difference interval you wish to choose:'))
        empty_list = []
        for i in range(0,len(listo)-seasonal_difference):
            if seasonal_difference < len(listo):
                empty_list.append(listo[i+(seasonal_difference)]-listo[i])
                 
            else:
                seasonal_difference = int(input('Re-enter the seasonal difference interval you wish to choose:'))
                continue
        print('proceeding after validation check')
        print('the seasonal_differenced_list is  and its length is :',empty_list,len(empty_list))
        
        
        print('The ACF & PACF calculations are as follows:')
        pair_list = pairs(empty_list)
        acf_values = correls(pair_list)
        pacf_values = PACF_values(empty_list)
        y = p_or_q_value(acf_values,empty_list)
        print('p value is ',y)
        
        x = p_or_q_value(acf_values,empty_list)
        print('q value is',x)

        option = input('Do you wish to conduct seasonal differencing again:')
        listo = empty_list
        if option == 'Yes':
            count = count + 1
            continue
        elif option == 'No':
            print('You chose not to , so its fine by me')
            break
    else:
        print('You only get 2 times limit to do a difference')
    return empty_list

def p_or_q_value(list3,b):
    threshold = 1.96/(math.sqrt(len(b)))
    print('The threshold is :',threshold)
    #threshold = 0.55
    b = list()
    for i in range(1,len(list3)):
        if list3[i] > threshold or list3[i] < -threshold:
            b.append(list3[i])
        else:
            continue
    z = b[-1]
    print(z)
    for i in range(0,len(list3)):
        if list3[i] == z:
            index = list3.index(list3[i])
            break
        else:
            continue
    return index

def AIC(p,q,variance,n):
    m = p + q + 1
    aic_value = n*(1 + math.log10(2*(22/7))) + (n*math.log10(variance)) + (2*m)
    return aic_value


def process_ARIMA(main_list):
    print('\nwelcome, we are going to demonstrate an ARIMA process')
    
    print('\nCalculating the PACF, ACF values,p & q values so as to give you an idea on what to proceed with:')
    
    initial_demo = pairs(main_list)
    initial_demo_acf_values = correls(initial_demo)
    initial_demo_pacf_values = PACF_values(main_list)
    
    
    plot_ACF_graph(initial_demo_acf_values)
    plot_PACF_graph(initial_demo_pacf_values)
    
    y = p_or_q_value(initial_demo_acf_values,main_list)
    print('q value is ',y)
    
    x = p_or_q_value(initial_demo_pacf_values,main_list)
    print('p value is ',x)

    while True:
        option1 = input('\nWould you like to procceed with seasonal differencing ?')
        
        if option1 ==  'Yes':
            #insert method required for S.D
            seasonal_list = seasonal_difference(main_list)
            print('Its seasonally differenced now')
            
            option2 = input('\nWould you now like to proceed with Normal differencing')
            
            if option2 == 'Yes':
                normal_list1 = normal_difference(seasonal_list)
                #insert method required for N.D
                print('\nIts normally differenced now')
                break
                
            else:
                break
                
        elif option1 == 'No':
            
            option3 = input('\nWould you like to proceed with normal differencing ?')
            if option3 == 'Yes':
                normal_list2 = normal_difference(main_list)
                print('\nIts normally differenced now')
                break
            else:
                break



process_ARIMA(number_of_users)