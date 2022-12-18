//點擊mark回家
function goHome(){
    window.location.href = "http://35.76.166.101:3000"
}

//開視窗載入
    //檢查登入狀態
    let loginUrl = "http://35.76.166.101:3000/api/user/auth";
    
    fetch(loginUrl)
    .then(res =>{
        res = res.json();
        return res
    })
    .then(result =>{
        let bookingUrl = "http://35.76.166.101:3000/booking"
        if (result["data"] != null){                 //  result = 使用者資訊;           
            let userData = "userData = " + JSON.stringify(result);     
            document.cookie =  userData;            //將使用者資訊存放到cookie供使用
            if((location.href) != bookingUrl){
                let signOpen = (document.querySelectorAll(".forNav"))[1];
                let signOut = document.querySelector(".forNav_hide");
                signOut.classList.remove("forNav_hide")
                signOpen.classList.add("forNav_hide")
            }else{
                window.location.href = "http://35.76.166.101:3000"
            }
        }
    })
// 登入及註冊介面
const sign = document.querySelector(".sign");
// 開啟signBar
function signOpen(){
    sign.classList.add("sign_active");
}
// 關閉signBar
function signClosed(){
    sign.classList.remove("sign_active");
    let Sign_barHide = document.querySelector(".sign_bar_hide");
    Sign_barHide.classList.remove("sign_bar_hide");
    let signupBar = (document.querySelectorAll(".sign_bar"))[1];
    signupBar.classList.add("sign_bar_hide");
    reminder2.style = "display:none";
    reminder1.style = "display:none";
    let forms = document.getElementsByTagName("input");
    for(x=0; x<forms.length; x++){
        forms[x].value  ="";
    }
    let signupButtton = document.querySelector("#sign_up_button");
    signupButtton.value = "註冊帳戶";
    let signinButtton = document.querySelector("#sign_in_button");
    signinButtton.value = "登入帳戶";
    //眼睛和密碼欄位重設
    let eyeactive = document.querySelector(".eyeactive");
    eyeactive.classList.remove("eyeactive");
    let passwordeyeO = document.querySelector(".passwordeyeO");
    passwordeyeO.classList.remove("signup_eye");
    passwordeyeO.classList.add("eyeactive");
    let password1 = (document.querySelector("#signinform").querySelectorAll(".sign_text"))[1];
    let password2 = (document.querySelector("#signupform").querySelectorAll(".sign_text"))[2];
    password1.setAttribute("type","password");
    password2.setAttribute("type","password");
}
//signBar切換
function signswitch(){
    let signBars = document.querySelectorAll(".sign_bar");
    for(x=0; x<2; x++){
        signBars[x].classList.toggle("sign_bar_hide");
    };

    //眼睛
    let eyeactives = document.querySelectorAll(".eyeactive");
    for(x=0; x<(eyeactives.length); x++){
        eyeactives[x].classList.remove("eyeactive");
    }
    let passwordeyeOs = document.querySelectorAll(".passwordeyeO");
    for(x=0; x<2; x++){
        passwordeyeOs[x].classList.add("eyeactive");
    }
    let password1 = (document.querySelector("#signinform").querySelectorAll(".sign_text"))[1];
    let password2 = (document.querySelector("#signupform").querySelectorAll(".sign_text"))[2];
    password1.setAttribute("type","password");
    password2.setAttribute("type","password");
};
//密碼的眼睛切換
function eyeSwitch(){
    let passwordeyeOs = document.querySelectorAll(".passwordeyeO");
    let passwordeyeCs = document.querySelectorAll(".passwordeyeC");
    for(x=0; x<2; x++){
        passwordeyeOs[x].classList.toggle("eyeactive");
        passwordeyeCs[x].classList.toggle("eyeactive");
    };
    let signBars = document.querySelectorAll(".sign_bar");
    let notLocation = 0;
    for(x=0; x<2; x++){
        let signBar = signBars[x]
        for(n=0; n<(signBar.classList).length; n++){
            if((signBar.classList)[n] == "sign_bar_hide"){
                notLocation = x
            }
        };
    };
    console.log( notLocation )
    let password =null;
    if(notLocation == 1){
        password = (document.querySelector("#signinform").querySelectorAll(".sign_text"))[1]
    }else{
        password = (document.querySelector("#signupform").querySelectorAll(".sign_text"))[2]
    };
    if(password.type == "password"){
        password.setAttribute("type","text")
    }else{
        password.setAttribute("type","password")
    }
}

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
            userData = null;
            let bookingUrl = "http://35.76.166.101:3000/booking"
            if((location.href) == bookingUrl){
                document.location.href = "http://35.76.166.101:3000/"
            }else{
                location.reload();
            }
        }
    })
})

//切換至「預定行程」
let reserveJourney = document.querySelectorAll(".forNav-1")[0]
reserveJourney.addEventListener("click",()=>{
    let login_token = document.cookie.indexOf("login_token");
    if(login_token == -1){
        signOpen()
    }else{
        document.location.href = "http://35.76.166.101:3000/booking"
    }
})

