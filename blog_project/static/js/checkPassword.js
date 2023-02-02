function checkPassword() {
    console.log("jianchap");
    var password = document.getElementById("id_password").value;
    var repassword = document.getElementById("repaw").value;
    // console.log(document.getElementById("id_password"));
    if(password === repassword) {
        // document.getElementById("alert").innerHTML="<br><font color='green'>两次密码输入一致</font>";
        // document.getElementById("alert").innerHTML="<p style='color: green;margin: auto'>两次密码输入一致</p>";
        document.getElementById("alert").innerHTML="<i class=\"fa fa-circle-check\" style='color: green'></i>";
        document.getElementById("submit").disabled = false;

    }else{
        document.getElementById("alert").innerHTML="<i class=\"fa fa-xmark\" style='color: red;'></i><p style='margin: auto;color: red;font-size: x-small;position: center'>两次密码输入不一致</p>";
        document.getElementById("submit").disabled = true;
    }
};