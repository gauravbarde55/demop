
// async function updateStates() {
//     const country = document.getElementById('country').value;
//     const response = await fetch(`/states?country=${country}`);
//     const states = await response.json();
//     const stateSelect = document.getElementById('state');
//     stateSelect.innerHTML = '<option value="">Select State</option>'; // Clear existing options
//     states.forEach(state => {
//         const option = document.createElement('option');
//         option.value = state;
//         option.textContent = state;
//         stateSelect.appendChild(option);
//     });

// }

async function updateCourseNames() {
    const courses_types = document.getElementById('courses_types').value;
    const response = await fetch(`/course_names?courses_types=${courses_types}`);
    const coursenamess = await response.json();
    const courseNameSelect = document.getElementById('courses_names');
    courseNameSelect.innerHTML = '<option value="">Select Course Name</option>'; // Clear existing options
    coursenamess.forEach(courses_names => {   ////////////////////// TextBox Field ID
        const option = document.createElement('option');
        option.value = courses_names.course_name_id;
        option.textContent = courses_names.course_name;
        courseNameSelect.appendChild(option);
    });

}


    function showOtpPopup() {
        document.getElementById('otpPopup').style.display = 'flex';
    }

    function enableOTPButton() {
        console.log('Enable Submit Button Called');
        const otpBtn = document.getElementById('otpbtn');
        otpBtn.classList.remove('disabled');
        otpBtn.disabled = false; // Enable submit button
        // document.getElementById('otpPopup').style.display = 'none'; //// Close OTP Popup
    }
    function disableOTPButton() {
        //Enable
        // $('#otpbtn').prop('disabled', false)

        // Get a reference to the button element
        const button = document.getElementById("otpbtn");

        // Disable the button
        button.disabled = true;

        // console.log('Enable Submit Button Called');
        // const otpBtn = document.getElementById('otpbtn');
        // otpBtn.classList.add('disabled');
        // otpBtn.disabled = true; // Enable submit button
        // // document.getElementById('otpPopup').style.display = 'none'; //// Close OTP Popup
    }

    function sendOtp() {
        document.getElementById('otpMessage').textContent = '';
        const mobile = document.getElementById('mobile').value;
        fetch('/send_otp', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ mobile })
        })
        .then(response => response.json())
        .then(data => {
            if (data.success) {
                showOtpPopup();
            } else {
                alert('Failed to send OTP. Please try again.');
            }
        });
    }

    /////////////////////////////
    function resendOtp() {
        const mobile = document.getElementById('mobile').value;
        fetch('/send_otp', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ mobile })
        })
        .then(response => response.json())
        .then(data => {
            if (data.success) {
                document.getElementById('otpMessage').textContent = 'OTP resent successfully!';
            } else {
                document.getElementById('otpMessage').textContent = 'Failed to resend OTP. Please try again.';
            }
        });
    }

    function showOtpSection() {
        document.getElementById('otpSection').classList.remove('hidden');
    }

    /////////////////////////////
    function verifyOtp() {
        const otp = [
            document.getElementById('otp1').value,
            document.getElementById('otp2').value,
            document.getElementById('otp3').value,
            document.getElementById('otp4').value
        ].join('');

        const mobile = document.getElementById('mobile').value;

        fetch('/verify_otp', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ otp, mobile })
        })
        .then(response => response.json())
        .then(data => {
            const messageElement = document.getElementById('otpMessage');
            if (data.success) {
                // messageElement.textContent = 'OTP Verified Successfully!';
                // enableSubmitButton(); // Enable submit button after successful OTP
                // document.getElementById('form').submit();
                setTimeout(() => {
                    messageElement.textContent = 'OTP Verified Successfully!';
                }, 3000); // Submit form after 3 second
                // setTimeout(() => {
                //     document.getElementById('form').submit();
                // }, 1000); // Submit form after 1 second
                clearOtpFields(); // Clear OTP fields after verification
                // showImage();
                // img.style.visibility="visible";
                // enableSubmitButton();
                // closePopup(); // Close the popup after Submit
                // Reload the page
                // window.location.reload();
            } else {
                messageElement.textContent = 'Invalid OTP. Please Try Again.';
                // alert('Invalid OTP. Please try again.');
                // img.style.visibility="visible";
            }
        });
    }

    
        // /////////////////////////////////////////////////////


    function moveFocus(event, nextFieldId) {
        if (event.target.value.length === 1 && nextFieldId) {
            document.getElementById(nextFieldId).focus();
        }
    }

    function closePopup() {
        console.log('Close Popup Function Called');

        document.getElementById('num_verify').value = '1';
        document.getElementById('otpPopup').style.display = 'none';
        showImage();
        enableSubmitButton(); // Enable submit button after successful OTP
        // enableSubmitButton(); // Enable submit button after successful OTP
    }

    ////// Display Verified Image Logo
    function showImage() {
        console.log('Show Image Function Called');
        var img = document.getElementById('rf_verify_image');
        img.style.visibility = 'visible';
    }

    function clearOtpFields() {
        document.getElementById('otp1').value = '';
        document.getElementById('otp2').value = '';
        document.getElementById('otp3').value = '';
        document.getElementById('otp4').value = '';

        const messageElement = document.getElementById('otpMessage');
        messageElement.textContent = '';

        closePopup(); // Close the popup after Clearing Fields and Submit
        // Reload the page
        // window.location.reload();
        // setTimeout(function(){
        //     window.location.reload();
        // }, 2000);
    }

    function cancelOtpPopup() {
        document.getElementById('otp1').value = '';
        document.getElementById('otp2').value = '';
        document.getElementById('otp3').value = '';
        document.getElementById('otp4').value = '';

        const messageElement = document.getElementById('otpMessage');
        messageElement.textContent = '';

        document.getElementById('otpPopup').style.display = 'none';
        // closePopup(); // Close the popup after Clearing Fields and Submit
        // Reload the page
        // window.location.reload();
        // setTimeout(function(){
        //     window.location.reload();
        // }, 2000);
    }

    // function enableSubmitButton() {
    //     console.log('Enable Submit Button Called');
    //     const submitBtn = document.getElementById('submitBtn');
    //     submitBtn.classList.remove('disabled');
    //     submitBtn.disabled = false; // Enable submit button
    //     document.getElementById('otpPopup').style.display = 'none'; //// Close OTP Popup
    // }
    function enableSubmitButton() {
        console.log('Enable Submit Button Called');
        fname_val=document.getElementById('first_name').value;
        fname_trim_val=fname_val.trim();
        // console.log(fname_trim_val);

        lname_val=document.getElementById('last_name').value;
        lname_trim_val=lname_val.trim();

        num_verify_val=document.getElementById('num_verify').value;

        email_val=document.getElementById('email_id').value;
        email_trim_val=email_val.trim();

        // terms_val=document.getElementById('tandc').value;
        terms_val=document.getElementById('tandc').checked;
        console.log('terms check val: ',terms_val)
        // city_val=document.getElementById('all_cities').value;
        // qual_val=document.getElementById('qualification').value;
        // ctype_val=document.getElementById('courses_types').value;
        // cname_val=document.getElementById('courses_names').value;

        console.log('fname_val',fname_val.length);
        // console.log('lname_val',lname_val);
        // console.log('ctype_val',num_verify_val);
        // console.log('cname_val',email_val);

        // console.log('city_val',city_val);
        // console.log('qual_val',qual_val);
        // console.log('ctype_val',ctype_val);
        // console.log('cname_val',cname_val);
        // document.getElementById('otpPopup').style.display = 'none'; //// Close OTP Popup
        // if((document.getElementById('first_name').value.trim !== '') && (!document.getElementById('last_name').value.trim !== '') && (document.getElementById('num_verify').value == '1') && (document.getElementById('email').value.trim != '') && (document.getElementById('all_cities').value.trim != '-1') && (document.getElementById('qualification').value.trim != '-1') && (document.getElementById('courses_types').value.trim != '') && (document.getElementById('courses_names').value.trim != '')){
        // if((fname_val.trim !== '') && (lname_val.trim !== '') && (num_verify_val === '1') && (email_val.trim !== '') && (city_val.trim !== '-1') && (qual_val.trim !== '-1') && (ctype_val.trim !== '-1') && (cname_val.trim !== '-1')){
        if((fname_trim_val.length > 0) && (lname_trim_val.length > 0) && (email_trim_val.length > 0) && (num_verify_val=='1') && (terms_val=='true')){
            console.log("if Condition Satisfied");
            const submitBtn = document.getElementById('register_btn');
            submitBtn.classList.remove('disabled');
            submitBtn.disabled = false; // Enable submit button

            // hideEnquiryFormPopup();
            document.getElementById('otpPopup').style.display = 'none'; //// Close OTP Popup
        }
        else{
            console.log("Else Condition Satisfied");
            const submitBtn = document.getElementById('register_btn');
            submitBtn.classList.add('disabled');
            submitBtn.disabled = true; // Enable submit button
        }
        
    }

    function submitForm() {
        // Submit the form if the submit button is enabled
        if (!document.getElementById('register_btn').disabled) {
            // document.getElementById('enquiryForm').submit();
            document.getElementById('form').submit();

            //// Close the Enquiry Form
            document.getElementById('enquiryPopup').style.display = 'none';

            setTimeout(() => {
                window.location.reload();
            }, 2000); // Submit form after 1 second
        }
    }


    function checktermsvalue(){
        // gterms_val=document.getElementById('tandc2').value;
        gterms_chk=document.getElementById('tandc').checked;
        // console.log(gterms_val);
        console.log(gterms_chk);
        // enableSubmitButton()
    }
    /////////////////////// Enquiry Form on Popup
    // $(function(){
    //     $('#test').click(function(){
    //         // You need to get the attribute from the element
    //         var error = $(this).attr('value');
    //     });
    // });

    // function showEnquiryFormPopup(ele) {
    //     document.getElementById('enquiryPopup').style.display = 'flex';

    //     // var btnValue = ele.innerText;
    //     var brochure_btn_val = ele.value;
    //     console.log(brochure_btn_val);
    //     // button_val=document.getElementById('download_brochure').value;
    //     // brochure_btn = document.getElementsByClassName("download_brochure");
    //     // brochure_btn_val=brochure_btn[0].value;

    //     // console.log(bro_btn_val[0].value);
    //     // button_val=bro_btn_val;
    //     // button_val=this.;
    //     document.getElementById('brochure_name').value=brochure_btn_val;
    //     console.log('button_val');
    //     console.log(brochure_btn_val);
    // }
    // var img = document.getElementById('verify_image');
    // img.style.visibility = 'hidden';

    // function hideEnquiryFormPopup() {
    //     console.log('Hide Enquiry Form');
    //     // document.getElementById('enquiryPopup').style.display = 'none';

    //     document.getElementById('first_name').value = '';
    //     document.getElementById('last_name').value = '';
    //     document.getElementById('mobile').value = '';
    //     document.getElementById('email').value = '';
    //     document.getElementById('message').value = '';

    //     document.getElementById('num_verify').value = '';

    //     var city_rst = document.querySelectorAll('#all_cities option');
    //     for (var i = 0, l = city_rst.length; i < l; i++) {
    //         city_rst[i].selected = city_rst[i].defaultSelected;
    //     }

    //     var qual_rst = document.querySelectorAll('#qualification option');
    //     for (var i = 0, l = qual_rst.length; i < l; i++) {
    //         qual_rst[i].selected = qual_rst[i].defaultSelected;
    //     }

    //     var c_type_rst = document.querySelectorAll('#courses_types option');
    //     for (var i = 0, l = c_type_rst.length; i < l; i++) {
    //         c_type_rst[i].selected = c_type_rst[i].defaultSelected;
    //     }

    //     var c_name_rst = document.querySelectorAll('#courses_names option');
    //     for (var i = 0, l = c_name_rst.length; i < l; i++) {
    //         c_name_rst[i].selected = c_name_rst[i].defaultSelected;
    //     }

    //     // $('#my_select option').prop('selected', function() {
    //     //     return this.defaultSelected;
    //     // });

    //     const submitBtn = document.getElementById('submitBtn');
    //     submitBtn.classList.add('disabled');
    //     submitBtn.disabled = true; // Enable submit button

    //     const otpBtn = document.getElementById('otpbtn');
    //     otpBtn.classList.add('disabled');
    //     otpBtn.disabled = true; // Enable submit button

    //     var img = document.getElementById('rf_verify_image');
    //     img.style.visibility = 'hidden';


    //     const messageElement = document.getElementById('otpMessage');
    //     messageElement.textContent = '';

    //     document.getElementById('enquiryPopup').style.display = 'none';
    // }


    // function closeEnquiyForm(){
    //     document.getElementById('enquiryPopup').style.display = 'none';
    // }


    

    function enableOTPbtn() {
        // alert("You pressed a key inside the input field");
        var mobile_value = document.getElementById("mobile").value;
        mobile_value_length=mobile_value.length;
        // console.log(mobile_value_length);
        // if (mobile_value_length > 8) {
        if (mobile_value_length > 9) {
        // if (mobile_value_length === 9) {
            enableOTPButton();
            // alert("Submitted successfully!");
        } else {
            disableOTPButton();
            // event.preventDefault();
            // console.log('Need Ten Numbers');
            // alert("Enter ten numbers");
        }
        
    }

    
