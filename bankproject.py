import cx_Oracle
import smtplib
import getpass
import random
import os
import datetime
import smtplib
def Send_mail(msg):
    mail = smtplib.SMTP('smtp.gmail.com', 587)
    mail.ehlo;
    mail.set_debuglevel(1)
    mail.starttls()
    mail.login("jeya.krithiga98@gmail.com","jeya.krithiga98")
    res=mail.sendmail("jeya.krithiga98@gmail.com","kjeyakrithiga@gmail.com",str(msg))
    mail.quit()
con=cx_Oracle.connect("bank/mymailid")
print(con.version)
cur=con.cursor()
cur.execute("drop table tab")
cur.execute("create table tab(fname varchar(30),lname varchar(30),pinno int,accno int,amount int,date1 varchar(30),time1 varchar(30))")
class transactA:
    def __init__(self,amt):
        self.amt=amt
    def deposit(self):
        self.amount1=int(input("ENTER DEPOSIT AMOUNT:"))
        self.amt=self.amt+self.amount1
        print("BALANCE AMOUNT IN YOUR ACCOUNT:",self.amt)
        Send_mail("\n\n An amount of "+str(self.amount1)+" has been deposited into your account. Your current Balance is :"+str(self.amt)+". \n Thank You")
        return self.amt
    def withdraw(self):
        self.pinno=int(input("ENTER PIN NUMBER FOR AUTHENTICATION"))
        self.amount=int(input("ENTER WITHDRAWAL AMOUNT"))
        if(self.amt<self.amount):
            print("YOU HAVE NO ENOUGH AMOUNT IN YOUR ACCOUNT!!!")
        else:
            self.amt=self.amt-self.amount
            print("WITHDRAW SUCCESS!!!")
            print("BALANCE AMOUNT IN YOUR ACCOUNT:",self.amt)
        Send_mail("\n\n An amount of "+str(self.amount)+" has been deposited into your account. Your current Balance is :"+str(self.amt)+". \n Thank You")
        return self.amt
    def transfer(self):
        self.accnum=int(input("ENTER THE ACCOUNT NUMBER FOR TRANSACTION:"))
        cur.execute("select amt from tab where pin=:1",(self.accnum))
        self.amt1=cur.fetchone()
        self.amt1=self.amt1+amt
        print("amt1:",self.amt1)
        Send_mail("An amount of "+self.amt1+" has been deposited into your account")
        return self.amt1
def balance(pin):
    print("BALANCE ENQUIRY")
    cur.execute("SELECT amount FROM tab WHERE pinno=:a",{'a':pin})
    res=cur.fetchone()
    amo=res[0]
    print("Current balance amount in your account is : ",end="")
    print(amo)
    print("Type 'Yes' if you want receipt else 'No'")
    st=input()
    if(st.upper()=="YES"):
        print("receipt")
    else:
        print("No receipt")
def transact(pin2):
     print("TRANSACT")
     print("1.MONEY DEPOSIT","2.MONEY WITHDRAW","3.TRANSFER")
     ch=int(input("ENTER KIND OF TRANSACTION"))
     cur.execute("SELECT amount FROM tab WHERE pinno= :a",{'a':pin2})
     amt=list(cur.fetchone())
     amt4=int(amt[0])
     t=transactA(amt4)
     if ch==1:
         amt5=t.deposit()
         cur.execute("UPDATE tab SET amount=:a WHERE pinno=:b",{'a':amt5,'b':pin2})
         con.commit()
     elif ch==2:
         amt5=t.withdraw()
         cur.execute("UPDATE tab SET amount=:a WHERE pinno=:b",{'a':amt5,'b':pin2})
         con.commit()
     elif ch==3:
         amt5=t.transfer()
         cur.execute("UPDATE tab SET amount=:a WHERE pinno=:b",{'a':amt5,'b':pin2})
         con.commit()
     return amt
def signin():
    print("\n\t\t\tSIGN IN\t:\t")
    accno1=input("\n\tPrint your account number to sign in\t:\t")
    
    print("\n\t\t\tEnter your password  :",end="")
    #pin1=getpass.getpass(stream=None)
    pin1=int(input())
    for i in range(0,80):
        print("_",end="")
    print("HELLO",emailid,"!!!")
    stop=0
    print("pin1:",pin1)
    os.system('cls')
    while stop!=1:
        print("1.BALANCE ENQUIRY","2.TRANSACT","3.PRINT STATEMENT","4.ACCOUNT CLOSURE","5.CUSTOMER LOGOUT")
        choice=int(input("ENTER YOUR CHOICE"))
        if choice==1:
            balance(pin1)
        elif choice==2:
            transact(pin1)
        elif choice==3:
            printstatement()
        elif choice==4:
            accclose(pin1)
        elif choice==5:
            stop=1
            logout(pin1)
            cur.close()
            con.close()
            break

def signup():
    print("\n\t\tEnter your first name\t\t:\t",end="")
    fname=input()
    #print("\t\t\t",end="")
    print("\n\t\tEnter your last name\t\t:\t",end="")
    lname=input()
    pin=int(input("\n\t\tEnter your 6-digit PIN number\t:\t"))
    if(len(str(pin))<6):
      print("\n\t\t\t\tInvalid PIN")
      print("\n\t\tPLEASE RE-ENTER YOUR PIN\t:\t")
      pin=int(input())
    amt=int(input("\n\t\tEnter the initial deposit amount:\t"))
    date1=datetime.datetime.now()
    accno=random.randint(10000000000,100000000000)
    cur.execute("insert into tab values(:1,:2,:3,:4,:5,:6,:7)",(fname,lname,pin,accno,amt,str(date1)[:10],str(date1)[11:19]))
    print("\n\t\t\t SIGNED UP SUCCESSFULLY.....")
    Send_mail("\n\n Kindly note your account number : "+str(accno)+". \nThank You")
    #print("mes:",mes1)
    print("\n\t\tPRESS 1 FOR SIGNIN OR 2 TO END PROCESS")
    choi=int(input())
    if(choi==1):
        signin()
    else:
        cur.execute("select * from tab")
        res=cur.fetchall()
        for r in res:
            print("r:",r)
if __name__=='__main__':
    print("\n\t\t\t\tBANKING SYSTEM\t\t\t")
    ch1=int(input("\n\tNEW USER ENTER :1 ELSE ENTER :2"))
    if(ch1==1):
        signup()
        con.commit()
    elif(ch==2):
        signin()
    #cur.close()
    #con.close()
