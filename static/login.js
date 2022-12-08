//開視窗載入
    //檢查登入狀態
    let loginUrl = "http://35.76.166.101:3000/api/user/auth";
    fetch(loginUrl)
    .then(res =>{
        res = res.json();
        return res
    })
    .then(result =>{
        const userData = result;                                    // userData = 使用者資料
        if (userData != null){
            let signOpen = (document.querySelectorAll(".forNav-1"))[1];
            let signOut = document.querySelector(".forNav_hide");
            signOut.classList.remove("forNav_hide")
            signOpen.classList.add("forNav_hide")
        }
    })
// 登入及註冊介面
const sign = document.querySelector(".sign");
// 開啟signBar
function signOpen(){
    sign.classList.add("sign_active")
}
// 關閉signBar
function signClosed(){
    sign.classList.remove("sign_active");
    reminder2.style = "display:none";
    reminder1.style = "display:none";
    let forms = document.getElementsByTagName("input");
    for(x=0; x<forms.length; x++){
        forms[x].value  ="";
    }

}
//signBar切換
function signswitch(){
    let signCloseds = document.querySelectorAll(".sign_closed")
    let signBars = document.querySelectorAll(".sign_bar");
    for(x=0; x<2; x++){
        signBars[x].classList.toggle("sign_bar_hide")
        signCloseds[x].classList.toggle("sign_closed_hide")
    };
};

// 註冊帳號
let signupButtton = document.querySelector("#sign_up_button");
const reminder2 = document.querySelector(".reminder2");
const emailRule = /^\w+((-\w+)|(\.\w+))*\@[A-Za-z0-9]+((\.|-)[A-Za-z0-9]+)*\.[A-Za-z]+$/;
signupButtton.addEventListener("click",()=>{
    let userInPut = document.querySelector("#signupform").getElementsByTagName("input");
    let name = userInPut[0].value;
    let email = userInPut[1].value;
    let password = userInPut[2].value;
    //欄位不可為空
    if (name == "" || email == "" || password ==""){
        reminder2.style = "display:flex"
        reminder2.innerHTML = "姓名、電郵、密碼欄位不可為空";
        return null;
    }
    // email正則表達式驗證有效性
    let vaild = emailRule.test(email);
    if (vaild == false){
        reminder2.style = "display:flex"
        reminder2.innerHTML = "請輸入有效電子郵件地址";
        return null;
    }
    //密碼應大於4字
    if(password.length < 4){
        reminder2.style = "display:flex"
        reminder2.innerHTML = "密碼長度應大於4個字";
        return null;
    }
    //註冊帳號
    let url = "http://35.76.166.101:3000/api/user";
    fetch(url, {
        method:"POST",
        body: JSON.stringify({
            "name" : name,
            "email" : email,
            "password" : password
        }),
        credentials: "include",
        cache:"no-cache",
        headers: new Headers({
            "Content-Type":"application/json; charset=UTF-8",
        }),
    })
    .then(res=>{
        res = res.json();
        return res
    })
    .then(result=>{
        console.log(result);
        if(result["ok"] == true){
            reminder2.style = "display:flex";
            reminder2.innerHTML = "註冊成功，請返回登入頁面重新登入";
        }
        else{
            let message = result["message"];
            reminder2.style = "display:flex";
            reminder2.innerHTML = message
        }
    })
})
//登入帳號
let signinButtton = document.querySelector("#sign_in_button");
const reminder1 = document.querySelector(".reminder1");
signinButtton.addEventListener("click",()=>{
    let userInPut = document.querySelector("#signinform").getElementsByTagName("input");
    let email = userInPut[0].value;
    let password = userInPut[1].value;
    //欄位不可為空
    if (email == "" || password ==""){
        reminder1.style = "display:flex"
        reminder1.innerHTML = "電郵、密碼欄位不可為空";
        return null;
    }
    // email正則表達式驗證有效性
    let vaild = emailRule.test(email);
    if (vaild == false){
        reminder1.style = "display:flex"
        reminder1.innerHTML = "請輸入有效電子郵件地址";
        return null;
    }
    //登入帳號
    let url = "http://35.76.166.101:3000/api/user/auth";
    fetch(url, {
        method:"PUT",
        body: JSON.stringify({
            "email" : email,
            "password" : password
        }),
        headers: new Headers({
            "Content-Type":"application/json; charset=UTF-8",
        }),
    })
    .then(res=>{
        res = res.json();
        return res
    })
    .then(result=>{
        if(result["ok"] == true){
            location.reload();
        }
        else{
            let message = result["message"];
            reminder1.style = "display:flex"
            reminder1.innerHTML = message;
        }
    })
})
//登出帳號
let signOut = (document.querySelectorAll(".forNav-1"))[2];
signOut.addEventListener("click",()=>{
    let url = "http://35.76.166.101:3000/api/user/auth";
    fetch(url, {
        method:"DELETE"
    })
    .then(res=>{
        res = res.json();
        return res
    })
    .then(result=>{
        if(result["ok"] == true){
            location.reload();
        }
    })
})