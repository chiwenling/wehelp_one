// task 1
console.log("===Task 1===")
function findAndPrint(messages, current_station) {
    let stations = ["Songshan", "Nanjing Sanmin", "Taipei Arena", "Nanjing Fuxing", "Songjiang Nanjing",
                    "Zhongshan", "Beimen", "Ximen", "Xiaonanmen", "Chiang Kai-shek Memorial Hall",
                    "Guting", "Taipower Building", "Gongguan", "Wanlong", "Jingmei", "Dapinglin",
                    "Qizhang", "Xindian City Hall", "Xindian"];

    if (current_station === "Qizhang") {
        stations.splice(16, 0, "Xiaobitan");
    }

    let count = {};
    for (let [friend, message] of Object.entries(messages)) {
        let stationInMessage = '';
        for (let station of stations) {
            if (message.includes(station)) {
                stationInMessage = station;
                break;
            }
        }
        if (stationInMessage) {
            if (stations.indexOf(current_station) > stations.indexOf(stationInMessage)) {
                count[friend] = stations.indexOf(current_station) - stations.indexOf(stationInMessage);
            } else {
                count[friend] = stations.indexOf(stationInMessage) - stations.indexOf(current_station);
            }
        }
    }

    let minCount = '';
    let nearestFriend = '';

    for (let friend in count) {
        if (minCount === '' || count[friend] < minCount) {
            minCount = count[friend];
            nearestFriend = friend;
        }
    }
    console.log(nearestFriend);
}   

let messages = {
    "Leslie": "I'm at home near Xiaobitan station.",
    "Bob": "I'm at Ximen MRT station.",
    "Mary": "I have a drink near Jingmei MRT station.",
    "Copper": "I just saw a concert at Taipei Arena.",
    "Vivian": "I'm at Xindian station waiting for you."
};

findAndPrint(messages, "Wanlong");
findAndPrint(messages, "Songshan");
findAndPrint(messages, "Qizhang");
findAndPrint(messages, "Ximen");
findAndPrint(messages, "Xindian City Hall");


// task 2
console.log("===Task 2===")

function book(consultants, hour, duration, criteria) {
    let available = [];

    for (let consultant of consultants) {
        let isAvailable = true;
        
        if (consultant['booked'] === undefined) {
            available.push(consultant);
            continue;
        }

        for (let i = 0; i < duration; i++) {
            let isBooked = false;
            for (let bookedHour of consultant['booked']) {
                if (bookedHour === hour + i) {
                    isBooked = true;
                    break;
                }
            }
            if (isBooked) {
                isAvailable = false;
                break;
            }
        }

        if (isAvailable) {
            available.push(consultant);
        }
    }

    if (available.length === 0) {
        console.log("No Service");
        return;
    }

    let best = available[0];

    for (let consultant of available) {
        if (criteria === 'price') {
            if (consultant['price'] < best['price']) {
                best = consultant;
            }
        } else if (criteria === 'rate') {
            if (consultant['rate'] > best['rate']) {
                best = consultant;
            }
        }
    }

    console.log(best['name']);

    if (best['booked'] === undefined) {
        best['booked'] = [];
    }
    for (let i = hour; i < hour + duration; i++) {
        best['booked'].push(i);
    }
}

let consultants = [
    {"name": "John", "rate": 4.5, "price": 1000},
    {"name": "Bob", "rate": 3, "price": 1200},
    {"name": "Jenny", "rate": 3.8, "price": 800}
];

book(consultants, 15, 1, "price"); 
book(consultants, 11, 2, "price");  
book(consultants, 10, 2, "price");  
book(consultants, 20, 2, "rate");   
book(consultants, 11, 1, "rate");   
book(consultants, 11, 2, "rate");   
book(consultants, 14, 3, "price");  


// task 3
console.log("===Task 3===")

function func(...data){  
    let word='';
    let check=[];
    
    for(word of data){ 
        if(word.length/2 === 1){
            check.push(word[1]);
        }else if(word.length/2 === 2){
            check.push(word[2]);
        }else{
            check.push(word[Math.floor(word.length/2)]);
        }
    }
     
    for(let i = 0; i < check.length; i++){
        let count = 0;
        for(let j = 0; j < check.length; j++){
            if(check[i] === check[j]){
                count++;
            }
        }
        if(count === 1){
            console.log(data[i]);
            return;
        }
    }
    console.log("沒有");     
}

func("彭大牆", "陳王明雅", "吳明"); 
func("郭靜雅", "王立強", "郭林靜宜", "郭立恆", "林花花"); 
func("郭宣雅", "林靜宜", "郭宣恆", "林靜花"); 
func("郭宣雅", "夏曼藍波安", "郭宣恆");


// task 4
console.log("===Task 4===")
function getNumber(index){
    let answer = 0;
    if (index/3 === 0){
        answer = 0 + 4*(index-1*(index/3))-index/3;
    }else{
        answer = 0 + 4*(index-Math.floor(1*(index/3)))-Math.floor(index/3);
    }
    console.log(answer);
    return answer;
}
getNumber(1); 
getNumber(5);  
getNumber(10);  
getNumber(30);
