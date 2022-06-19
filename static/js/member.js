// signin function
function signin() {
    Swal.fire({
        title: 'SignIn Form',
        html: `
            <input type="email" id="email" class="swal2-input" placeholder="Email">
            <input type="password" id="password" class="swal2-input" placeholder="Password">
            `,
        confirmButtonText: 'Submit',
        focusConfirm: false,
        preConfirm: () => {
            const email = Swal.getPopup().querySelector('#email').value
            const password = Swal.getPopup().querySelector('#password').value
            if (!email || !password) {  Swal.showValidationMessage(`Please enter email and password`) }
            return { email: email, password: password }
        }
        }).then((result) => {
            $.ajax({  
                method: 'POST',
                url: '/signin', 
                data: { email: result.value.email, password: result.value.password },
                success: function(response) {
                    if (response == "success"){
                        let timerInterval
                        Swal.fire({
                            title: 'Success',
                            icon: 'success',
                            html: 'Will redirect in <b></b> milliseconds.',
                            timer: 4000,
                            timerProgressBar: true,
                            didOpen: () => {
                                Swal.showLoading()
                                const b = Swal.getHtmlContainer().querySelector('b')
                                timerInterval = setInterval(() => {
                                b.textContent = Swal.getTimerLeft()
                                }, 100)
                            },
                            willClose: () => { clearInterval(timerInterval) }
                            }).then((result) => {
                            /* Read more about handling dismissals below */
                            if (result.dismiss === Swal.DismissReason.timer) {
                                // console.log('I was closed by the timer')
                                window.location.href = "/dashboard"
                            }
                        })
                    } else {
                        Swal.fire({
                            title: 'An error occurred!',
                            text: response,
                            icon: 'warning',
                            confirmButtonText: 'Ok'
                        })
                    }
                },
                error: function(response){
                    Swal.fire({
                        title: 'An error occurred!',
                        text: 'Please try again later.',
                        icon: 'error',
                        confirmButtonText: 'Ok'
                    })
                }
            })
        }
    )
}
// end signin function

// signup function
function signup() {
    Swal.fire({
        title: 'SignUp Form',
        html: `
            <input type="text" id="fullname" class="swal2-input" placeholder="Full Name">
            <input type="email" id="email" class="swal2-input" placeholder="Email">
            <input type="password" id="password" class="swal2-input" placeholder="Password">
            <input type="password" id="key" class="swal2-input" placeholder="Key">
            `,
        confirmButtonText: 'Submit',
        focusConfirm: false,
        preConfirm: () => {
            const fullname = Swal.getPopup().querySelector('#fullname').value
            const email = Swal.getPopup().querySelector('#email').value
            const password = Swal.getPopup().querySelector('#password').value
            const key = Swal.getPopup().querySelector('#key').value
            if (!fullname || !password || !email || !key) { Swal.showValidationMessage(`Please compleate the infomation`) }
            // if (password != re_password) { Swal.showValidationMessage(`Incorrect password`) }
            return { fullname: fullname, email: email, password: password, key: key }}
        }).then((result) => {
            $.ajax({  
                method: 'POST',
                url: '/signup', 
                data: { fullname: result.value.fullname, email: result.value.email, password: result.value.password, key: result.value.key },
                success: function(response) {
                    if (response == "success"){
                        Swal.fire({
                            title: 'Success',
                            icon: 'success',
                            confirmButtonText: 'Ok'}
                        )
                    } else {
                        Swal.fire({
                            title: 'An error occurred!',
                            text: response,
                            icon: 'warning',
                            confirmButtonText: 'Ok'}
                        )
                    }
                },
                error: function(response){
                    Swal.fire({
                        title: 'An error occurred!',
                        text: 'Please try again later.',
                        icon: 'error',
                        confirmButtonText: 'Ok'}
                    )
                }
            })
        }
    )
}
// end signup function