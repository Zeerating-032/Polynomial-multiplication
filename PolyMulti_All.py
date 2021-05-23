#-*-coding="utf8"-*-
import re

class fraction:
	def __init__(self, up, down):
		self.up=up
		self.down=down
	
	def __add__(f1, f2):
		d=f1.down*f2.down
		u=f1.up*f2.down+f2.up*f1.down
		u, d=reduction(u, d)
		return fraction(u, d)
	
	def __mul__(f1, f2):
		d=f1.down*f2.down
		u=f1.up*f2.up
		u, d=reduction(u, d)
		return fraction(u, d)
	
	def __str__(self):
		if self.up%self.down==0:
			return str(self.up//self.down)
		else:
			if self.down<0:
				self.up*=-1
				self.down*=-1
			return f"({self.up}/{self.down})" #括起來比較好看

class poly:
	def __init__(self, dict):
		self.dict=dict
		self.max_time=max(dict.keys())
		self.ky=list(dict.keys()) #key -> times 
		self.ve=list(dict.values()) #value -> coefficient

	def __mul__(p1, p2):
		mx=p1.max_time+p2.max_time
		has_calculated={i:fraction(0, 1) for i in range(mx, -1, -1)} #init result dict 
		
		for i in p1.ky:
			for j in p2.ky:
				has_calculated[i+j]+=p1.dict[i]*p2.dict[j]
				
		for i in list(has_calculated.keys()):
			if has_calculated[i].up==0: #分子是否為零
				del has_calculated[i]
		
		return poly(has_calculated)
	
	def __str__(self):
		out=""
		for i, j in zip(self.ve, self.ky):
			out+=f"+{i}x^{j}"

		if out.endswith("^1"):
			out=out[:-2]
		out=out.replace("+-","-")#一段轉化為簡寫的判斷
		out=out.replace("x^0","")
		out=out.replace("^1+","+")
		out=out.replace("^1-","-")
		out=out.replace("+1x","+x")
		out=out.replace("-1x","-x")
		if out.startswith("+"):
			out=out[1:]
		
		return out


def separate(que): #arg:str
	corrForm=re.match("^[x\d+-/.^()]+$", que) #格式檢查
	if corrForm is None:
		print("格式錯誤")
		exit(0)

	#ex. 3x(x^2+1)(2-x)1/2
	each=re.compile("[\w+-/.^]+")
	all_eq=re.findall(each, que) #['3x', 'x^2+1', '2-x', '1/2']
	
	return all_eq 

def to_p(all_eq): #arg:str list
	r=[] #r用來存所有poly
	for eq in all_eq:
		eq=eq[0]+eq[1:].replace("-", "+-") #等等方便直接分離 #若括號後即負號則不變
		li=eq.split("+") #["2", "-x"]
		dic={}
		for i in li:
			if "x" in i: #not constant
				a=re.match("([\S]*)x(\^[\d]+)?", i)
				coe, times=a.group(1), a.group(2) #coe = coefficient
				
				if coe=="" or coe=="-": #have no coe or only negative sign
					coe+="1"
				
				coe=stof(coe)
				times=int(times[1:]) if times is not None else 1 #去除前面的^
				dic[times]=coe
			else:
				dic[0]=stof(i)
				
		r.append(poly(dic)) #作完dict就轉成poly
	return r


def stof(num): #string to fraction #arg:str
	if "/" in num: #a fraction
		li=num.split("/")
		a, b=int(li[0]), int(li[1])
		
	elif "." in num: #a decimal
		li=num.split(".")
		a=int(li[0]+li[1])
		b=int("1"+"0"*len(li[1]))
		a, b=reduction(a, b) #約分縮小數字

	else: #an integet
		a, b=int(num), 1
	
	return fraction(a, b)

def reduction(a, b): #arg:two int
	c, d=max(a, b), min(a, b)
	while 1: #輾轉相除法
		if c%d==0:
			break
		else:
			c, d=d, c%d
	#(a, b)=d
	return a//d, b//d


def iter_mul(p_list): #arg:poly list
	pp=p_list[0]
	for i in p_list[1:]:
		pp*=i
	return pp


if __name__=="__main__":
	question=input("輸入一段多項式，各式以小括號分開:")
	
	eqs=separate(question)
	
	poly_li=to_p(eqs)
	
	p=iter_mul(poly_li)
	print(p)
