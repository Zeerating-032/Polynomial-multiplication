#-*-coding="utf8"-*-
question=input("輸入一段多項式，各式以括號分開:")
sperate=question.split(")")
sperate.pop()
for i in range(len(sperate)):
	sperate[i]=sperate[i][1:]#將多項式依括號分開並刪除括號

def divide(sperate):#轉換str成dict
	all_list,symbol_lis=[],("+","-")
	for eq in sperate:
		temp,temp_lis,positive,finish="",[],True,{}
		for point in range(len(eq)):
			now=eq[point]
			if point==0 and now=='-':
				positive=False
				continue
			if not now in symbol_lis:
				temp+=now
			else:
				if not positive:
					temp='-'+temp
				temp_lis.append(temp)
				temp=""
				if now=='+':
					positive=True
				else:
					positive=False
		if not positive:
			temp='-'+temp
		temp_lis.append(temp)#temp_lis是一個依加減號分離的str list
		for i in temp_lis:
			if 'x' in i:
				j=i.split('x')#一段簡寫還原判斷
				if j[0]=="":
					j[0]=1
				elif j[0]=='-':
					j[0]=-1
				if j[1]=="":
					j[1]=1
				elif j[1][0]=='^':
					j[1]=j[1][1:]
				finish[int(j[1])]=int(j[0])
			else:
				finish[0]=int(i)
		all_list.append(finish)
	return all_list

def calculate(lis):
	length=len(lis)
	while length>=2:
		has_calculated={}
		a,b=lis[0],lis[1]
		max_time=max(a.keys())+max(b.keys())
		for i in range(max_time,-1,-1):#初始化相乘答案的dict
			has_calculated[i]=0
		for i in list(a.keys()):
			for j in list(b.keys()):
				has_calculated[i+j]+=a[i]*b[j]
		for i in list(has_calculated.keys()):
			if has_calculated[i]==0:
				del has_calculated[i]
		del lis[0]
		lis[0]=has_calculated
		length-=1
	return has_calculated

def output(dict):
	out=""
	for i in dict.keys():
		num,t_num=str(dict[i]),str(i)
		out=out+num+'x^'+t_num+'+'
	out=out[:-1]
	if out[0]=="1":
		out=out[1:]
	if out.endswith("^1"):
		out=out[:-2]
	out=out.replace("+-","-")#一段轉化為簡寫的判斷
	out=out.replace("x^0","")
	out=out.replace("^1+","+")
	out=out.replace("^1-","-")
	out=out.replace("+1x","+x")
	out=out.replace("-1x","-x")
	return out

#main
all_list=divide(sperate)
finish_eq=calculate(all_list)
out=output(finish_eq)
print(out)
