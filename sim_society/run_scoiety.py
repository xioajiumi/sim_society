import roles
import settings


def build_admin(*args,**kwargs):
    return roles.Admin(*args,**kwargs)
def build_officer(*args,**kwargs):
    return roles.Officer(*args,**kwargs)
def build_common_people(*args,**kwargs):
    return roles.CommonPeople(*args,**kwargs)
def build_breaker(*args,**kwargs):
    return roles.Breaker(*args,**kwargs)
def build_table(*args,**kwargs):
    return roles.Table(*args,**kwargs)

#officer is asking for money
def give_your_money(admin,officer,people,year):
    cost=officer.money_asked
    res,is_breaker=people.give_money(admin,cost)
    officer.record[year].append(1 if res else 0)
    if res:
        officer.money+=cost
        people.money+=(people.value_of_education-cost)
    #people who don't give the money could due to expensive or breaker
    #only breaker inspire other to be more brave and less materialism
    elif is_breaker:
        admin.reject_odd+=admin.reject_odd_incr
        people.money-=people.value_of_education



def main():
    print("start game")
    table=build_table()
    admin=build_admin({"id":"admin_1"})
    officer=build_officer({"id":"officer_1","record":{}})
    breakers=[build_breaker({"id":f"breaker_{0+1}"}) for i in range(0,settings.BREAKER_NUM)]
    common_peoples=[build_common_people({"id":f"common_{0+1}"}) for i in range(0,settings.COMMON_NUM)]
    # peoples=common_peoples+breakers
    peoples=breakers+common_peoples
    for year in range(settings.START_YEAR,settings.MAX_YEAR+1):
        # print("#"*30,"year%d"%year)
        print(admin.reject_odd)

        officer.record[str(year)]=[]
        [give_your_money(admin,officer,people,str(year)) for people in peoples]
        # officer.register(str(year),table=table)
        print(officer.record[str(year)])
        officer.check(str(year),table=table)


if __name__=="__main__":
    main()