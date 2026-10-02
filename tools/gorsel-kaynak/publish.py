import json,sys,shutil,os,glob
R='/home/claude/klinikfarmakoloji-site/'; G=R+'sites/default/files/yazi-gorselleri/'
m=json.load(open(sys.argv[1])); n=0
for aid,base in m.items():
    for f in glob.glob(f'out/{aid}.*.png'):
        lang=f.split('.')[-2]; shutil.copy(f,G+base+'.'+lang+'.png'); n+=1
print('copied',n)
