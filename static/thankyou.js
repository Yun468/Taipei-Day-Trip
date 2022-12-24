//開視窗取得訂單編號
let currentUrlPath = location.href;
let arr = currentUrlPath.split("?number=");
let serial_number = arr[1];
let paidResult = serial_number.indexOf("&");
if ( paidResult !== -1){
    serial_number = (serial_number.split("&"))[0];
}

let number = document.querySelector(".number");
number.innerHTML = serial_number;
let result = document.querySelector(".result");
if (paidResult === -1){
    result.innerHTML = "成功"
}else{
    result.innerHTML = "失敗"
}


