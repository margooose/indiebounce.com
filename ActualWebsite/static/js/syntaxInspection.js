$("p.Update-"Info-Div"").html(function(index, html) {return "" + (index + 1) + "" + html;}); // https://stackoverflow.com/questions/41384598/jquery-javascript-equivalent-of-css-counter



    function ShowUpdate(update_pk) {



        let update_list = document.querySelectorAll('.Update-Info-Div');

        update_list.forEach(function(update_unique) {
            let update_text = update_unique.textContent;
            console.log(parseInt(update_text));


        });


    };

