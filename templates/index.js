//開式窗載入景點
    let Bob = document.querySelector(".Bob");
    let ob = document.querySelector(".ob");
    let obs = document.querySelectorAll(".ob");
    let tit = document.querySelectorAll(".tit");
    let det1 = document.querySelectorAll(".det1");
    let det2 = document.querySelectorAll(".det2");
    let obin = document.querySelectorAll(".obin");
    let url =  "http://35.76.166.101:3000/api/attractions?page=";
    let nextPage = null;
    fetch(url).then(function (response){         
        return response.json()           
    }).then(function (result){
        let data =  result["data"];              //data = 陣列，12筆景點資料
        for (n=0;n<12;n++){
            tit[n].textContent = data[n]["name"];
            det1[n].textContent = data[n]["mrt"];
            det2[n].textContent = data[n]["category"];
            obin[n].setAttribute("style", "background-image:url(" + data[n]["images"][0] + ")");
            obs[n].setAttribute("id",data[n]["id"])
        };
        nextPage = result["nextPage"];
    })
    //景點分類(menu)
    let url_cate = "http://35.76.166.101:3000/api/categories";
    fetch(url_cate).then((response) =>{
        return response.json()
    })
    .then((result) =>{
        let data = result["data"]
        cateLength = data.length;
        let cate = document.querySelector(".cate");
        let fragmentCate = document.createDocumentFragment();
        for(x=1; x<(cateLength); x++){
            let cateC = cate.cloneNode(false);
            cateC.textContent = data[x]
            fragmentCate.appendChild(cateC);
        };
        let menuIndex = fragmentCate
        let menu = document.querySelector(".menu");
        menu.appendChild(menuIndex);
        firstCate = document.querySelector(".cate");
        firstCate.textContent = data[0];
    })



//下拉載入
    //debounce
    function debounce(func, delay=400) {
        let timer = null;
        
        return () => {
            let context = this;
            let args = arguments;
        
            clearTimeout(timer);
            timer = setTimeout(() => {
            func.apply(context, args);
            }, delay)
        }
    };
    window.addEventListener('scroll', debounce(scroll));
    
    //載入函式
    function scroll(){
        if (nextPage === null){
            window.removeEventListener('scroll', debounce(scroll));
            return nextPage
        }; 
        let url =  "http://35.76.166.101:3000/api/attractions?page=";
        let { scrollTop, scrollHeight, clientHeight } = document.documentElement

        if (scrollTop + clientHeight >= scrollHeight - 5) {
            if (input.value == null){
                url = url +nextPage;
            }else{
                let value ="&keyword="+(input.value);
                url = url +nextPage+value;
            }
        fetch(url).then(function (response){         
            return response.json()        
        })
        .then(function (result){
            let data =  result["data"];              //data = 新陣列
            let length = data.length;
            let turns = Math.ceil(length/4);
            let attraction = document.querySelector(".attraction");
            let newdiv = null;
            let len = 4 ;
            for(i=0; i<turns; i++){
                let fragment1 = document.createDocumentFragment();
                if((length-4)<0){
                    len = length
                }
                for (x=0;x<len;x++){ 
                    let obClone = ob.cloneNode(true);                           
                    fragment1.appendChild(obClone);
                };
                let obsC = fragment1.querySelectorAll(".ob");
                let titC= fragment1.querySelectorAll(".tit");                           
                let det1C = fragment1.querySelectorAll(".det1");
                let det2C = fragment1.querySelectorAll(".det2");
                let obinC = fragment1.querySelectorAll(".obin");
                for(n=0;n<len;n++){
                    titC[n].textContent = data[(i*4)+n]["name"];                           
                    det1C[n].innerHTML = data[(i*4)+n]["mrt"];
                    det2C[n].innerHTML = data[(i*4)+n]["category"];   
                    obinC[n].setAttribute("style", "background-image:url(" + data[(i*4)+n]["images"][0] + ")");
                    obsC[n].setAttribute("id",data[(i*4)+n]["id"]);
                };
                newdiv =  fragment1;
                let BobClone = Bob.cloneNode(false);
                BobClone.appendChild(newdiv);
                attraction.appendChild(BobClone);
                length = length - 4;
            };
            nextPage = result["nextPage"];
            if (nextPage === null){
            let finish = document.querySelector(".finish");
            finish.style = "display:block";
            } 
        })};
    }

