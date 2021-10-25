
import codecs

line_seen=set()#初始化空的无序集合

in_file=codecs.open('E:/codes/track1.txt','r',encoding='utf-8')

out_file=codecs.open('E:/codes/track_1.txt','w',encoding='utf-8')

lines=in_file.readlines()

for line in lines:
    for i in line:
        if not i.isalpha() and i != ':' and i != '(' and i != ')' and i!=' ':
            out_file.write(i)
            line_seen.add(i)

in_file.close()
out_file.close()