$(document).ready(function(){
    let forms = document.querySelectorAll(".love_post_form") ;

    // love post
    for(let form of forms){
        form.addEventListener('submit',(event_) => {
            event_.preventDefault() ;
            let post_id = form.querySelector("input").value ;
            let span = form.parentNode.parentNode.querySelector("p span") ;
            let love_button_svg = form.querySelector("svg") ;

            $.ajax({
                url: 'love_post/',
                data: ({post_id: post_id}),
                type: 'GET',
                success: function($data, $textStatus, $XMLHttpRequest){
                    if($data != ''){
                        color = "tomato" ;
                        svg_style_text = love_button_svg.querySelector("style").textContent ;
                        svg_style_text = svg_style_text.replace("none", "color") ;
                        svg_style_text = svg_style_text.replace(color, "none") ;
                        svg_style_text = svg_style_text.replace("color", color) ;

                        love_button_svg.querySelector("style").textContent = svg_style_text ;

                        if ($data > 1) {
                            span.textContent = $data + ' personne aiment cet article';
                        }
                        else {
                            span.textContent = $data + ' personne aime cet article';
                        }
                    }
                }
            })
        })
    }

    // comment post
    let comment_forms = document.querySelectorAll(".comment_form") ;

    for(let comment_form of comment_forms){
        comment_form.style.display = "none" ;


        const comment_link = comment_form.parentNode.querySelector("a.comment_link") ;

        if (comment_link != undefined) {
            comment_link.addEventListener('click', (ev) => {
            ev.preventDefault() ;

            link_class_name = comment_link.className ;

            if ( comment_form.style.display == "block") {
                comment_link.style.color = "var(--primary-btn)" ;
                comment_link.textContent = "Commenter" ;
                comment_form.style.display = "none" ;
            }
            else{
                comment_link.style.color = "tomato";
                comment_link.textContent = "Annuler" ;
                comment_form.style.display = "block" ;
                }
            }) ;
        }

        

        function make_comment_removable(delete_button){
        delete_button.addEventListener('click', (ev) => {
                ev.preventDefault() ;

                $.ajax({
                    url: 'remove_comment/',
                    data: {comment_id: delete_button.id},
                    type: 'GET',
                    success: function($data, $textStatus, $XMLHttpRequest){
                        if ($data == "OK") {
                            delete_button.parentNode.remove() ;
                        }
                    }
                }) ;
            }) ;
    }

        // comment
        comment_form.querySelector("form").addEventListener('submit', (ev) => {
            ev.preventDefault() ;

            let url = comment_form.querySelector("form").action ;

            let post_id = comment_form.querySelector("form p input[type='hidden']").value ;
            let comment_content = comment_form.querySelector("form p input[type='text']").value ;

            $.ajax({
                url: url,
                data: {post_id: post_id, comment_content: comment_content},
                type: "GET",
                success: function($data, $textStatus, $XMLHttpRequest){
                    if ($data != ""){
                        let comments = comment_form.parentNode.parentNode.querySelector(".post_comments") ;
                        let comment = document.createElement("p") ;
                        let delete_comment_link = document.createElement("a") ;
                        let span_author = document.createElement("span") ;
                        let br = document.createElement("br")

                        comment.className = "small p-0 mb-2" ;

                        span_author.className = "comment-author" ;

                        author = $data.split(",")[0] ;
                        comment_id = $data.split(",")[1] ;
                        span_author.textContent = author;

                        comment.appendChild(span_author) ;
                        comment.appendChild(br) ;

                        delete_comment_link.href = "#" ;
                        delete_comment_link.className = "remove-comment-btn rounded ms-4 text-end class text-decoration-none" ;
                        delete_comment_link.id = comment_id ;
                        delete_comment_link.href = "#" ;
                        delete_comment_link.textContent = "Supprimer" ;
                        comment.appendChild(document.createTextNode(" " + comment_content)) ;
                        comment.appendChild(delete_comment_link) ;

                        make_comment_removable(delete_comment_link) ;

                        if (comments) {
                            first_comment = comments.querySelector("p + p") ;
                            comments.insertBefore(comment, first_comment) ;
                        }
                        else {
                            new_comment_container = document.createElement("div") ;
                            new_comment_container.className = "post_comments p-2" ;

                            first_para = document.createElement("p") ;
                            first_para.className = "comments-begin small p-0 m-0 text-end" ;

                            first_para.style.color = "var(--primary-btn)" ;

                            first_para.appendChild(document.createTextNode("Commentaire des utilisateurs...")) ;

                            new_comment_container.appendChild(first_para) ;

                            new_comment_container.appendChild(comment) ;

                            comment_form.parentNode.parentNode.appendChild(new_comment_container) ;
                        }

                        comment_form.style.display = "none" ;
                        comment_form.querySelector("#comment").value = "" ;
                        comment_link.textContent = "Commenter" ;
                        comment_link.style.color = "var(--primary-btn)" ;
                    }
                }
            })
        }) ;
    }

    let post_comments = document.querySelectorAll(".post_comments") ;

    for(let comment of post_comments){
        let delete_buttons = comment.querySelectorAll("a") ;

        for(let delete_button of delete_buttons) {
            make_comment_removable(delete_button) ;
        }
    }
}) ;