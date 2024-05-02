import matplotlib.pyplot as plt
x= [1,2,3]
# y = [mean(NSD_deeplab), mean(NSD_fasterViT), mean(NSD_maxFormer)]
# y_error = [std(NSD_deeplab), std(NSD_fasterViT), std(NSD_maxFormer)]
y=[3 ,4, 5]
y1 = [1,2,3,4,5]
y2 = [2,3,4,5,6]
y3 = [3,4,5,6,7,8]
y_error =[0.1,0.3,0.2]

colors = ['black','red','blue']
plt.errorbar(x,y,yerr = y_error,fmt= 'o',ecolor=('black','red','blue'),elinewidth = 1)

for i, y in enumerate([y1,y2,y3]):
    plt.scatter([x[i]] * len(y), y, color=colors[i], label=f'y{i+1}')
# Show plot
plt.show()
