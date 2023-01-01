//開視窗取得訂單編號
let currentUrlPath = location.href;
let arr = currentUrlPath.split("?number=");
let serial_number = arr[1];

//預防沒有訂單編號，跳轉首頁
if (serial_number == null || serial_number ==""){
    window.location.href = "http://35.76.166.101:3000"
};

//確認訂單是否成功付款
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


