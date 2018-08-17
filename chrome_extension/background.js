if (document.title == "Amazon.com Shopping Cart") {

   var total = document.getElementsByClassName('a-size-medium a-color-price sc-price sc-white-space-nowrap sc-price-sign')[0].innerHTML;
   // total = total.getElementsByClassName('a-spacing-none a-spacing-top-mini')[0];
   // total = total.getElementsByClassName('a-color-price a-text-bold')[0].innerHTML;
   total = total.replace(/\s/g,'');
   total = total.substr(-2);
   if (total != 0) {
      total = 100 - Number(total);
   }

   if (total<10&&total!=0) {
      total = 0 + String(total);
   }

   var modalTop = document.createElement("div");
   modalTop.setAttribute("id", "modal");
   modalTop.setAttribute("class", "modal");

   var modalMid = document.createElement("div");
   modalMid.setAttribute("id", "modal-content");
   modalMid.setAttribute("class", "modal-content");

   var span = document.createElement("span");
   span.setAttribute("id", "close");
   span.setAttribute("class", "close");

   var css = 'close:hover,close:focus {color: black; text-decoration: none; cursor: pointer;}';
   var style = document.createElement('Style');
   style.appendChild(document.createTextNode(css));

   var para = document.createElement("p");
   var text = document.createTextNode("+0."+total);
   para.appendChild(text);
   para.setAttribute("Style", "color:#25ba27; font-weight:bold; font-size:100px; padding-top:50px;");

   var para2 = document.createElement("p");
   var text2 = document.createTextNode("To your Charity account!");
   para2.appendChild(text2);
   para2.setAttribute("Style", "color:#25ba27; font-size:15px; padding-top:25px;");

   modalMid.appendChild(span);
   modalMid.appendChild(para);
   modalMid.appendChild(para2);
   modalTop.appendChild(modalMid);

   var topNav = document.getElementById("nav-AssociateStripe");
   topNav.insertBefore(modalTop, topNav.childNodes[0]);

   var pic = chrome.runtime.getURL('coins.png');

   document.getElementById("modal").setAttribute("Style", "display:block; position:fixed; z-index:1; left:0; top:0; width:100%; height:100%; overflow:auto; background-color:rgb(0,0,0); background-color:rgba(0,0,0,0.4);");
   document.getElementById("modal-content").setAttribute("Style", "text-align:center; height:500px; color:#25ba27; background-color:#fefefe; margin:15% auto; padding:20px; border:1px solid #888; width:30%; background-image:url('chrome-extension://gdcgcmkejocjbkjeeidinoiijhjkohbd/coins.png');");
   document.getElementById("close").setAttribute("Style", "color: #aaa; float:right; font-size:28px; font-weight:bold;");
   document.getElementById("modal").appendChild(style);

   window.onclick = function(event) {
       if (event.target == modalTop) {
           modalTop.style.display = "none";
       }
    }
}
