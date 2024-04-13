# Task 1
print("===Task 1===")

def find_and_print(messages, current_station):
    stations = ["Songshan", "Nanjing Sanmin", "Taipei Arena", "Nanjing Fuxing", "Songjiang Nanjing",
                "Zhongshan", "Beimen", "Ximen", "Xiaonanmen", "Chiang Kai-shek Memorial Hall",
                "Guting", "Taipower Building", "Gongguan", "Wanlong", "Jingmei", "Dapinglin",
                "Qizhang", "Xindian City Hall", "Xindian"]

    if current_station == "Qizhang":
        stations.insert(16, "Xiaobitan")

    count = {}
    for friend, message in messages.items():
        station_in_message = None
        for station in stations:
            if station in message:
                station_in_message = station
                break
        if station_in_message:
            if stations.index(current_station) > stations.index(station_in_message):
                count[friend] = stations.index(current_station) - stations.index(station_in_message)
            else:
                count[friend] = stations.index(station_in_message) - stations.index(current_station)

    nearest_friend = min(count, key=count.get) 
    print(nearest_friend)

messages = {
    "Leslie":"I'm at home near Xiaobitan station.",
    "Bob":"I'm at Ximen MRT station.",
    "Mary":"I have a drink near Jingmei MRT station.",
    "Copper":"I just saw a concert at Taipei Arena.",
    "Vivian":"I'm at Xindian station waiting for you."
}

find_and_print(messages, "Wanlong") 
find_and_print(messages, "Songshan")  
find_and_print(messages, "Qizhang")  
find_and_print(messages, "Ximen")  
find_and_print(messages, "Xindian City Hall")  


# Task 2
print("===Task 2===")

def book(consultants, hour, duration, criteria):
    available = []

    for consultant in consultants:
        is_available = True

        if 'free' in consultant:
            for i in range(duration):
                if hour + i in consultant['free']:
                    is_available = False
                    break
        
        if is_available:
            available.append(consultant)

    if available:
        best = available[0]

        for consultant in available:
            if criteria == 'price':
                if consultant['price'] < best['price']:
                    best = consultant
            elif criteria == 'rate':
                if consultant['rate'] > best['rate']:
                    best = consultant
        
        print(best['name'])

        if 'free' in best:
            best['free'].extend(range(hour, hour + duration))
        else:
            best['free'] = list(range(hour, hour + duration))
    else:
        print("No Service")


consultants=[
    {"name":"John", "rate":4.5, "price":1000},
    {"name":"Bob", "rate":3, "price":1200},
    {"name":"Jenny", "rate":3.8, "price":800}
]

book(consultants, 15, 1, "price")  
book(consultants, 11, 2, "price")  
book(consultants, 10, 2, "price")  
book(consultants, 20, 2, "rate")   
book(consultants, 11, 1, "rate")   
book(consultants, 11, 2, "rate")   
book(consultants, 14, 3, "price")  

# Task 3
print("===Task 3===")

def func(*data):
    List=list([])
    List.extend(data)
   
    word=''
    check=[]
    for word in List :
        if len(word)//2 != 0:
            check.append(word[len(word)//2]) 
        elif len(word) == 2:
            check.append(word[1])
        else:
            check.append(word[2])                   

    for i in check:
        if check.count(i) == 1:
            print(List[check.index(i)])    
            return
    print("沒有")
      
func("彭大牆", "陳王明雅", "吳明") 
func("郭靜雅", "王立強", "郭林靜宜", "郭立恆", "林花花")  
func("郭宣雅", "林靜宜", "郭宣恆", "林靜花") 
func("郭宣雅", "夏曼藍波安", "郭宣恆")


# Task 4
print("===Task 4===")
def get_number(index):
    answer = 0
    if index % 3 == 0:
        answer = 0 + 4*(index- index//3)- 1*index//3   
    else:
        answer = 0 + 4*(index - index//3) - 1*index//3         
    print(answer)

get_number(1) 
get_number(5)  
get_number(10)  
get_number(30) 

# Task 5 todo 
print("===Task 5===")
