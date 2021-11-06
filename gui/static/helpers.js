function copyToClipboard() {
    var copyText = getDivText();


    navigator.clipboard.writeText(copyText);

    var tooltip = document.getElementById("myTooltip");
    tooltip.innerHTML = "Copied: " + copyText;
}

function outFunc() {
    var tooltip = document.getElementById("myTooltip");
    tooltip.innerHTML = "Copy to clipboard";
}

function getDivText() {
    var mytext;
    $(document).ready(function() {
        $('#mybtntext').click(function() {
            mytext = $('.commandBox').text();
        });
    });
    return "lel";
}


function collapseDiv() {
    var coll = document.getElementsByClassName("navbar");
    var i;

    for (i = 0; i < coll.length; i++) {
        coll[i].addEventListener("click", function() {
            this.classList.toggle("active");
            var content = this.nextElementSibling;
            if (content.style.display === "block") {
                content.style.display = "none";
            } else {
                content.style.display = "block";
            }
        });
    }
}


$(function() {

    // jQuery selection for the 2 select boxes
    var dropdown = {
        exe: $('#select_exe'),
        machine: $('#select_machine')
    };

    // call to update on load
    updateMachine();

    // function to updateMachine XHR and update exe dropdown
    function updateMachine() {
        url = window.location.pathname
        console.log(url)
        if (url == "/build") {
            var send = {
                executable: dropdown.exe.val()
            };
            dropdown.machine.attr('disabled', 'disabled');
            dropdown.machine.empty();
            $.getJSON("/_get_choices", send, function(data) {
                data.forEach(function(item) {
                    console.log(item)
                    dropdown.machine.append(
                        $('<option>', {
                            value: item[0],
                            text: item[1]
                        })
                    );
                });
                dropdown.machine.removeAttr('disabled');
            });
        }
    }

    // event listener to state dropdown change
    dropdown.exe.on('change', function() {
        updateMachine();
    });

});