//     document.getElementById('mobile').addEventListener('keydown', function (event) {
//     if (event.keyCode == 8) {
//         console.log('BACKSPACE was pressed');
//     }
//     if (event.keyCode == 46) {
//         console.log('DELETE was pressed');
//     }
// });

    // /////////////////// JQuery Code
    // $(".mobile").keypress(function (e) {
    //     alert('Key Pressed');
    //     let myArray = [];
    //     for (i = 48; i < 58; i++) myArray.push(i);
    //     if (!(myArray.indexOf(e.which) >= 0)) e.preventDefault();

    //     if ($(".mobile").val().length === 10) {
    //         alert("Submitted successfully!");
    //     } else {
    //         e.preventDefault();
    //         console.log('Need Ten Numbers');
    //         // alert("Enter ten numbers");
    //     }
    // });
    // $("form").submit(function (e) {
    //     if ($(".mobile").val().length === 10) {
    //         alert("Submitted successfully!");
    //     } else {
    //         e.preventDefault();
    //         alert("Enter ten numbers");
    //     }
    // });
    // function himg() {
    //     var img = document.getElementById('rf_verify_image');
    //     img.style.visibility='hidden';
    // }
    // himg();


    ////////////////////////// Terms and Conditions JS Starts
    document.addEventListener("DOMContentLoaded", function() {
    // Get elements
const popupt = document.getElementById('popupt');
const openPopupt = document.getElementById('openPopupt');
const closePopupt = document.getElementById('closePopupt');
const acceptBtn = document.getElementById('acceptBtn');
const checkbox = document.getElementById('tandc');

// Open the popup when the button is clicked
openPopupt.onclick = function() {
    console.log('popup function called');
    popupt.style.display = 'block';
}

function Openpopupfun(){
    console.log('popup function called');
    popupt.style.display = 'block';
}

// Close the popup when the close button is clicked
closePopupt.onclick = function() {
    popupt.style.display = 'none';
}

// Close the popup when clicking outside of the popup content
window.onclick = function(event) {
    if (event.target === popupt) {
        popupt.style.display = 'none';
    }
}

// Enable the Accept button when the checkbox is checked
checkbox.onchange = function() {
    acceptBtn.disabled = !this.checked;
}

// Handle the Accept button click
acceptBtn.onclick = function() {
    alert('You have accepted the terms and conditions!');
    popupt.style.display = 'none'; // Close the popup after acceptance
    checktermsvalue();
    enableSubmitButton();
}
    })