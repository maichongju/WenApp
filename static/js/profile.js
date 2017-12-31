function openProfile(evt, item) {
    var i, tabcontent, tablinks;
    tabcontent = document.getElementsByClassName("tabcontent");
    for (i = 0; i < tabcontent.length; i++) {
        tabcontent[i].style.display = "none";
    }
    tablinks = document.getElementsByClassName("tablinks");
    for (i = 0; i < tablinks.length; i++) {
        tablinks[i].className = tablinks[i].className.replace(" active", "");
    }
    document.getElementById(item).style.display = "block";
    evt.currentTarget.className += " active";
}

function updateDefaultTab(Idname) {
    var i,tablinks;
    tablinks = document.getElementsByClassName("tablinks");
    for(i =0; i < tablinks.length; i++){
        console.log(tablinks[i].id);
        tablinks[i].id = "";
    }
    for(i =0; i < tablinks.length; i++){
        if (tablinks[i].value == Idname){
            tablinks[i].id = "defaultOpen";
            break;
        }
    }
    /*tablinks[0].Id = "defaultOpen";*/
}

function updateSuccessPrompt(){
    var msg = document.getElementById("msg_pass_save");
    if (msg != null){
        msg.innerHTML = "Password Saved";
    }
}

function windowOnLoad(Idname){
    switch(Idname){
        case "password":
            
            break;
        case "other":
            break;
        case "main":
            break;
    }

    updateDefaultTab(Idname);
}