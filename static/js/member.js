// signin function
function signin() {
    Swal.fire({
        title: 'SignIn Form',
        html: `
            <input type="text" id="username" class="swal2-input" placeholder="Username">
            <input type="password" id="password" class="swal2-input" placeholder="Password">
            `,
        confirmButtonText: 'Submit',
        focusConfirm: false,
        preConfirm: () => {
            const username = Swal.getPopup().querySelector('#username').value
            const password = Swal.getPopup().querySelector('#password').value
            if (!username || !password) {  Swal.showValidationMessage(`Please enter username and password`) }
            return { username: username, password: password }
        }
        }).then((result) => {
            $.ajax({  
                method: 'POST',
                url: '/signin', 
                data: { username: result.value.username, password: result.value.password },
                success: function(response) {
                    if (response == "success"){
                        let timerInterval
                        Swal.fire({
                            title: 'Redirect',
                            icon: 'success',
                            html: 'จะเปลี่ยนเส็นทางในอีก <b></b>.',
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
                            title: 'เกิดข้อผิดพลาด!',
                            text: response,
                            icon: 'warning',
                            confirmButtonText: 'ตกลง'
                        })
                    }
                },
                error: function(response){
                    Swal.fire({
                        title: 'เกิดข้อผิดพลาด!',
                        text: 'เกิดข้อผิดพลาดกรุณาลองใหม่อีกครั้งในภายหลัง!',
                        icon: 'error',
                        confirmButtonText: 'ตกลง'
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
            <input type="text" id="username" class="swal2-input" placeholder="Username">
            <input type="email" id="email" class="swal2-input" placeholder="Email">
            <input type="password" id="password" class="swal2-input" placeholder="Password">
            <input type="password" id="key" class="swal2-input" placeholder="Key">
            `,
        confirmButtonText: 'Submit',
        focusConfirm: false,
        preConfirm: () => {
            const username = Swal.getPopup().querySelector('#username').value
            const email = Swal.getPopup().querySelector('#email').value
            const password = Swal.getPopup().querySelector('#password').value
            const key = Swal.getPopup().querySelector('#key').value
            if (!username || !password || !email || !key) { Swal.showValidationMessage(`Please compleate the infomation`) }
            // if (password != re_password) { Swal.showValidationMessage(`Incorrect password`) }
            return { username: username, email: email, password: password, key: key }}
        }).then((result) => {
            $.ajax({  
                method: 'POST',
                url: '/signup', 
                data: { username: result.value.username, email: result.value.email, password: result.value.password, key: result.value.key },
                success: function(response) {
                    if (response == "success"){
                        Swal.fire({
                            title: 'Success',
                            icon: 'success',
                            confirmButtonText: 'ตกลง'}
                        )
                    } else {
                        Swal.fire({
                            title: 'เกิดข้อผิดพลาด!',
                            text: response,
                            icon: 'warning',
                            confirmButtonText: 'ตกลง'}
                        )
                    }
                },
                error: function(response){
                    Swal.fire({
                        title: 'เกิดข้อผิดพลาด!',
                        text: 'เกิดข้อผิดพลาดกรุณาลองใหม่อีกครั้งในภายหลัง!',
                        icon: 'error',
                        confirmButtonText: 'ตกลง'}
                    )
                }
            })
        }
    )
}
// end signup function