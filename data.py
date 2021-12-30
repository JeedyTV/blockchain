import matplotlib.pyplot as plt


trans1 =
time1 = 

trans2 = 
time2 = 

trans3 = 
time3 = 

trans4 = 
time4 = 

trans5 = [1, 7, 11, 14, 21, 26, 50, 52]
time5 = [20, 33, 42, 65, 80, 155, 162, 179]

plt.plot(time1, trans1, label='Difficulty 1')
plt.plot(time2, trans2, label='Difficulty 2')
plt.plot(time3, trans3, label='Difficulty 3')
plt.plot(time4, trans4, label='Difficulty 4')
plt.plot(time5, trans5, label='Difficulty 5')
plt.xlabel('Time (s)')
plt.ylabel('Cumulated number of transactions')
plt.legend()
plt.show()