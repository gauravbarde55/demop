async function populateFeeTypes() {
    const response = await fetch('/fees_types');
    const fee_types = await response.json();
    const feeTypeSelect = document.getElementById('fees_types');
    fee_types.forEach(fees_types => { //////////////////////// courses_types is textbox id
        const option = document.createElement('option');
        option.value = fees_types.id;
        option.textContent = fees_types.fees_name;
        feeTypeSelect.appendChild(option);
    });
}
populateFeeTypes();

async function updateFeesNames() {
    const fees_types = document.getElementById('fees_types').value;
    const response = await fetch(`/fees_names?fees_types=${fees_types}`);
    const coursenamess = await response.json();
    console.log('course names');
    console.log(coursenamess);
    // document.getElementById('fees_amt').innerHTML = '';
    // document.getElementById('fees_amt').innerHTML = coursenamess[2] || 0;
    // document.getElementById('total_amt').innerHTML = '';
    // document.getElementById('total_amt').innerHTML = coursenamess[2] || 0;
    // document.getElementById('amount').value = '';
    // document.getElementById('amount').value = coursenamess[2];

    document.getElementById('fees_amt').value = '';
    document.getElementById('fees_amt').value = coursenamess[2] || 0;
    document.getElementById('total_amt').value = '';
    document.getElementById('total_amt').value = coursenamess[2] || 0;
    document.getElementById('amount').value = '';
    document.getElementById('amount').value = coursenamess[2] || 0;


    enableFeesPaymentBtn(fees_types)
    // const courseNameSelect = document.getElementById('courses_names');
    // courseNameSelect.innerHTML = '<option value="">Select Course Name</option>'; // Clear existing options
    // coursenamess.forEach(courses_names => {   ////////////////////// TextBox Field ID
    //     const option = document.createElement('option');
    //     option.value = courses_names.course_name_id;
    //     option.textContent = courses_names.course_name;
    //     courseNameSelect.appendChild(option);
    // });

}

async function enableFeesPaymentBtn(fees_types) {
    console.log('fees_types');
    console.log(fees_types);
    if(fees_types>0){
        const paymentBtn = document.getElementById('payment_btn');
        paymentBtn.classList.remove('disabled');
        paymentBtn.disabled = false; // Enable submit button
        // document.getElementById("payment_btn").style.backgroundColor = "orange";

        // const paymentBtn = document.getElementById('payment_btn');
        // paymentBtn.classList.add('disabled');
        // paymentBtn.disabled = true; // Enable submit button
    }
    else{
        const paymentBtn = document.getElementById('payment_btn');
        paymentBtn.classList.add('disabled');
        paymentBtn.disabled = true; // Enable submit button
        // document.body.style.background = color;
        // document.getElementById("payment_btn").style.backgroundColor = "grey";
    }
// if((fname_trim_val.length > 0) && (lname_trim_val.length > 0) && (email_trim_val.length > 0) && (num_verify_val=='1') && (city_val != '-1') && (qual_val != '-1') && (ctype_val != '-1') && (cname_val != '-1')){
//     console.log("if Condition Satisfied");
//     const submitBtn = document.getElementById('submitBtn');
//     submitBtn.classList.remove('disabled');
//     submitBtn.disabled = false; // Enable submit button

//     // hideEnquiryFormPopup();
//     document.getElementById('otpPopup').style.display = 'none'; //// Close OTP Popup
// }
}
enableFeesPaymentBtn()

async function verify_coupon(){
    console.log('hsdgdg');
    const coupon_code = document.getElementById('coupon_code').value;
    console.log('coupon_code 1')
    console.log(coupon_code)
    // const response = await fetch(`/verify_coupon?coupon_code=${coupon_code}`);
    // const couponCodes = await response.json();
    // console.log('Coupon Code');
    // console.log(couponCodes);
}