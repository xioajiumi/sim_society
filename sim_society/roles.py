from random import random
import settings
import pandas as pd

class Role():
    def __init__(self,status,default_status) -> None:
        # use default status if custom status is not full
        if status != default_status:
            for k,v in default_status.items():
                if not getattr(status,k,None):
                    val=v
                else:
                    val=status[k]
                    del status[k]
                status[k.lower()]=val
        self.status=status
        for k,v in self.__dict__["status"].items():
            setattr(self,k.lower(),v)
            getattr(self,k.lower())


    def register(self,*args,**kwargs):
        print("register")



class Admin(Role):    
    def __init__(self,status=settings.ADMIN_STATUS) -> None:
        super().__init__(status,settings.ADMIN_STATUS)


class Table(Role):
    def __init__(self,status=settings.TABLE_STATUS) -> None:
        super().__init__(status,settings.TABLE_STATUS)
    def save(self):
        print("save table")



class Officer(Role):
    def __init__(self,status=settings.OFFICER_STATUS) -> None:
        super().__init__(status,settings.OFFICER_STATUS)
    def register(self, *args, **kwargs):
        year=args[0]
        table=kwargs["table"]
        super().register()

    def check(self,year,table):
        def give_percent(year):
            total=len(self.record[year])
            gived=sum(self.record[year])
            return gived/total
        def fuck_off(self,year,time_to_fuck_off):
            percent,past_years=time_to_fuck_off
            #officer won't fuck off at first
            if int(year)<past_years:
                sig=False
            else:
                sig=True
                for year in range(int(year)+1-past_years,int(year)+1):
                    if give_percent(str(year))>=(1-percent):
                        sig=False
                        break
            return sig
        def incr(self,year,time_to_incr):
            percent,past_years,rate=time_to_incr
            if int(year)<past_years:
                sig=False
            else:
                sig=True
                for year in range(int(year)+1-past_years,int(year)+1):
                    if give_percent(str(year))<percent:
                        sig=False
                        break
            return sig
        def dec(self,year,time_to_dec):
            percent,past_years,rate=time_to_dec
            if int(year)<past_years:
                sig=False
            else:
                sig=True
                for year in range(int(year)+1-past_years,int(year)+1):
                    if (1-give_percent(str(year)))<=percent:
                        sig=False
                        break
            return sig
            

        time_to_fuck_off=fuck_off(self,year,self.time_to_fuck_off)
        time_to_incr=incr(self,year,self.time_to_incr)
        time_to_dec=dec(self,year,self.time_to_dec)   
        if time_to_incr:
            self.money_asked*=(1+self.time_to_incr[2])
        if time_to_dec:
            self.money_asked*=(1-self.time_to_dec[2])

        print("money asked%f"%self.money_asked)

class CommonPeople(Role):
    def __init__(self,status=settings.COMMON_STATUS) -> None:
        super().__init__(status,settings.COMMON_STATUS)
    
    #Have certain probability to be a breaker temporally, else do the cost and benefit analysis
    def give_money(self,admin,cost):
        if random()<admin.reject_odd:
            sig=False
            is_breaker=True
        else:
            sig=True if ((self.value_of_education-cost)>=(-self.value_of_education)) else False
            is_breaker=False
        return (sig,is_breaker)


class Breaker(Role):
    def __init__(self, status=settings.BREAKER_STATUS) -> None:
        super().__init__(status, settings.BREAKER_STATUS)

    # never give money
    def give_money(self,admin,cost):
        return (False,True)

