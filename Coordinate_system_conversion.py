import numpy as np
import cv2
import xlrd
import pandas as pd

in_para1=np.array([[11.4068441,0,9.60,0],[0,11.4068441,5.40,0],[0,0,1,0]])#相机的内参矩阵dx=0.263 uo、vo取分辨率的一半
in_para2=np.array([[11.4068441,0,9.60,0],[0,11.4068441,5.40,0],[0,0,1,0]])
in_para3=np.array([[11.4068441,0,9.60,0],[0,11.4068441,5.40,0],[0,0,1,0]])
in_para4=np.array([[11.4068441,0,9.60,0],[0,11.4068441,5.40,0],[0,0,1,0]])

ex_para1=np.array([[0.773881136,0.633330867,0,5.58],[-0.633330867,0.773881136,0,-1.20],[0,0,1,2.18],[0,0,0,1]])#外参矩阵
ex_para2=np.array([[0.264073984,0.964502427,0,6.19],[-0.964502427,0.264073984,0,17.60],[0,0,1,2.16],[0,0,0,1]])
ex_para3=np.array([[0.361529815,0.932360549,0,5.20],[-0.932360549,0.361529815,0,-22.44],[0,0,1,2.23],[0,0,0,1]])
ex_para4=np.array([[0.270065249,-0.962842023,0,-9.98],[0.962842023,0.270065249,0,-2.81],[0,0,1,1.92],[0,0,0,1]])


mul1=np.dot(in_para1,ex_para1)#内外参乘积
mul2=np.dot(in_para2,ex_para2)
mul3=np.dot(in_para3,ex_para3)
mul4=np.dot(in_para4,ex_para4)

exc = pd.read_csv(r'C:\Users\景大帅\Desktop\xy.csv')#导入excel中的u0,v0
finn = exc.values
fin=finn.astype(float)
#print(fin)
uandv = fin[:, 7:]#行人轨迹坐标x_t,y_t
vandu =uandv.T#转置
vvandu=np.mat(vandu)

#print(vandu)

xl=fin[:,3] #标定框左上角x坐标
yl=fin[:,4] #标定框左上角y坐标
x_t=fin[:,7] #标定中心坐标x
y_t=fin[:,8] #标定中心坐标y

num=fin[:,2] #人的序号


xll=np.mat(xl)
yll=np.mat(yl)
x_tt=np.mat(x_t)
y_tt=np.mat(y_t)




#像素坐标
came_loc=vvandu #[u0,v0,1]
#print(xll.shape)

#相似三角形求lamda=Zc
h=2*(yll-y_tt)*0.00263 #像素点的个数*大小=图像高度
#print(h.shape)
lamda = (1.68*0.03/h)-0.03

lamda=np.tile(lamda, (4,1))
#print(lamda)

#print(np.mat(np.linalg.pinv(mul1)).shape)
#print(np.mat(came_loc).shape)
global_loc1 = np.dot(np.mat(np.linalg.pinv(mul1)),np.mat(came_loc))  #mul1求伪逆

global_loc11=np.multiply(global_loc1,lamda) #第一个摄像头转化为世界坐标

#print(global_loc)
#print(global_loc1.shape)
#print(np.shape(np.linalg.pinv))
#print(global_loc1)
#print(global_loc11)

global_loc2 = np.dot(np.mat(np.linalg.pinv(mul2)),np.mat(came_loc))  #mul1求伪逆

global_loc22=np.multiply(global_loc2,lamda) #第二个摄像头转化



global_loc3 = np.dot(np.mat(np.linalg.pinv(mul3)),np.mat(came_loc))  #mul1求伪逆

global_loc33=np.multiply(global_loc3,lamda)#第三个摄像头转化


global_loc4 = np.dot(np.mat(np.linalg.pinv(mul4)),np.mat(came_loc))  #mul1求伪逆

global_loc44=np.multiply(global_loc4,lamda) #第四个摄像头转化
numpy.savetxt("new.csv", global_loc11, delimiter=',')














