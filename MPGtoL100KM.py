print(" ") 
print("==============Convert MPG to L/100KM==============") 
print(" ")

mpg = input("Enter MPG for your car: ")

def mpgToLper100km (mpg):
    return str(round(mpg = int(mpg) * (1.609344 / 4.54609188)), 2)
    #return str(round(mpg, 2))
	
print ("Your car uses " + mpgToLper100km(mpg) + " litters of gas per 100 km")

print(" ") 
print("==============End of MPG to L/100KM===============") 