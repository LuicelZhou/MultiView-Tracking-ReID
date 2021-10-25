import codecs

line_seen=set()#初始化空的无序集合

in_file=codecs.open('I:/codes/track4new.txt','r',encoding='utf-8')

out_file=codecs.open('I:/codes/track4.1.txt','w',encoding='utf-8')

lines=in_file.readlines()

for line in lines:
    if line not in line_seen:
        out_file.write(line)
        line_seen.add(line)

in_file.close()
out_file.close()
