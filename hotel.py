import pandas as pd
from datetime import datetime, date, timedelta
import sys
hotel = pd.read_csv('hotel.csv', index_col=0)
hotel = hotel.astype({
    "Guests": "object",
    "Check_in": "object",
    "Expected_check_out": "object",
    "room_type": "object",
    "breakfast_included": "object",
})
print(
'''
██   ██  ██████  ████████ ███████ ██           ██████  ███████     ██    ██  ██ 
██   ██ ██    ██    ██    ██      ██          ██    ██ ██          ██    ██ ███ 
███████ ██    ██    ██    █████   ██          ██    ██ ███████     ██    ██  ██ 
██   ██ ██    ██    ██    ██      ██          ██    ██      ██      ██  ██   ██ 
██   ██  ██████     ██    ███████ ███████      ██████  ███████       ████    ██ 
''')
select=int(input("1.Customer login \n 2. Admin login \n"))
if select ==1:
    num=int(input("Enter the number of guests staying:"))
    options=["Suite(₹10,000 per night)","Double(₹7,000 per night)","Single(₹4,000 per night)"]
    room_types=["Suite","Double","Single"]
    if num>3:
        print(f"Your options are: \n 0.{options[0]}")
    elif num>1:
        print(f"Your options are: \n 0.{options[0]} \n 1.{options[1]}")
    elif num ==1:
        print(f"Your options are: \n 0.{options[0]} \n 1.{options[1]} \n 2.{options[2]}")
    else:
        print("Invalid number of guests! \n Exiting now!")
        sys.exit()
    selected=int(input("Select one of the above:"))
    if selected not in range(3):
        print("Invalid Room Type! \n Exiting now!")
        sys.exit()
    if num>3 and selected!=0:
        print("Invalid Room Type! \n Exiting now!")
        sys.exit()
    if num>1 and selected not in [0,1]:
        print("Invalid Room Type! \n Exiting now!")
        sys.exit()
    print("Would you like breakfast to be included ?(₹600 per person)")
    breakfast=input("Type Y for yes and N for no:").strip().upper() == "Y"
    date_str = input("Enter a date (YYYY-MM-DD): ")

    try:
        date_in = datetime.strptime(date_str, "%Y-%m-%d").date()

        if date_in >= date.today():
            pass
        else:
            print("Date cannot be in the past")
            sys.exit()

    except ValueError:
        print("Invalid date format")
        sys.exit()
    date_str = input("Enter a date (YYYY-MM-DD): ")

    try:
        date_out = datetime.strptime(date_str, "%Y-%m-%d").date()

        tomorrow = date.today() + timedelta(days=1)

        if date_out >= tomorrow and date_out>date_in:
            pass
        else:
            print("Date must be tomorrow or later and greater than date of check in")
            sys.exit()

    except ValueError:
        print("Invalid date format")
        sys.exit()
    prices=[10000,7000,4000]
    days=(date_out-date_in).days
    base_bill=prices[selected]*days
    breakfast_bill=num*breakfast*600*days
    raw_bill=base_bill+breakfast_bill
    tax=0.05*raw_bill
    final_bill=raw_bill+tax+300 #raw bill + 5% gst + service charges
    bill_details=f"Base: ₹{base_bill} + Breakfast: ₹{breakfast_bill} + Tax: ₹{tax} + Service: ₹300 = Total: ₹{final_bill}"
    names=[]
    for i in range(num):
        name=str(input(f"Enter the name of the guest no. {i}:"))
        names.append(name)
    print("Your final bill is ",bill_details)
    i=input("Press Y to book and N to cancel:").strip().upper() == "Y"
    if i:
        available_rooms = hotel[
            (hotel["available"] == 1)
            & (hotel["room_type"].astype(str).str.startswith(room_types[selected]))
        ]

        if available_rooms.empty:
            print("Sorry no room of the selected type is available. \n Exiting now")
            sys.exit()

        room_no = available_rooms.index[0]
        hotel.loc[room_no]=[", ".join(names),date_in,date_out,num,options[selected],"Y" if breakfast else "N",bill_details,0]
        hotel.to_csv("hotel.csv")
        print(f"Room no. {room_no} has been booked.")
    else:
        print("Booking cancelled.")
