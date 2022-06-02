async function send_sub() {

    let inputValue = document.getElementById("allow_token").value;

    const { value: fullname } = await Swal.fire({
        input: 'text',
        inputLabel: 'ชื่อเต็ม',
        inputPlaceholder: 'Ex: นพรัตน์ บุญทวี',
        confirmButtonText: 'Next'
    })
    const { value: nickname } = await Swal.fire({
        input: 'text',
        inputLabel: 'ชื่อเล่น',
        inputPlaceholder: 'Ex: นาย',
        confirmButtonText: 'Next'
    })
    const { value: facebook_url } = await Swal.fire({
        input: 'url',
        inputLabel: 'ลิงค์เฟสบุ๊ค',
        inputPlaceholder: 'Ex: https://facebook.com/me',
        confirmButtonText: 'Next'
    })
    const { value: file } = await Swal.fire({
        title: 'Select image',
        input: 'file',
        confirmButtonText: 'Next',
        inputAttributes: {
            'accept': 'image/*',
            'aria-label': 'Upload your profile picture'
        }
        })
        
        if (file) {
        const reader = new FileReader()
        reader.onload = (e) => {
            Swal.fire({
            title: 'ตรวจสอบความถูกต้อง',
            imageUrl: e.target.result,
            html: `
                <h4>ชื่อเต็ม: ${fullname}</h4>
                <h4>ชื่อเล่น: ${fullname}</h4>
                <h4>ลิงค์เฟสบุ๊ค: ${facebook_url}</h4>
            `,
            showCancelButton: true,
            confirmButtonColor: '#3085d6',
            cancelButtonColor: '#d33',
            confirmButtonText: 'Send'
            }).then((result) => {
                console.log(inputValue)
                console.log(e.target.result)
            })
        }
        reader.readAsDataURL(file)
    }
}