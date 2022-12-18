//開視窗取得使用者訂購行程
let url = "http://35.76.166.101:3000/api/booking";
fetch(url).then(res =>{
    res = res.json();
    return res
})
.then(result =>{                        //result = 行程
    //寫入使用者姓名
    let user = document.querySelector(".user");
    let userData = JSON.parse((document.cookie.split("userData=")[1]).split(";")[0]);       //從cookie 抓使用者資料並轉物件
    user.innerHTML = userData["data"]["name"] ;


    //預定行程內容
    if(result["data"] == null){
        let noneBooking = document.querySelector(".none_booking");
        noneBooking.style.display = "block";

    }else{
        let booking = document.querySelector(".booking");
        let form_connect = document.getElementsByName("form_connect")[0];
        booking.style.display = "grid";
        form_connect.style.display = "flex";
        
        //預定景點資訊
        let title = document.getElementById("title");
        let picture = document.querySelector(".section_picture");
        let date = document.getElementById("date");
        let time = document.getElementById("time");
        let price = document.getElementById("price");
        let place = document.getElementById("place");

        let realTime = ""
        if (result["data"]["time"] == "moring"){                      //判斷時間
            realTime = "上午9點至中午12點"
        }else{
            realTime  = "下午14點至下午17點"
        }

        title.innerHTML = result["data"]["attraction"]["name"]
        picture.setAttribute("style", "background-image:url(" + result["data"]["attraction"]["image"] + ")");
        date.innerHTML = result["data"]["date"];
        time.innerHTML =  realTime ;
        price.innerHTML = result["data"]["price"];
        place.innerHTML = result["data"]["attraction"]["address"];


        //使用者資料自動填入
        let name = document.getElementsByName("name")[0];
        let email = document.getElementsByName("email")[0]
        name.value = userData["data"]["name"];
        email.value = userData["data"]["email"];

        //計算總價
        let sum = document.getElementById("sum");
        sum.innerHTML = result["data"]["price"];

        //將景點編號存入deleteButton
        let deleteButton = document.querySelector(".delete");
        let attractionID = result["data"]["attraction"]["id"]
        deleteButton.setAttribute("data-attractionid",attractionID)     
    }
});


//刪除訂購行程
let deleteButton = document.querySelector(".delete");
deleteButton.addEventListener("click",()=>{
let url = "http://35.76.166.101:3000/api/booking";

    let attractionId = deleteButton.dataset.attractionid

    fetch(url, {
        method:"DELETE",
        body: JSON.stringify({
            "attractionId" : attractionId
        }),
        credentials: "include",
        cache:"no-cache",
        headers: new Headers({
            "Content-Type":"application/json; charset=UTF-8",
        }),
    }).then(res =>{
        res = res.json();
        return res
    }).then(result =>{                      //result = 行程
            //寫入使用者姓名
            if(result["ok"] == true){
                let user = document.querySelector(".user");
                let userData = JSON.parse((document.cookie.split("userData=")[1]).split(";")[0]);       //從cookie 抓使用者資料並轉物件
                user.innerHTML = userData["data"]["name"] ;
            
                //預定行程內容
                if(result["data"] == null){
                    let booking = document.querySelector(".booking");           //刪除預定的行程
                    let form_connect = document.getElementsByName("form_connect")[0];
                    booking.remove();
                    form_connect .style.display = "none";
                    let noneBooking = document.querySelector(".none_booking");
                    noneBooking.style.display = "block";
                }
            }else{
                alert(result["message"])
            }

        })
    })

