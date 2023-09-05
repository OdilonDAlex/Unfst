$(document).ready(function(){

    all_input_who_need_js = ["#id_username", "#id_last_name", "#id_first_name", "#id_password"] ;

    $(".helptext").addClass(" small") ;
    $(".helptext").css("color",  "var(--primary-btn)") ;

    for(let input_ of all_input_who_need_js){
        let label_ = $(input_).parent().children("label") ;
        let labelText = label_.text() ;
        labelText = labelText.slice(0, labelText.length - 2) ;
        label_.text(labelText) ;
        console.log(labelText) ;
        console.log(label_) ;

        let copy_of_label = label_.clone() ;

        label_.remove() ;

        $(input_).parent().addClass("form-floating") ;
        $(input_).addClass("form-control form-control-sm") ;
        $(input_).attr("placeholder", labelText) ;
        $(input_).css("background-color", "var(--primary-bg)");
        $(input_).css("color", "var(--secondary-btn)");

        copy_of_label.insertAfter($(input_)) ;

        $(".errorlist").css("color", "tomato");
    }

})