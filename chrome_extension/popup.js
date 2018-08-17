// $(function(){
//     $.ajax({
//         url: "https://request-redirect.herokuapp.com/data",
//         dataType: "json",
//         success: (data) => {
//             console.log(data);
//             var balance = data["balance"];
//             console.log(balance);
//             if (balance != undefined) {
//                 console.log(balance);
//                 console.log($("#balance"));
//                 console.log(document.getElementById("balance"));
//                 console.log(document.body);
//                 $("#balance").html(balance);
//             }
//             $("#charity").html(data["charity"]);
//         }
//     });
// });

window.onload = () => {
    var balance = document.getElementById("balance");
    var charity = document.getElementById("charity");

    var xmlHttp = new XMLHttpRequest();
    xmlHttp.open(
        "GET",
        "https://request-redirect.herokuapp.com/data",
        false
    );
    xmlHttp.send( null );
    var response = xmlHttp.responseText

    var obj = JSON.parse(response);

    if (obj["balance"] != undefined) {
        balance.innerHTML = obj["balance"];
    }

    if (obj["charity"] != undefined) {
        charity.innerHTML = obj["charity"];
    }
};
