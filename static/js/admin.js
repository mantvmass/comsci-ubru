function delete_hint() {
    Swal.fire({
        title: 'Are you sure?',
        text: "You won't be able to revert this!",
        icon: 'warning',
        showCancelButton: true,
        confirmButtonColor: '#3085d6',
        cancelButtonColor: '#d33',
        confirmButtonText: 'Yes, delete it!'
      }).then((result) => {
            if (result.isConfirmed) {
                $.ajax({  
                    method: 'POST',
                    url: '/delete_hint', 
                    success: function(response) {
                        if (response == "success"){
                            window.location.href = "/manage"
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
        }
    )
}

function edit_hint() {
    Swal.fire({
        title: 'Update Hint',
        html: `<input type="text" id="hint_update" class="swal2-input" placeholder="">`,
        confirmButtonText: 'Update',
        focusConfirm: false,
        preConfirm: () => {
            const hint = Swal.getPopup().querySelector('#hint_update').value
            if (!hint) {
                Swal.showValidationMessage(`Please enter hint`)
            }
            return { hint: hint }
        }
      }).then((result) => {
        var up_hint = result.value.hint 
        if (result.isConfirmed) {
            Swal.fire({
                title: 'Do you want to save the changes?',
                showDenyButton: true,
                confirmButtonText: 'Save',
                denyButtonText: `Don't save`,
              }).then((result) => {
                /* Read more about isConfirmed, isDenied below */
                if (result.isConfirmed) {
                    $.ajax({  
                        method: 'POST',
                        url: '/edit_hint',
                        data: { hint: up_hint },
                        success: function(response) {
                            if (response == "success"){
                                window.location.href = "/manage"
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
              }
            )
       }
    })
}