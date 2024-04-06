function triggerFeedbackMessages(message) {


    switch (message.category) {
        case "register": popupFeedback(); break;
        case "login": mixinFeedback(); break;
        case "logout": mixinFeedback(); break;
        case "create_list": {
            message["title"] = message.text;
            message["text"] = "List successfully created!";
            popupFeedback(); break;
        }
    }

    function popupFeedback() {
        var options = {
            text: message.text,
            icon: message.icon,
            timer: 3000,
        }

        if (message.title)
            options.title = message.title;

        Swal.fire(options);
    }

    function mixinFeedback() {
        Swal.mixin({
            toast: true,
            position: "top",
            showConfirmButton: false,
            timer: 3000,
            timerProgressBar: true,
            didOpen: (toast) => {
                toast.onmouseenter = Swal.stopTimer;
                toast.onmouseleave = Swal.resumeTimer;
            },
        }).fire({
            title: message.text,
            icon: message.icon,
            customClass: "animate__animated",
            showClass: {
                popup: "animate__bounceInDown"
            },
            hideClass: {
                popup: "animate__bounceOutUp"
            },
        });
    }
}

function deleteListConfirmation() {
    document.activeElement.blur();
    return Swal.fire({
        title: "Are you sure you want to delete this list?",
        text: "You won't be able to revert this!",
        icon: "warning",
        showCancelButton: true,
        cancelButtonColor: "#3085d6",
        confirmButtonColor: "#d33",
        confirmButtonText: "Yes, delete it!"
    });
}