//點擊搜尋

    //關閉迴車監聽
    document.querySelector('form').addEventListener('submit',function(e){e.preventDefault()});

    //點擊搜尋
    let btn = document.getElementById("btn");
    let input = document.querySelector(".input")
    btn.addEventListener("click", () =>{
        let url1 =  "http://35.76.166.101:3000/api/attractions?page=&keyword=";
        let value =input.value;
        url = url1+value;
        fetch(url).then(function (response){       
                return response.json()        
        })
        .then(function (result){
            if (result["nextPage"] === null){
                let finish = document.querySelector(".finish");
                finish.style = "display:block; flex:1";
            };
            let BobClone = Bob.cloneNode(false);
            let fragment2 = document.createDocumentFragment();
            fragment2.appendChild(BobClone);
            let obClone = ob.cloneNode(true);
            fragment2.appendChild(obClone);                     

            //清空attraction
            let attraction = document.querySelector(".attraction");
            let AllBob = document.querySelectorAll(".Bob");
            let AllBoblen = AllBob.length;
            for(x=0;x<AllBoblen;x++){
                attraction.removeChild(AllBob[x]);
            };
            
            //清空fragment
            let resetBob = fragment2.querySelector(".Bob");
            let resetob = fragment2.querySelector(".ob");
            newBob = resetBob;
            newob = resetob;
            fragment2.removeChild(resetBob);
            fragment2.removeChild(resetob);

            let data =  result["data"];
            let length = data.length;
            let turns = Math.ceil(length/4);
            let newdiv = null;
            let len = 4 ;
            for(i=0; i<turns; i++){
                let fragment1 = document.createDocumentFragment();
                if((length-4)<0){
                    len = length
                }
                for (x=0;x<len;x++){ 
                    let obClone = newob.cloneNode(true);                           
                    fragment1.appendChild(obClone);
                };
                let obsC = fragment1.querySelectorAll(".ob");
                let titC= fragment1.querySelectorAll(".tit");                           
                let det1C = fragment1.querySelectorAll(".det1");
                let det2C = fragment1.querySelectorAll(".det2");
                let obinC = fragment1.querySelectorAll(".obin");
                for(n=0;n<len;n++){
                    titC[n].textContent = data[(i*4)+n]["name"];                           
                    det1C[n].innerHTML = data[(i*4)+n]["mrt"];
                    det2C[n].innerHTML = data[(i*4)+n]["category"];   
                    obinC[n].setAttribute("style", "background-image:url(" + data[(i*4)+n]["images"][0] + ")");
                    obsC[n].setAttribute("id",data[(i*4)+n]["id"]);
                };
                newdiv =  fragment1;
                let BobClone = newBob.cloneNode(false);
                BobClone.appendChild(newdiv);
                attraction.appendChild(BobClone);
                length = length - 4;
            };
            nextPage = result["nextPage"];
        });
    });
    
//景點分類關鍵字填入
    //點擊輸入框跳出選單
    document.addEventListener('click',function openMenu(e){
        let menuOpen = document.querySelector(".menu_open");
        let menu = document.querySelector(".menu");
        let cate = document.querySelectorAll(".cate");
        //打開menu
        if (e.target == input){                
            menuOpen.style = "display : block";
        }else if(e.target == menu){
            menuOpen.style = "display : block";
        }else if(e.target == cate){
            menuOpen.style = "display : block";
        }else{
            menuOpen.style = "display : none";
        }            
    })
    
    //填入景點分類至搜尋框
    function putOn(cate){
        input.value = cate
    }


//點擊圖片跳轉
    function turnPage(){
        window.addEventListener("click",function (event){
            let path = event.path;      //array
            let choseditem = event.target;
            let obChose ="";
            if (choseditem.className == "obin"){
                obChose = path[1];
            }else if(choseditem.className == "tit"){
                obChose = path[3];
            }else{
                obChose = path[2];
            };
            let id = obChose.id;
            if(id ==""){
                return none
            }else{
                window.location.href = "http://35.76.166.101:3000/attraction/" + id
            }
        })
    };



   