//開視窗載入景點資訊
    let currentUrlPath = window.location.pathname;
    let arr = currentUrlPath.split('/');
    let id = arr[2];
    let pictures = "";
    let url ="http://35.76.166.101:3000/api/attraction/" +id;
    fetch(url).then((res) =>{
        return res.json()
    })
    .then((result) =>{
        data = result["data"];
        pictures = data["images"];              //pictures = 景點照片url
        let name = document.querySelector(".name");
        let cateAndMrt = document.querySelector(".cateAndMrt");
        let description = document.querySelector("#description");
        let address = document.querySelector("#address");
        let transport = document.querySelector("#transport");
        let picture_current = document.querySelector(".picture");

        name.innerHTML = data["name"];
        cateAndMrt.innerHTML= data["category"]+" at "+data["mrt"];
        description.innerHTML = data["description"];
        address.innerHTML = data["address"];
        transport.innerHTML = data["transport"];
        picture_current.setAttribute("style", "background-image:url(" + data["images"][0] + ")");
    
        
//pictureRadios、picture處理及監聽事件
        let fragment1 = document.createDocumentFragment();
        let fragment2 = document.createDocumentFragment();
        for(x=0; x<(pictures.length-1); x++){
            let pictureRadioC = pictureRadios[0].cloneNode(true);
            pictureRadioC.value = x+1;
            fragment1.appendChild(pictureRadioC);
            let pictureC = picture_current.cloneNode(true);
            pictureC.setAttribute("style", "background-image:url(" + data["images"][x+1] + ")")
            fragment2.appendChild(pictureC);
        };
        let slide_radio = document.querySelector(".slide_radio");
        slide_radio.appendChild(fragment1);
        let picture_container = document.querySelector(".picture_container");
        picture_container.appendChild(fragment2);
        picture_current.classList.add("active");
        let newPictures = document.querySelectorAll(".picture");
        for(x=0; x<newPictures.length; x++){
            newPictures[x].setAttribute("number",x)         //幫picture加上數字
        }

        //pictureRadios點擊監聽事件
        for(x=0; x<pictureRadios.length; x++){
            pictureRadios[x].addEventListener("click",(e)=>{
                currentPR(e.target)
            })
        }
        currentPictureRadio()               //調動radio checked
    });



//點選pictureRadio切換照片
    function currentPR(self){
        let number = self.value                                              //第幾個radio
        let newPictures = document.querySelectorAll(".picture");
        let newPictureRadios = document.getElementsByName("picture");
        if(newPictureRadios[number].checked = true){
            let pictureActive = document.querySelector(".active");
            pictureActive.classList.remove("active");
            newPictures[number].classList.add("active");
        }
    }

//picture左右鍵切換照片，監聽事件
    let arrow_right = document.querySelector(".arrow_right");
    arrow_right.addEventListener("click",()=>{
        let newPictures = document.querySelectorAll(".picture");
        let pictureActive = document.querySelector(".active");
        let number = Number(pictureActive.getAttribute("number"));          //當前顯示畫面的照片號碼
        number = number +1;
        if(number >= newPictures.length){
            number = 0;
        };
        pictureActive.classList.remove("active");
        newPictures[number].classList.add("active");

        //同步切換radio
        let newPictureRadios = document.getElementsByName("picture");
        newPictureRadios[number].checked = true;

    });

    let arrow_left = document.querySelector(".arrow_left");
    arrow_left.addEventListener("click",()=>{
        let newPictures = document.querySelectorAll(".picture");
        let pictureActive = document.querySelector(".active");
        let number = Number(pictureActive.getAttribute("number"));          //當前顯示畫面的照片號碼
        number = number -1;
        if(number < 0){
            number = (newPictures.length)-1;
        };
        pictureActive.classList.remove("active");
        newPictures[number].classList.add("active");

        //同步切換radio
        let newPictureRadios = document.getElementsByName("picture");
        newPictureRadios[number].checked = true;
    });

//所有radio預設
    let timeRadios = document.getElementsByName("time");
    let morning = document.querySelector(".morning");
    let afternoon = document.querySelector(".afternoon");
    let pictureRadios = document.getElementsByName("picture");
    function currentPictureRadio(){
        //pictureRadio
        pictureRadios[0].checked = true ;
        pictureRadios[0].value = 0;
        //timeRadio
        timeRadios[0].checked = true; 
        morning.setAttribute("style","display:block");
    };

//timeRadio監聽事件 + 切換價格
    timeRadios[0].addEventListener("click",(e)=>{
        if(timeRadios[0].checked = true){
            morning.setAttribute("style","display:block");
            afternoon.setAttribute("style","display:none");
        }
    });
    timeRadios[1].addEventListener("click",(e)=>{
        if(timeRadios[1].checked = true){
            morning.setAttribute("style","display:none");
            afternoon.setAttribute("style","display:block");
        }
    });

//預定行程
    let journey = document.querySelector(".button");
    journey.addEventListener("click",() =>{
        let login_token = (document.cookie).indexOf("login_token");
        console.log(login_token )
        if(login_token == -1){
            signOpen()
            return
        }
        else{
            let url = "http://35.76.166.101:3000/api/booking";

            let id = location.href.split("/")[4].split("?")[0];
            let date = document.getElementById("date").value;
            let price = "";
            let timeRadios = document.getElementsByName("time");
            for (x=0; x<2; x++){
                if (timeRadios[x].checked){
                    if(x == 0){
                        price = 2000
                    }else{
                        price = 2500
                    }
                }
            }
            fetch(url, {
                method:"POST",
                body: JSON.stringify({
                    "id" : id,
                    "date" : date,
                    "price" : price
                }),
                credentials: "include",
                cache:"no-cache",
                headers: new Headers({
                    "Content-Type":"application/json; charset=UTF-8",
                }),
            })
            .then(res =>{
                res = res.json();
                return res
            })
            .then(result =>{
                if(result["ok"] == true){
                    alert("預定成功，稍後請至 *預定行程* 頁面付款")
                }else if(result["message"] == "尚未登入帳號"){
                    signOpen()
                }else{
                    alert(result["message"])
                }
            })
        }
        
    })