elif select == 2:
    while True:
        admin=int(input("1.View all guests \n 2.View stay history \n 3.Check out guest \n 4.Add complimentary breakfast \n 5.Exit \n"))
        if admin==1:
            guests=hotel[hotel["available"]==0]
            if guests.empty:
                print("No guests are staying right now")
            else:
                print(guests[["Guests","Check_in","Expected_check_out","no_guests","room_type","breakfast_included","bill"]])
        elif admin==2:
            history=pd.read_csv("history.csv")
            print(history)
        elif admin==3:
            room_no=int(input("Enter room no. to check out:"))
            if room_no not in hotel.index:
                print("Invalid room number")
                continue
            if hotel.loc[room_no,"available"]==1:
                print("Room is already empty")
                continue
            try:
                early_date=date.today()
                check_in=datetime.strptime(str(hotel.loc[room_no,"Check_in"]),"%Y-%m-%d").date()
                if early_date<check_in:
                    print("Checkout date is not valid. Guest hasn't checked in yet!")
                    continue
            except ValueError:
                print("Date is not correct")
                continue
            days=(early_date-check_in).days
            if days==0:
                days=1
            rtype=str(hotel.loc[room_no,"room_type"])
            if rtype.startswith("Suite"):
                price=10000
            elif rtype.startswith("Double"):
                price=7000
            else:
                price=4000
            people=int(hotel.loc[room_no,"no_guests"])
            breakfast=str(hotel.loc[room_no,"breakfast_included"]).strip().upper()=="Y"
            base_bill=price*days
            breakfast_bill=people*breakfast*600*days
            raw_bill=base_bill+breakfast_bill
            tax=0.05*raw_bill
            final_bill=raw_bill+tax+300
            bill_details=f"Base: ₹{base_bill} + Breakfast: ₹{breakfast_bill} + Tax: ₹{tax} + Service: ₹300 = Total: ₹{final_bill}"
            print("Final checkout bill is ",bill_details)
            history=pd.read_csv("history.csv")
            history.loc[len(history)]=[hotel.loc[room_no,"Guests"],hotel.loc[room_no,"Check_in"],early_date,room_no,hotel.loc[room_no,"room_type"],price,bill_details]
            history.to_csv("history.csv",index=False)
            hotel.loc[room_no]=["","", "",0,hotel.loc[room_no,"room_type"],"", "",1]
            hotel.to_csv("hotel.csv")
            print("Guest checked out and room is now available")
        elif admin==4:
            room_no=int(input("Enter room no. to add complimentary breakfast:"))
            if room_no not in hotel.index:
                print("Invalid room number")
                continue
            if hotel.loc[room_no,"available"]==1:
                print("Room is empty")
                continue
            hotel.loc[room_no,"breakfast_included"]="Y"
            try:
                date_in=datetime.strptime(str(hotel.loc[room_no,"Check_in"]),"%Y-%m-%d").date()
                date_out=datetime.strptime(str(hotel.loc[room_no,"Expected_check_out"]),"%Y-%m-%d").date()
            except ValueError:
                print("Dates are not correct")
                continue
            days=(date_out-date_in).days
            rtype=str(hotel.loc[room_no,"room_type"])
            if rtype.startswith("Suite"):
                price=10000
            elif rtype.startswith("Double"):
                price=7000
            else:
                price=4000
            people=int(hotel.loc[room_no,"no_guests"])
            base_bill=price*days
            breakfast_bill=0
            raw_bill=base_bill+breakfast_bill
            tax=0.05*raw_bill
            final_bill=raw_bill+tax+300
            bill_details=f"Base: ₹{base_bill} + Breakfast: ₹{breakfast_bill} complimentary + Tax: ₹{tax} + Service: ₹300 = Total: ₹{final_bill}"
            hotel.loc[room_no,"bill"]=bill_details
            hotel.to_csv("hotel.csv")
            print("Complimentary breakfast added")
            print("New bill is ",bill_details)
        elif admin==5:
            print("Exiting admin panel")
            break
        else:
            print("Invalid option")
else:
    print("Invalid option")
